import streamlit as st
import datetime

# Importamos las clases definidas en la carpeta models
from models.cliente import Cliente
from models.reserva import Reserva

# ==========================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS BOUTIQUE
# ==========================================
st.set_page_config(
    page_title="tour.app | Platform",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,500;0,9..40,700&family=Playfair+Display:ital,wght@0,600;0,800&display=swap');

    .stApp { background-color: #FAFAFA !important; font-family: 'DM Sans', sans-serif !important; color: #2B2B2B !important; }
    #MainMenu, footer, header, .stDeployButton {visibility: hidden; display:none;}

    h1 { font-family: 'Playfair Display', serif !important; color: #3B1219 !important; font-size: 2.3rem !important; font-weight: 800 !important; }
    h2, h3, h4 { font-family: 'Playfair Display', serif !important; color: #581845 !important; }

    .app-card { background: #FFFFFF; border-radius: 16px; padding: 24px; border: 1px solid #EAE6E1; box-shadow: 0 10px 25px rgba(88, 24, 69, 0.03); margin-bottom: 20px; }
    .reserva-card { background: #FFFFFF; border-radius: 14px; border-left: 5px solid #581845; padding: 20px; margin-bottom: 15px; border-top: 1px solid #EAE6E1; border-right: 1px solid #EAE6E1; border-bottom: 1px solid #EAE6E1; }
    .price-card { background: linear-gradient(135deg, #3B1219 0%, #581845 100%); color: #FFFFFF !important; border-radius: 14px; padding: 22px; margin-top: 15px; }
    .price-card h4 { color: #F3E5D8 !important; font-size: 1.5rem !important; margin: 0 !important; }
    .profit-card { background-color: #F2F9F6; border-left: 4px solid #27AE60; border-radius: 8px; padding: 14px 18px; color: #1E6B40; margin-top: 12px; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 10px; border-bottom: 1px solid #EAE6E1; }
    .stTabs [aria-selected="true"] { background-color: #FFFFFF !important; color: #581845 !important; border-bottom: 3px solid #581845 !important; font-weight: 700 !important; }
    .badge { background-color: #F8F1F4; color: #581845; padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; margin-right: 6px; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div>
        <h1>tour.app</h1>
        <p style="color: #8C827A; margin: 0; font-size: 0.95rem;">Plataforma de Cotización y Logística B2B · Mendoza</p>
    </div>
""", unsafe_allow_html=True)

# Inicialización de bases de datos en sesión
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

# Lista en memoria para almacenar las reservas guardadas
if 'lista_reservas' not in st.session_state:
    st.session_state.lista_reservas = []

tabs = st.tabs(["🍷 Cotizador B2B", "📋 Agenda de Reservas", "📖 Catálogo de Bodegas"])

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
        
        # Instanciamos los Objetos
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

        # Parada 1
        st.markdown("**Parada 1 (Mañana)**")
        col_b1, col_e1 = st.columns([1, 1.2])
        with col_b1:
            bodega_1 = st.selectbox("Bodega 1", lista_bodegas, key="b1", label_visibility="collapsed")
        with col_e1:
            if bodega_1 != "Sin opciones":
                exp_b1 = bodegas_zona[bodega_1]["Experiencias"]
                exp_nombres_1 = [f"{e['Nombre']} (${e['Precio']:,})" for e in exp_b1]
                idx_exp_1 = st.selectbox("Exp 1", range(len(exp_nombres_1)), format_func=lambda x: exp_nombres_1[x], key="e1", label_visibility="collapsed")
                obj_reserva.paradas.append((bodega_1, exp_b1[idx_exp_1]["Nombre"], exp_b1[idx_exp_1]["Precio"]))

        # Parada 2
        st.markdown("**Parada 2 (Almuerzo)**")
        col_b2, col_e2 = st.columns([1, 1.2])
        with col_b2:
            bodega_2 = st.selectbox("Bodega 2", lista_bodegas, key="b2", label_visibility="collapsed")
        with col_e2:
            if bodega_2 != "Sin opciones":
                exp_b2 = bodegas_zona[bodega_2]["Experiencias"]
                exp_nombres_2 = [f"{e['Nombre']} (${e['Precio']:,})" for e in exp_b2]
                idx_exp_2 = st.selectbox("Exp 2", range(len(exp_nombres_2)), format_func=lambda x: exp_nombres_2[x], key="e2", label_visibility="collapsed")
                obj_reserva.paradas.append((bodega_2, exp_b2[idx_exp_2]["Nombre"], exp_b2[idx_exp_2]["Precio"]))

        # Parada 3
        st.markdown("**Parada 3 (Tarde / Sunset)**")
        col_b3, col_e3 = st.columns([1, 1.2])
        with col_b3:
            bodega_3 = st.selectbox("Bodega 3", lista_bodegas, key="b3", label_visibility="collapsed")
        with col_e3:
            if bodega_3 != "Sin opciones":
                exp_b3 = bodegas_zona[bodega_3]["Experiencias"]
                exp_nombres_3 = [f"{e['Nombre']} (${e['Precio']:,})" for e in exp_b3]
                idx_exp_3 = st.selectbox("Exp 3", range(len(exp_nombres_3)), format_func=lambda x: exp_nombres_3[x], key="e3", label_visibility="collapsed")
                obj_reserva.paradas.append((bodega_3, exp_b3[idx_exp_3]["Nombre"], exp_b3[idx_exp_3]["Precio"]))

        # Cálculo de Totales de la Reserva
        obj_reserva.calcular_totales(tipo_margen, valor_margen)
        
        km_1 = bodegas_zona[bodega_1]["Km"] if bodega_1 in bodegas_zona else 0
        km_2 = bodegas_zona[bodega_2]["Km"] if bodega_2 in bodegas_zona else 0
        km_3 = bodegas_zona[bodega_3]["Km"] if bodega_3 in bodegas_zona else 0
        km_totales = sum([km_1, km_2, km_3]) + 20

        st.markdown(f"""
        <div class="price-card">
            <h4>$ {obj_reserva.precio_total_cliente:,.0f} ARS</h4>
            <small>Precio Paquete Cerrado ({obj_reserva.cant_pax} pax) · Idioma: {obj_reserva.cliente.idioma}</small>
        </div>
        <div class="profit-card">
            📈 Ganancia Libre Agencia: $ {obj_reserva.ganancia_agencia:,.0f} ARS
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # BOTÓN PRINCIPAL: GUARDAR LA RESERVA EN LA AGENDA
        if st.button("💾 Guardar y Registrar Reserva", use_container_width=True):
            st.session_state.lista_reservas.append(obj_reserva)
            st.success(f"¡Reserva de {obj_reserva.cliente.nombre} guardada con éxito en la Agenda!")
            
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 4. Salida de Mensajes Rápida")
    
    with st.expander("📲 Generar Mensaje para el Cliente", expanded=False):
        guia_txt = f"\n• Guía turístico profesional acompañante: {obj_reserva.guia_nombre}." if (obj_reserva.incluye_guia and obj_reserva.guia_nombre) else ("\n• Guía turístico profesional acompañante." if obj_reserva.incluye_guia else "")
        
        p1_txt = f"{obj_reserva.paradas[0][0]} ➔ {obj_reserva.paradas[0][1]}" if len(obj_reserva.paradas) > 0 else ""
        p2_txt = f"{obj_reserva.paradas[1][0]} ➔ {obj_reserva.paradas[1][1]}" if len(obj_reserva.paradas) > 1 else ""
        p3_txt = f"{obj_reserva.paradas[2][0]} ➔ {obj_reserva.paradas[2][1]}" if len(obj_reserva.paradas) > 2 else ""

        msg_cliente = f"""¡Hola {obj_reserva.cliente.nombre}! ✨
Esta es la propuesta personalizada que más se ajusta a lo que nos solicitaron:

🗓 *Fecha:* {obj_reserva.fecha.strftime('%d/%m/%Y')}
📍 *Punto de retiro:* {obj_reserva.cliente.hospedaje}
⏰ *Hora de salida:* 09:30 hs
👥 *Pasajeros:* {obj_reserva.cant_pax} personas ({obj_reserva.cliente.idioma})

🍷 *ITINERARIO EXCLUSIVO ({obj_reserva.zona}):*
1️⃣ *10:30 hs* - {p1_txt}
2️⃣ *13:00 hs* - {p2_txt}
3️⃣ *17:00 hs* - {p3_txt}

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
        
        msg_chofer = f"""¡Hola {obj_reserva.chofer_nombre}! 👋
Tenemos un traslado disponible para el día *{obj_reserva.fecha.strftime('%d/%m/%Y')}*.

👥 *Cantidad de pasajeros:* {obj_reserva.cant_pax} pax (Idioma: {obj_reserva.cliente.idioma})
🏨 *Lugar de retiro:* {obj_reserva.cliente.hospedaje}{guia_chofer_txt}
📍 *Itinerario:*
• Parada 1: {bodega_1} - 10:30 hs
• Parada 2: {bodega_2} - 13:00 hs
• Parada 3: {bodega_3} - 17:00 hs

Auditoría de recorrido: ~{km_totales} km totales
💰 *Monto a pagar al chofer:* ${obj_reserva.monto_chofer:,.0f}

¿Tenés disponibilidad para realizarlo? ¡Avisanos y te lo asignamos! 👍"""
        st.text_area("Copia para Chofer:", msg_chofer, height=260)

# ------------------------------------------
# TAB 2: AGENDA Y GESTIÓN DE RESERVAS (CRM)
# ------------------------------------------
with tabs[1]:
    st.markdown("### Agenda & Gestión de Reservas")
    st.caption("Administración de solicitudes cargadas, actualización de pagos y seguimiento de estados.")
    
    if not st.session_state.lista_reservas:
        st.info("Aún no hay reservas guardadas. Cotizá una propuesta en la primera pestaña y apretá el botón 'Guardar y Registrar Reserva'.")
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
                # Controles para cambiar estado en tiempo real
                res.estado_reserva = st.selectbox(
                    "Estado Reserva", 
                    ["A Confirmar", "Reservado", "Cancelado"], 
                    index=["A Confirmar", "Reservado", "Cancelado"].index(res.estado_reserva),
                    key=f"res_est_{idx}"
                )
                res.estado_pago = st.selectbox(
                    "Estado Pago", 
                    ["Pendiente", "Señado (50%)", "Saldado (100%)"], 
                    index=["Pendiente", "Señado (50%)", "Saldado (100%)"].index(res.estado_pago),
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
                
                tags_html = "".join([f'<span class="badge">{tag}</span>' for tag in b_data.get("Tags", [])])
                st.markdown(tags_html, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown("**Experiencias Disponibles:**")
                for exp in b_data["Experiencias"]:
                    st.markdown(f"• **{exp['Nombre']}**: ${exp['Precio']:,} ARS por persona")
                    
            st.markdown('</div>', unsafe_allow_html=True)