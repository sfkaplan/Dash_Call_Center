#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import plotly.express as px

# Datos de ejemplo
data = [
    {"Tipo de Problema": "Sin conexión Wi-Fi", "Región": "Norte", "Agente": "Agente A", "Nº de Casos": 120, "AHT Promedio (min)": 14.8},
    {"Tipo de Problema": "Sin conexión Wi-Fi", "Región": "Sur", "Agente": "Agente B", "Nº de Casos": 95, "AHT Promedio (min)": 17.1},
    {"Tipo de Problema": "Luz roja en router", "Región": "Norte", "Agente": "Agente A", "Nº de Casos": 80, "AHT Promedio (min)": 9.6},
    {"Tipo de Problema": "Luz roja en router", "Región": "Sur", "Agente": "Agente C", "Nº de Casos": 70, "AHT Promedio (min)": 11.2},
    {"Tipo de Problema": "Contraseña olvidada", "Región": "Centro", "Agente": "Agente B", "Nº de Casos": 150, "AHT Promedio (min)": 5.2},
    {"Tipo de Problema": "Problema con cableado", "Región": "Sur", "Agente": "Agente D", "Nº de Casos": 40, "AHT Promedio (min)": 18.4},
    {"Tipo de Problema": "Microcortes intermitentes", "Región": "Norte", "Agente": "Agente E", "Nº de Casos": 60, "AHT Promedio (min)": 13.9},
]

df = pd.DataFrame(data)
df["% Casos Totales"] = (df["Nº de Casos"] / df["Nº de Casos"].sum() * 100).round(1)

st.title("📞 Dashboard de AHT por Tipo de Problema, Región y Agente")

# Filtros
col1, col2, col3 = st.columns(3)
tipo_selected = col1.multiselect("Filtrar por Tipo de Problema", df["Tipo de Problema"].unique(), default=df["Tipo de Problema"].unique())
region_selected = col2.multiselect("Filtrar por Región", df["Región"].unique(), default=df["Región"].unique())
agente_selected = col3.multiselect("Filtrar por Agente", df["Agente"].unique(), default=df["Agente"].unique())

# Aplicar filtros
df_filtered = df[
    df["Tipo de Problema"].isin(tipo_selected) &
    df["Región"].isin(region_selected) &
    df["Agente"].isin(agente_selected)
]

# Mostrar tabla
st.subheader("📋 Datos Filtrados")
st.dataframe(df_filtered)

# Gráfico de barras: AHT por Tipo de Problema
st.subheader("📊 AHT Promedio por Tipo de Problema")
fig1 = px.bar(df_filtered.groupby("Tipo de Problema")["AHT Promedio (min)"].mean().reset_index(),
              x="Tipo de Problema", y="AHT Promedio (min)",
              color="AHT Promedio (min)", color_continuous_scale="Blues")
st.plotly_chart(fig1, use_container_width=True)

# Gráfico de calor: AHT por Región y Tipo de Problema
st.subheader("🌡️ Mapa de Calor: AHT por Región y Tipo de Problema")
heatmap_data = df_filtered.pivot_table(index="Región", columns="Tipo de Problema", values="AHT Promedio (min)", aggfunc="mean")
st.dataframe(heatmap_data.style.background_gradient(cmap='Blues', axis=None))

# Top agentes con mayor AHT
st.subheader("🏆 Top Agentes con Mayor AHT")
top_agentes = df_filtered.groupby("Agente")["AHT Promedio (min)"].mean().reset_index().sort_values(by="AHT Promedio (min)", ascending=False)
st.dataframe(top_agentes)

st.caption("Creado con ❤️ por Samuel y ChatGPT")

