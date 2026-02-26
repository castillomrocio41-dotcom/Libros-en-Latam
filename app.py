import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Configuración de página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Mercado Editorial LATAM",
    page_icon="📚",
    layout="wide"
)

# ── Carga de datos ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("mercado_editorial_latam_2000_2025.csv")
    return df

df = load_data()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📚 Mercado Editorial de América Latina (2000–2025)")
st.markdown("**7 países · 25 años · Fuentes: CAL, CANIEM, CERLALC, CCL, CCdL, BNP, BNB**")
st.caption("Los datos de 2025 son estimaciones basadas en tendencias de 2024.")

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.header("🔎 Filtros globales")

anio_min, anio_max = st.sidebar.slider(
    "Rango de años", 2000, 2025, (2000, 2025)
)

paises_disponibles = sorted(df["pais"].unique())
paises_sel = st.sidebar.multiselect(
    "Países", paises_disponibles, default=paises_disponibles
)

df_f = df[
    (df["anio"] >= anio_min) &
    (df["anio"] <= anio_max) &
    (df["pais"].isin(paises_sel))
]

if df_f.empty:
    st.warning("No hay datos con los filtros seleccionados.")
    st.stop()

# ════════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — EVOLUCIÓN DE LA PRODUCCIÓN EDITORIAL
# ════════════════════════════════════════════════════════════════════════════════
st.divider()
st.header("📦 Sección 1 · Producción Editorial por País")
st.markdown("Comparación de ejemplares producidos (millones) y títulos ISBN registrados en el tiempo.")

col1, col2 = st.columns(2)

