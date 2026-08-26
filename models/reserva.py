class Reserva:
    def __init__(self, cliente, fecha, zona, cant_pax):
        self.cliente = cliente
        self.fecha = fecha
        self.zona = zona
        self.cant_pax = cant_pax
        
        # Estados flexibles para B2B
        self.estado_reserva = "A Confirmar"  # A Confirmar, Reservado, Cancelado
        self.estado_pago = "Pendiente"      # Pendiente, Señado (50%), Saldado (100%)
        
        # Detalle del itinerario
        self.paradas = []  # Tuplas de (nombre_bodega, nombre_exp, precio_exp)
        
        # Guía y Chofer
        self.incluye_guia = False
        self.guia_nombre = ""
        self.costo_guia = 0.0
        self.costo_traslado_neto = 0.0
        self.monto_chofer = 0.0
        self.chofer_nombre = ""
        
        # Totales
        self.ganancia_agencia = 0.0
        self.precio_total_cliente = 0.0

    def calcular_totales(self, tipo_margen: str, valor_margen: float):
        costo_bodegas = sum(precio for _, _, precio in self.paradas) * self.cant_pax
        costo_neto_total = costo_bodegas + self.costo_traslado_neto + self.costo_guia
        
        if tipo_margen == "Porcentaje (%)":
            self.ganancia_agencia = costo_neto_total * (valor_margen / 100)
        else:
            self.ganancia_agencia = valor_margen
            
        self.precio_total_cliente = costo_neto_total + self.ganancia_agencia