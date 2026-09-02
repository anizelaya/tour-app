import streamlit as st
import datetime

# Importamos las clases definidas en la carpeta models
from models.cliente import Cliente
from models.reserva import Reserva

# ==========================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS FORZADOS
# ==========================================
st.set_page_config(
    page_title="tour.app | Platform",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos globales agresivos contra el Dark Mode móvil
st.markdown("""
    <style>
    :root { color-scheme: light !important; }

    .stApp, .main, [data-testid="stAppViewContainer"] { 
        background-color: #FAFAFA !important; 
        color: #1A1A1A !important; 
    }

    #MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none; }

    h1 { 
        font-family: 'serif' !important; 
        color: #3B1219 !important; 
        font-size: 2rem !important; 
        font-weight: 800 !important; 
    }
    h2, h3, h4, p, span, label { color: #2B2B2B !important; }

    /* Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 4px; 
        background-color: #EAE6E1 !important;
        padding: 5px !important;
        border-radius: 12px !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #F0EDE8 !important;
        border-radius: 8px !important;
        padding: 10px 16px !important;
    }
    .stTabs [data-baseweb="tab"] * {
        color: #4A4A4A !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #581845 !important;
    }
    .stTabs [aria-selected="true"] * {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    /* Contenedores y Tarjetas */
    .app-card { 
        background-color: #FFFFFF !important; 
        border: 1px solid #D1C7BD !important; 
        border-radius: 16px; 
        padding: 20px; 
        margin-bottom: 20px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); 
    }
    
    .reserva-card, .bodega-card { 
        background-color: #FFFFFF !important; 
        border: 1px solid #D1C7BD !important; 
        border-radius: 14px; 
        padding: 18px; 
        margin-bottom: 15px; 
    }

    /* Tarjeta de Precio */
    .price-card { 
        background-color: #581845 !important; 
        border-radius: 14px; 
        padding: 20px; 
        margin-top: 15px; 
    }
    .price-card * { color: #FFFFFF !important; }

    .profit-card { 
        background-color: #E8F8F5 !important; 
        border-left: 6px solid #2ECC71 !important; 
        border-radius: 8px; 
        padding: 14px; 
        margin-top: 12px; 
    }
    .profit-card * { 
        color: #0E4B26 !important; 
        font-weight: 700 !important; 
    }

    /* Formulario e Inputs */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 2px solid #581845 !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] * {
        color: #1A1A1A !important;
        font-weight: 700 !important;
    }
    input, textarea {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 2px solid #8C827A !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    .stButton > button {
        background-color: #581845 !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        border: none !important;
    }
    .stButton > button * {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }

    .badge { 
        background-color: #F8F1F4; 
        color: #581845; 
        padding: 4px 10px; 
        border-radius: 20px; 
        font-size: 0.8rem; 
        font-weight: 700; 
        margin-right: 6px; 
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown("""
    <div style="padding-bottom: 10px;">
        <h1 style="color: #3B1219 !important;">tour.app</h1>
        <p style="color: #666666 !important; margin: 0; font-size: 0.95rem;">Plataforma de Cotización B2B · Mendoza</p>
    </div>
""", unsafe_allow_html=True)

# Base de Datos inicial
if 'bodegas_db' not in st.session_state:
    st.session_state.bodegas_db = {
        "Finca Bandini": {
            "Zona": "Luján y Maipú", "Km": 35,
            "Imagen": "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?q=80&w=600&auto=format&fit=crop",
            "Tags": ["Alta Gama", "Vistas Montaña", "Sunset"],
            "Experiencias": [
                {"Nombre": "Degustación Terroir (3 vinos)", "Precio": 18000},
                {"Nombre": "Degustación Íconos Premium (5 vinos)", "Precio": 28000},
                {"Nombre": "Almuerzo 3 Pasos Maridado", "Precio": 58000},
                {"Nombre": "Sunset Bandini (Incluye 2 tragos)", "Precio": 25000}
            ]
        },
        "Bodega Los Toneles": {
            "Zona": "Luján y Maipú", "Km": 15,
            "Imagen": "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?q=80&w=600&auto=format&fit=crop",
            "Tags": ["Apta Niños", "Cafetería", "Restaurante Abrasado"],
            "Experiencias": [
                {"Nombre": "Degustación Abrasado Clásica", "Precio": 15000},
                {"Nombre": "Almuerzo Menú Abrasado (Carnes)", "Precio": 48000},
                {"Nombre": "Cafetería y Pastelería de Autor", "Precio": 11000}
            ]
        },
        "Viñedos Entre Dos": {
            "Zona": "Luján y Maipú", "Km": 30,
            "Imagen": "https://images.unsplash.com/photo-1528823872057-9c018a7a80b9?q=80&w=600&auto=format&fit=crop",
            "Tags": ["Apta Niños", "Cafetería", "Jardines"],
            "Experiencias": [
                {"Nombre": "Degustación de Alfajores & Vinos", "Precio": 12000},
                {"Nombre": "Almuerzo Informal en los Jardines", "Precio": 32000},
                {"Nombre": "Cafetería & Opciones Dulces", "Precio": 9500}
            ]
        },
        "Andeluna Cellars": {
            "Zona": "Valle de Uco Corto", "Km": 85,
            "Imagen": "https://images.unsplash.com/photo-1560493676-04071c5f467b?q=80&w=600&auto=format&fit=crop",
            "Tags": ["Alta Gama", "Cordillera", "Sunset"],
            "Experiencias": [
                {"Nombre": "Degustación Edición Limitada", "Precio": 26000},
                {"Nombre": "Almuerzo 6 Pasos Altura", "Precio": 68000},
                {"Nombre": "Tarde de Té / Cafetería en la Montaña", "Precio": 18000}
            ]
        }
    }

if 'lista_reservas' not in st.session_state:
    st.session_state.lista_reservas = []

tabs = st.tabs(["🍷 Cotizador B2B", "📋 Agenda de Reservas", "📖 Catálogo de Bodegas", "⚙️ Panel Admin"])

# ------------------------------------------
# TAB 1: COTIZADOR & ARMADOR
# ------------------------------------------
with tabs[0]:
    col_left, col_right = st.columns([1.1, 1.9], gap="large")
    
    with col_left:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("### 1. Parámetros del Tour")
        cliente_nombre = st.text_input("Cliente / Pasajero Principal", "Mariana Gómez")
        
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            fecha_tour = st.date_input("Fecha del Tour", datetime.date.today())
            cant_pax = st.number_input("Pasajeros", min_value=1, max_value=17, value=2)
        with c_p2:
            idioma_cliente = st.selectbox("Idioma Preferido", ["Español", "Inglés", "Portugués", "Francés"])
            zona_elegida = st.selectbox("Circuito", ["Luján y Maipú", "Valle de Uco Corto", "Valle de Uco Largo"])
            
        hospedaje = st.text_input("Punto de Retiro / Hospedaje", "Hotel Park Hyatt Mendoza")
        
        obj_cliente = Cliente(nombre=cliente_nombre, idioma=idioma_cliente, hospedaje=hospedaje)
        obj_reserva = Reserva(cliente=obj_cliente, fecha=fecha_tour, zona=zona_elegida, cant_pax=cant_pax)
        
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("### 2. Servicios Extras & Logística")

        obj_reserva.incluye_guia = st.checkbox("🚩 Incluir Guía Turístico Profesional")
        if obj_reserva.incluye_guia:
            c_g1, c_g2 = st.columns(2)
            with c_g1:
                obj_reserva.guia_nombre = st.text_input("Nombre del Guía", "Daiana")
            with c_g2:
                obj_reserva.costo_guia = st.number_input("Honorarios Guía ($)", value=35000, step=5000)

        st.markdown("---")
        obj_reserva.costo_traslado_neto = st.number_input("Costo Neto Traslado ($)", value=70000, step=5000)
        obj_reserva.monto_chofer = st.number_input("Monto Pago Chofer ($)", value=60000, step=5000)
        obj_reserva.chofer_nombre = st.text_input("Chofer Asignado", "Carlos")
        
        st.markdown("---")
        tipo_margen = st.radio("Cálculo de Ganancia Agencia:", ["Porcentaje (%)", "Monto Fijo ($)"], horizontal=True)
        
        if tipo_margen == "Porcentaje (%)":
            valor_margen = st.slider("Porcentaje de Ganancia", min_value=0, max_value=50, value=20)
        else:
            valor_margen = st.number_input("Ganancia Fija Deseada ($)", value=25000, step=5000)
            
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("### 3. Itinerario & Experiencias")
        
        bodegas_zona = {
            nombre: datos for nombre, datos in st.session_state.bodegas_db.items() 
            if datos["Zona"] == zona_elegida
        }
        lista_bodegas = list(bodegas_zona.keys()) or ["Sin opciones"]

        # Control de paradas dinámicas con botones + y -
        if 'cant_paradas' not in st.session_state:
            st.session_state.cant_paradas = 3

        col_p1, col_p2 = st.columns([3, 1])
        with col_p1:
            st.caption(f"Cantidad de paradas: {st.session_state.cant_paradas}")
        with col_p2:
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("➕", help="Agregar parada (máx. 5)") and st.session_state.cant_paradas < 5:
                    st.session_state.cant_paradas += 1
                    st.rerun()
            with c_btn2:
                if st.button("➖", help="Quitar parada (mín. 1)") and st.session_state.cant_paradas > 1:
                    st.session_state.cant_paradas -= 1
                    st.rerun()

        # Renderizado dinámico de paradas
        for i in range(st.session_state.cant_paradas):
            st.markdown(f"**Parada {i+1}**")
            col_b, col_e = st.columns([1, 1.2])
            
            with col_b:
                bodega_sel = st.selectbox(
                    f"Bodega {i+1}", 
                    lista_bodegas, 
                    key=f"b_{i}", 
                    label_visibility="collapsed"
                )
            with col_e:
                if bodega_sel != "Sin opciones":
                    exp_b = bodegas_zona[bodega_sel]["Experiencias"]
                    exp_nombres = [f"{e['Nombre']} (${e['Precio']:,})" for e in exp_b]
                    idx_exp = st.selectbox(
                        f"Exp {i+1}", 
                        range(len(exp_nombres)), 
                        format_func=lambda x: exp_nombres[x], 
                        key=f"e_{i}", 
                        label_visibility="collapsed"
                    )
                    obj_reserva.paradas.append((bodega_sel, exp_b[idx_exp]["Nombre"], exp_b[idx_exp]["Precio"]))

        # Cálculos de Totales
        obj_reserva.calcular_totales(tipo_margen, valor_margen)
        
        # Recorrido dinámico en KM
        km_paradas = [bodegas_zona[p[0]]["Km"] for p in obj_reserva.paradas if p[0] in bodegas_zona]
        km_totales = sum(km_paradas) + 20 if km_paradas else 20

        st.markdown(f"""
        <div class="price-card">
            <h4>$ {obj_reserva.precio_total_cliente:,.0f} ARS</h4>
            <small>Precio Paquete Cerrado ({obj_reserva.cant_pax} pax) · {len(obj_reserva.paradas)} Parada/s</small>
        </div>
        <div class="profit-card">
            📈 Ganancia Libre Agencia: $ {obj_reserva.ganancia_agencia:,.0f} ARS
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("💾 Guardar y Registrar Reserva", use_container_width=True):
            st.session_state.lista_reservas.append(obj_reserva)
            st.success(f"¡Reserva de {obj_reserva.cliente.nombre} registrada!")
            
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 4. Salida de Mensajes Rápida")
    
    with st.expander("📲 Generar Mensaje para el Cliente", expanded=False):
        guia_txt = f"\n• Guía turístico profesional acompañante: {obj_reserva.guia_nombre}." if (obj_reserva.incluye_guia and obj_reserva.guia_nombre) else ("\n• Guía turístico profesional acompañante." if obj_reserva.incluye_guia else "")
        
        paradas_txt_cliente = ""
        for idx_p, p_item in enumerate(obj_reserva.paradas):
            paradas_txt_cliente += f"\n{idx_p+1}️⃣ *Parada {idx_p+1}:* {p_item[0]} ➔ {p_item[1]}"

        msg_cliente = f"""¡Hola {obj_reserva.cliente.nombre}! ✨
Esta es la propuesta personalizada que más se ajusta a lo que nos solicitaron:

🗓 *Fecha:* {obj_reserva.fecha.strftime('%d/%m/%Y')}
📍 *Punto de retiro:* {obj_reserva.cliente.hospedaje}
⏰ *Hora de salida:* 09:30 hs
👥 *Pasajeros:* {obj_reserva.cant_pax} personas ({obj_reserva.cliente.idioma})

🍷 *ITINERARIO EXCLUSIVO ({obj_reserva.zona}):*{paradas_txt_cliente}

🚘 *Servicio Incluido:*
• Traslado privado exclusivo ida y vuelta en servicio ejecutivo.{guia_txt}
• Accesos y reservas confirmadas en cada establecimiento.

💵 *PRECIO TOTAL DEL PAQUETE:* *${obj_reserva.precio_total_cliente:,.0f} ARS*

📌 *Condiciones de Reserva:*
_Para congelar tarifa y garantizar cupos en las bodegas, el servicio se abona de manera completa como mínimo 48 horas antes de la fecha del tour._

¿Les gustaría confirmar este itinerario para enviarles los medios de pago? 🥂"""
        st.text_area("Copia para Cliente:", msg_cliente, height=260)

    with st.expander("🚘 Generar Consulta para el Chofer", expanded=False):
        guia_chofer_txt = f"\n⚠️ *Nota:* Servicio acompañado por Guía ({obj_reserva.guia_nombre})." if (obj_reserva.incluye_guia and obj_reserva.guia_nombre) else ("\n⚠️ *Nota:* Servicio acompañado por Guía." if obj_reserva.incluye_guia else "")
        
        paradas_txt_chofer = ""
        for idx_p, p_item in enumerate(obj_reserva.paradas):
            paradas_txt_chofer += f"\n• Parada {idx_p+1}: {p_item[0]}"

        msg_chofer = f"""¡Hola {obj_reserva.chofer_nombre}! 👋
Tenemos un traslado disponible para el día *{obj_reserva.fecha.strftime('%d/%m/%Y')}*.

👥 *Cantidad de pasajeros:* {obj_reserva.cant_pax} pax (Idioma: {obj_reserva.cliente.idioma})
🏨 *Lugar de retiro:* {obj_reserva.cliente.hospedaje}{guia_chofer_txt}
📍 *Itinerario:*{paradas_txt_chofer}

Auditoría de recorrido: ~{km_totales} km totales
💰 *Monto a pagar al chofer:* ${obj_reserva.monto_chofer:,.0f}

¿Tenés disponibilidad para realizarlo? ¡Avisanos y te lo asignamos! 👍"""
        st.text_area("Copia para Chofer:", msg_chofer, height=260)

# ------------------------------------------
# TAB 2: AGENDA Y GESTIÓN DE RESERVAS
# ------------------------------------------
with tabs[1]:
    st.markdown("### Agenda & Gestión de Reservas")
    st.caption("Administración de solicitudes cargadas y seguimiento de estados.")
    
    if not st.session_state.lista_reservas:
        st.info("Aún no hay reservas guardadas. Cotizá una propuesta en la primera pestaña y hacé clic en 'Guardar y Registrar Reserva'.")
    else:
        for idx, res in enumerate(st.session_state.lista_reservas):
            st.markdown('<div class="reserva-card">', unsafe_allow_html=True)
            col_r1, col_r2, col_r3 = st.columns([2, 1.5, 1.5])
            
            with col_r1:
                st.markdown(f"#### 👤 Cliente: {res.cliente.nombre}")
                st.markdown(f"🗓 **Fecha:** {res.fecha.strftime('%d/%m/%Y')} | 👥 **Pax:** {res.cant_pax} ({res.cliente.idioma})")
                st.markdown(f"📍 **Circuito:** {res.zona} | 🏨 **Retiro:** {res.cliente.hospedaje}")
                
            with col_r2:
                st.markdown(f"💰 **Total Paquete:** ${res.precio_total_cliente:,.0f}")
                st.markdown(f"📈 **Ganancia Agencia:** ${res.ganancia_agencia:,.0f}")
                st.markdown(f"🚘 **Chofer:** {res.chofer_nombre} (${res.monto_chofer:,.0f})")
                
            with col_r3:
                res.estado_reserva = st.selectbox(
                    "Estado Reserva", 
                    ["A Confirmar", "Reservado", "Cancelado"], 
                    index=["A Confirmar", "Reservado", "Cancelado"].index(res.estado_reserva),
                    key=f"res_est_{idx}"
                )
                res.estado_pago = st.selectbox(
                    "Estado Pago", 
                    ["Pendiente", "Saldado (100%)"], 
                    index=["Pendiente", "Saldado (100%)"].index(res.estado_pago if res.estado_pago in ["Pendiente", "Saldado (100%)"] else "Pendiente"),
                    key=f"pag_est_{idx}"
                )
                
            st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# TAB 3: CATÁLOGO VISUAL
# ------------------------------------------
with tabs[2]:
    st.markdown("### Catálogo de Bodegas & Experiencias")
    st.caption("Fichas técnicas y tarifas públicas vigentes de los establecimientos vitivinícolas asociados.")
    
    filtro_zona_cat = st.selectbox("Filtrar por Zona", ["Todas", "Luján y Maipú", "Valle de Uco Corto", "Valle de Uco Largo"])
    
    for b_nombre, b_data in st.session_state.bodegas_db.items():
        if filtro_zona_cat == "Todas" or b_data["Zona"] == filtro_zona_cat:
            st.markdown('<div class="bodega-card">', unsafe_allow_html=True)
            col_img, col_info = st.columns([1, 2.2], gap="medium")
            
            with col_img:
                st.markdown(f'<img src="{b_data["Imagen"]}" style="width: 100%; border-radius: 10px; object-fit: cover; max-height: 200px;">', unsafe_allow_html=True)
                
            with col_info:
                st.markdown(f"### {b_nombre}")
                st.markdown(f"📍 **Zona:** {b_data['Zona']} | 🛣️ **Distancia estim. desde Ciudad:** {b_data['Km']} km")
                
                tags_html = "".join([f'<span class="badge" style="color:#581845 !important;">{tag}</span>' for tag in b_data.get("Tags", [])])
                st.markdown(tags_html, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown("**Experiencias Disponibles:**")
                for exp in b_data["Experiencias"]:
                    st.markdown(f"• **{exp['Nombre']}**: ${exp['Precio']:,} ARS por persona")
                    
            st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# TAB 4: PANEL DE ADMINISTRACIÓN DE BODEGAS
# ------------------------------------------
with tabs[3]:
    st.markdown("### ⚙️ Panel de Administración")
    st.caption("Gestión interna de catálogo, carga de nuevas bodegas, experiencias y actualización de tarifas.")
    
    clave_admin = st.text_input("Ingresá la contraseña de administradora:", type="password")
    
    if clave_admin == "zelaya123":
        st.success("Acceso concedido como Administradora.")
        
        col_adm1, col_adm2 = st.columns([1.2, 1], gap="large")
        
        # COLUMNA 1: CARGAR BODEGA NUEVA
        with col_adm1:
            st.markdown('<div class="app-card">', unsafe_allow_html=True)
            st.markdown("#### ➕ Cargar Nueva Bodega")
            
            nuevo_nombre = st.text_input("Nombre de la Bodega (ej. Bodega Catena Zapata)")
            nueva_zona = st.selectbox("Zona / Circuito", ["Luján y Maipú", "Valle de Uco Corto", "Valle de Uco Largo"])
            nuevos_km = st.number_input("Distancia aprox. desde Ciudad (km)", value=30, step=5)
            nueva_imagen = st.text_input("URL de Foto/Imagen", "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?q=80&w=600")
            nuevos_tags_str = st.text_input("Etiquetas / Tags (separadas por coma)", "Alta Gama, Vistas Montaña, Sunset")
            
            st.markdown("---")
            st.markdown("**Experiencias iniciales:**")
            
            exp1_nom = st.text_input("Nombre Exp 1", "Degustación Clásica")
            exp1_pre = st.number_input("Precio Exp 1 ($)", value=15000, step=1000)
            
            exp2_nom = st.text_input("Nombre Exp 2", "Almuerzo Maridado")
            exp2_pre = st.number_input("Precio Exp 2 ($)", value=45000, step=1000)
            
            if st.button("➕ Guardar Bodega en Catálogo", use_container_width=True):
                if nuevo_nombre.strip() != "":
                    tags_lista = [t.strip() for t in nuevos_tags_str.split(",") if t.strip() != ""]
                    
                    st.session_state.bodegas_db[nuevo_nombre] = {
                        "Zona": nueva_zona,
                        "Km": nuevos_km,
                        "Imagen": nueva_imagen,
                        "Tags": tags_lista,
                        "Experiencias": [
                            {"Nombre": exp1_nom, "Precio": exp1_pre},
                            {"Nombre": exp2_nom, "Precio": exp2_pre}
                        ]
                    }
                    st.success(f"¡{nuevo_nombre} cargada con éxito!")
                else:
                    st.error("Por favor ingresá un nombre válido para la bodega.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        # COLUMNA 2: MODIFICAR PRECIOS Y AGREGAR NUEVAS EXPERIENCIAS
        with col_adm2:
            st.markdown('<div class="app-card">', unsafe_allow_html=True)
            st.markdown("#### ✏️ Editar Bodega / Sumar Experiencias")
            
            bodega_sel_edit = st.selectbox("Seleccionar Bodega", list(st.session_state.bodegas_db.keys()))
            
            if bodega_sel_edit:
                datos_b = st.session_state.bodegas_db[bodega_sel_edit]
                st.markdown(f"**Bodega:** {bodega_sel_edit} ({datos_b['Zona']})")
                
                # 1. Modificar Precios Existentes
                st.markdown("---")
                st.markdown("**Precios de Experiencias Existentes:**")
                exp_modificadas = []
                for i, exp in enumerate(datos_b["Experiencias"]):
                    nuevo_p = st.number_input(
                        f"Precio para '{exp['Nombre']}' ($)", 
                        value=int(exp['Precio']), 
                        step=1000, 
                        key=f"edit_exp_{i}"
                    )
                    exp_modificadas.append({"Nombre": exp["Nombre"], "Precio": nuevo_p})
                    
                if st.button("💾 Actualizar Precios Existentes", use_container_width=True):
                    st.session_state.bodegas_db[bodega_sel_edit]["Experiencias"] = exp_modificadas
                    st.success(f"¡Precios de {bodega_sel_edit} actualizados!")

                # 2. Agregar una Nueva Experiencia a la Bodega
                st.markdown("---")
                st.markdown("**➕ Agregar Nueva Experiencia a esta Bodega:**")
                nueva_exp_nombre = st.text_input("Nombre de la nueva experiencia (ej. Picnic en Viñedos)", key="new_exp_name")
                nueva_exp_precio = st.number_input("Precio ($)", value=20000, step=1000, key="new_exp_price")
                
                if st.button("✨ Añadir Experiencia a la Bodega", use_container_width=True):
                    if nueva_exp_nombre.strip() != "":
                        st.session_state.bodegas_db[bodega_sel_edit]["Experiencias"].append({
                            "Nombre": nueva_exp_nombre,
                            "Precio": nueva_exp_precio
                        })
                        st.success(f"¡Se agregó '{nueva_exp_nombre}' a {bodega_sel_edit}!")
                    else:
                        st.warning("Escribí el nombre de la nueva experiencia antes de guardar.")
                        
            st.markdown('</div>', unsafe_allow_html=True)
            
    elif clave_admin != "":
        st.error("Contraseña incorrecta. Intentá nuevamente.")