with col1:
    fig1a = px.line(
        df_f, x="anio", y="ejemplares_producidos_millones",
        color="pais", markers=True,
        title="Ejemplares producidos (millones) por año",
        labels={"ejemplares_producidos_millones": "Millones de ejemplares", "anio": "Año", "pais": "País"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig1a.update_layout(hovermode="x unified", legend=dict(orientation="h", y=-0.25))
    st.plotly_chart(fig1a, use_container_width=True)

with col2:
    fig1b = px.line(
        df_f, x="anio", y="titulos_registrados_isbn",
        color="pais", markers=True,
        title="Títulos registrados con ISBN por año",
        labels={"titulos_registrados_isbn": "Títulos ISBN", "anio": "Año", "pais": "País"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig1b.update_layout(hovermode="x unified", legend=dict(orientation="h", y=-0.25))
    st.plotly_chart(fig1b, use_container_width=True)

# Gráfico de área apilada — participación regional
fig1c = px.area(
    df_f, x="anio", y="ejemplares_producidos_millones",
    color="pais",
    title="Participación regional en producción total (área apilada)",
    labels={"ejemplares_producidos_millones": "Millones de ejemplares", "anio": "Año", "pais": "País"},
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig1c.update_layout(hovermode="x unified", legend=dict(orientation="h", y=-0.15))
st.plotly_chart(fig1c, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — FACTURACIÓN Y ECONOMÍA DEL LIBRO
# ════════════════════════════════════════════════════════════════════════════════
st.divider()
st.header("💰 Sección 2 · Facturación y Economía del Libro")
st.markdown("Facturación estimada en USD, variación anual y ejemplares per cápita como indicador de madurez del mercado.")

col3, col4 = st.columns(2)

with col3:
    fig2a = px.bar(
        df_f, x="anio", y="facturacion_estimada_millones_usd",
        color="pais", barmode="group",
        title="Facturación estimada por país (USD millones)",
        labels={"facturacion_estimada_millones_usd": "USD millones", "anio": "Año", "pais": "País"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig2a.update_layout(hovermode="x unified", legend=dict(orientation="h", y=-0.25))
    st.plotly_chart(fig2a, use_container_width=True)

with col4:
    fig2b = px.line(
        df_f, x="anio", y="ejemplares_per_capita",
        color="pais", markers=True,
        title="Ejemplares per cápita por año",
        labels={"ejemplares_per_capita": "Ejemplares / habitante", "anio": "Año", "pais": "País"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig2b.add_hline(y=1.0, line_dash="dot", line_color="gray",
                    annotation_text="Umbral 1 ej./hab.")
    fig2b.update_layout(hovermode="x unified", legend=dict(orientation="h", y=-0.25))
    st.plotly_chart(fig2b, use_container_width=True)

# Heatmap de facturación
pivot_fact = df_f.pivot_table(
    index="pais", columns="anio", values="facturacion_estimada_millones_usd"
)
fig2c = px.imshow(
    pivot_fact,
    title="Mapa de calor — Facturación (USD millones) por país y año",
    labels=dict(color="USD M"),
    color_continuous_scale="YlOrRd",
    aspect="auto"
)
fig2c.update_layout(xaxis_title="Año", yaxis_title="País")
st.plotly_chart(fig2c, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — TENDENCIAS ESTRUCTURALES Y DIGITALIZACIÓN
# ════════════════════════════════════════════════════════════════════════════════
st.divider()
st.header("📐 Sección 3 · Tendencias Estructurales y Digitalización")
st.markdown("Caída de tirada promedio, adopción digital y comparativa del año 2025 entre países.")

col5, col6 = st.columns(2)

with col5:
    fig3a = px.line(
        df_f, x="anio", y="tirada_promedio_ejemplares",
        color="pais", markers=True,
        title="Tirada promedio por título (ejemplares)",
        labels={"tirada_promedio_ejemplares": "Ejemplares / título", "anio": "Año", "pais": "País"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig3a.update_layout(hovermode="x unified", legend=dict(orientation="h", y=-0.25))
    st.plotly_chart(fig3a, use_container_width=True)

with col6:
    df_dig = df_f[df_f["formato_digital_pct"].notna()].copy()
    if not df_dig.empty:
        fig3b = px.line(
            df_dig, x="anio", y="formato_digital_pct",
            color="pais", markers=True,
            title="Adopción de formato digital (% del mercado)",
            labels={"formato_digital_pct": "% Digital", "anio": "Año", "pais": "País"},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig3b.update_layout(hovermode="x unified", legend=dict(orientation="h", y=-0.25))
        st.plotly_chart(fig3b, use_container_width=True)
    else:
        st.info("Sin datos de digitalización para el período seleccionado.")

# Comparativa final — radar / bar con datos del último año disponible
anio_ultimo = df_f["anio"].max()
df_ultimo = df_f[df_f["anio"] == anio_ultimo].copy()

fig3c = px.bar(
    df_ultimo.sort_values("facturacion_estimada_millones_usd", ascending=True),
    x="facturacion_estimada_millones_usd", y="pais",
    orientation="h",
    color="ejemplares_per_capita",
    color_continuous_scale="Blues",
    title=f"Comparativa {anio_ultimo}: Facturación total vs. Ejemplares per cápita",
    labels={
        "facturacion_estimada_millones_usd": "Facturación (USD millones)",
        "pais": "País",
        "ejemplares_per_capita": "Ej. / hab."
    },
    text="facturacion_estimada_millones_usd"
)
fig3c.update_traces(texttemplate="USD %{text}M", textposition="outside")
fig3c.update_layout(height=400)
st.plotly_chart(fig3c, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
with st.expander("🗂 Ver tabla de datos completa"):
    st.dataframe(df_f, use_container_width=True, height=400)
    st.download_button(
        "⬇️ Descargar CSV filtrado",
        df_f.to_csv(index=False).encode("utf-8"),
        file_name=f"latam_libros_{anio_min}_{anio_max}.csv",
        mime="text/csv"
    )
st.caption("Fuentes: CAL (Argentina), CANIEM (México), CCL (Colombia), CCdL (Chile), CERLALC, BNP (Perú), BNB (Bolivia), BCE (Ecuador) · 2025 = estimado")
