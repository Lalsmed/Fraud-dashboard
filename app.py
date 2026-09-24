import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Fraude E-commerce",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🛡️ Dashboard Ejecutivo de Prevención de Fraude")
st.markdown("**E-commerce Fraud Detection System** | Actualizado: Enero 2023")

# Sidebar con filtros
st.sidebar.header("🔍 Filtros")
date_range = st.sidebar.date_input(
    "Rango de fechas",
    value=(datetime(2023, 1, 1), datetime(2023, 1, 31))
)
payment_method = st.sidebar.multiselect(
    "Método de pago",
    ['Credit_Card', 'Debit_Card', 'PayPal', 'Crypto'],
    default=['Credit_Card', 'Debit_Card', 'PayPal', 'Crypto']
)

# ============================================
# SECCIÓN 1: KPIs PRINCIPALES
# ============================================
st.subheader("📊 Indicadores Clave (KPIs)")

fila1 = st.columns(2)
fila2 = st.columns(2)

with fila1[0]:
    st.metric("💰 Pérdida por Fraude", "$25,260", "-12%")
with fila1[1]:
    st.metric("📈 Tasa de Fraude", "3.74%", "-5 bps")
with fila2[0]:
    st.metric("🛡️ Pérdida Evitada", "$22,890", "+8%")
with fila2[1]:
    st.metric("⚠️ Falsos Positivos", "1.04%", "+0.2%", delta_color="inverse")

# ============================================
# SECCIÓN 2: GRÁFICOS DE TENDENCIA
# ============================================
st.subheader("📈 Análisis de Tendencias")

# Generar datos de tendencia diaria
np.random.seed(42)
dates = pd.date_range('2023-01-01', periods=30)
fraudes_diarios = [150 + i*2 + np.random.randint(-20, 20) for i in range(30)]
volumen_diario = [5000 + np.random.randint(-200, 200) for _ in range(30)]

df_trend = pd.DataFrame({
    'Fecha': dates,
    'Fraudes': fraudes_diarios,
    'Volumen': volumen_diario
})

# Gráfico 1: Tendencia dual
fig_trend = go.Figure()

fig_trend.add_trace(go.Bar(
    x=df_trend['Fecha'],
    y=df_trend['Volumen'],
    name='Volumen Total',
    yaxis='y',
    marker_color='lightblue',
    opacity=0.6
))

fig_trend.add_trace(go.Scatter(
    x=df_trend['Fecha'],
    y=df_trend['Fraudes'],
    name='Fraudes Detectados',
    yaxis='y2',
    mode='lines+markers',
    line=dict(color='red', width=3),
    marker=dict(size=8)
))

fig_trend.update_layout(
    title='Volumen de Transacciones vs Fraudes Detectados',
    xaxis_title='Fecha',
    yaxis=dict(title='Volumen Total', side='left'),
    yaxis2=dict(title='Fraudes', side='right', overlaying='y'),
    hovermode='x unified',
    height=400
)

st.plotly_chart(fig_trend, use_container_width=True)

# Gráfico 2: Heatmap Hora/Día
col_heat, col_devices = st.columns(2)

with col_heat:
    st.markdown("### 🕐 Heatmap: Hora del Día vs Día de Semana")
    
    np.random.seed(42)
    z = np.random.rand(7, 24) * 10
    z[0:3, 2:5] *= 2
    
    fig_heat = go.Figure(data=go.Heatmap(
        z=z,
        x=[f'{h:02d}:00' for h in range(24)],
        y=['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
        colorscale='Reds',
        showscale=True
    ))
    
    fig_heat.update_layout(
        xaxis_title='Hora del Día',
        yaxis_title='Día de Semana',
        height=400
    )
    
    st.plotly_chart(fig_heat, use_container_width=True)

# ============================================
# SECCIÓN 3: TABLA DE DISPOSITIVOS
# ============================================
with col_devices:
    st.markdown("### 🚨 Top Dispositivos Sospechosos")
    
    df_devices = pd.DataFrame({
        'Device ID': ['DEV_SUSP_19', 'DEV_SUSP_17', 'DEV_SUSP_14', 'DEV_SUSP_15', 'DEV_SUSP_12'],
        'Transacciones': [100, 100, 99, 98, 96],
        '% Fraude': ['100%', '100%', '100%', '100%', '100%'],
        'Monto Total': ['$6,800', '$6,500', '$6,200', '$6,100', '$5,900'],
        'Status': ['🔴 Activo', '🔴 Activo', '🟡 Revisión', '🟢 Bloqueado', '🟢 Bloqueado']
    })
    
    st.dataframe(df_devices, use_container_width=True, height=400, hide_index=True)

# ============================================
# SECCIÓN 4: ALERTAS TEMPRANAS
# ============================================
st.subheader("🚨 Alertas Tempranas")

col_alert1, col_alert2 = st.columns(2)

with col_alert1:
    st.error("""
    **⚠️ ALERTA: Spike de Fraude Detectado**
    
    - **Condición:** Tasa de fraude en última hora > 8%
    - **Actual:** 9.2% (15/01/2023 14:00)
    - **Acción:** Step-up authentication activado
    - **Impacto:** 47 transacciones bloqueadas
    """)

with col_alert2:
    st.warning("""
    **⚠️ ALERTA: Drift del Modelo**
    
    - **Condición:** PR-AUC < 0.85
    - **Actual:** 0.82 (últimas 2 semanas)
    - **Acción:** Reentrenamiento programado
    - **Fecha:** 20/01/2023
    """)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Dashboard creado por Eduardo Medina Marmolejo | Modelo: Random Forest v2.1 | Última actualización: 15/01/2023</p>
    <p>Tecnologías: Python, Streamlit, Plotly, Pandas</p>
</div>
""", unsafe_allow_html=True)
