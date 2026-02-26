# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║         MERCADO EDITORIAL DE LATINOAMÉRICA — 2000 a 2025                   ║
# ║         Dashboard interactivo construido con Streamlit + Plotly             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
#
# DESCRIPCIÓN GENERAL:
#   Este archivo es el "cerebro" de la app. Streamlit lo lee de arriba a abajo
#   y va dibujando cada componente en pantalla en el orden en que aparece.
#   No necesitás saber programación avanzada para entenderlo — cada bloque
#   tiene un comentario que explica qué hace y por qué está ahí.
#
# ARCHIVOS NECESARIOS EN LA MISMA CARPETA:
#   - app.py                                     <- este archivo
#   - mercado_editorial_latam_2000_2025.csv       <- los datos
#   - requirements.txt                            <- lista de librerías
# ──────────────────────────────────────────────────────────────────────────────

# ── IMPORTACIONES ─────────────────────────────────────────────────────────────
# Acá le decimos a Python qué herramientas vamos a usar.
# Cada "import" trae una librería con funciones ya listas para usar.

import streamlit as st             # La librería principal — crea la interfaz web
import pandas as pd                # Maneja tablas de datos (lee el CSV, filtra, agrupa)
import plotly.express as px        # Crea gráficos interactivos de forma simple
import plotly.graph_objects as go  # Para gráficos más avanzados y personalizados


# ── CONFIGURACIÓN DE LA PÁGINA ────────────────────────────────────────────────
# Esta función DEBE ser la primera llamada a Streamlit en el archivo.
# Define cómo se ve la pestaña del navegador y el layout general.

st.set_page_config(
    page_title="📚 Mercado Editorial LATAM",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ── ESTILOS PERSONALIZADOS (CSS) ──────────────────────────────────────────────
# Streamlit permite inyectar CSS para cambiar colores, fuentes y estilos.
# st.markdown con unsafe_allow_html=True nos deja escribir HTML/CSS directamente.
# Pensá en esto como el "maquillaje" de la app — no cambia los datos, solo el look.

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg-dark:      #0f1117;
    --bg-card:      #1a1d27;
    --bg-card2:     #22263a;
    --accent-gold:  #f5c842;
    --accent-coral: #ff6b6b;
    --accent-teal:  #4ecdc4;
    --accent-blue:  #74b9ff;
    --text-primary: #f0f0f0;
    --text-muted:   #8892a4;
    --border-color: rgba(245,200,66,0.2);
}

.stApp {
    background: linear-gradient(135deg, #0f1117 0%, #131825 50%, #0f1117 100%);
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.8rem !important;
    background: linear-gradient(90deg, #f5c842, #ff6b6b, #4ecdc4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem !important;
}

h2 {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.6rem !important;
    color: var(--accent-gold) !important;
    border-left: 4px solid var(--accent-gold);
    padding-left: 12px;
    margin-top: 2rem !important;
}

h3 {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--accent-teal) !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
}

div[data-testid="metric-container"] {
    background: linear-gradient(135deg, var(--bg-card), var(--bg-card2));
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(245,200,66,0.15);
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--accent-gold) !important;
    font-family: 'Playfair Display', serif !important;
}
div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

section[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border-color);
}
section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

hr { border-color: var(--border-color) !important; margin: 2rem 0 !important; }

button[data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    color: var(--text-muted) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent-gold) !important;
    border-bottom-color: var(--accent-gold) !important;
}

.insight-box {
    background: linear-gradient(135deg, rgba(245,200,66,0.08), rgba(78,205,196,0.05));
    border: 1px solid rgba(245,200,66,0.25);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    margin: 0.5rem 0 1rem 0;
    font-size: 0.9rem;
    color: #ccc;
    line-height: 1.6;
}
.insight-box strong { color: var(--accent-gold); }

.source-tag {
    font-size: 0.72rem;
    color: var(--text-muted);
    text-align: right;
    margin-top: -0.5rem;
    font-style: italic;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-dark); }
::-webkit-scrollbar-thumb { background: var(--accent-gold); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CARGA DE DATOS
# ══════════════════════════════════════════════════════════════════════════════
# @st.cache_data guarda el CSV en memoria después de la primera lectura.
# Así, cuando el usuario mueve un filtro, no se vuelve a leer el disco — más rápido.

@st.cache_data
def load_data():
    """Lee el CSV y retorna un DataFrame de pandas."""
    df = pd.read_csv("mercado_editorial_latam_2000_2025.csv")
    return df

df = load_data()


# ══════════════════════════════════════════════════════════════════════════════
# PALETA DE COLORES POR PAÍS
# ══════════════════════════════════════════════════════════════════════════════
# Colores fijos para que cada país siempre tenga el mismo color en todos los gráficos.

COLORES_PAISES = {
    "Argentina": "#f5c842",
    "México":    "#ff6b6b",
    "Colombia":  "#4ecdc4",
    "Chile":     "#74b9ff",
    "Perú":      "#a29bfe",
    "Ecuador":   "#fd79a8",
    "Bolivia":   "#55efc4",
}


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIÓN: TEMA OSCURO PARA GRÁFICOS
# ══════════════════════════════════════════════════════════════════════════════
# Una función es un bloque de código reutilizable. En vez de repetir la misma
# configuración visual en cada gráfico, la centralizamos aquí y la llamamos
# al final de cada figura con: fig = apply_dark_theme(fig)

def apply_dark_theme(fig, height=420):
    """
    Aplica el tema oscuro y estilo consistente a cualquier gráfico Plotly.
    Parámetros:
        fig    — la figura a estilizar
        height — altura en píxeles (default 420)
    """
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(26,29,39,0.8)",
        font=dict(family="DM Sans, sans-serif", color="#c0c8d8", size=12),
        title_font=dict(family="Playfair Display, serif", size=16, color="#f0f0f0"),
        legend=dict(
            bgcolor="rgba(26,29,39,0.9)",
            bordercolor="rgba(245,200,66,0.2)",
            borderwidth=1,
            font=dict(size=11),
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        hovermode="x unified",
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", showline=True,
                   linecolor="rgba(255,255,255,0.1)", tickfont=dict(size=11)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", showline=False,
                   tickfont=dict(size=11)),
        margin=dict(t=50, b=80, l=60, r=20)
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("# 📚 Mercado Editorial de América Latina")
st.markdown(
    "<p style='color:#8892a4; font-size:1.05rem; margin-top:-0.5rem;'>"
    "7 países · 25 años de datos · Fuentes: CAL, CANIEM, CERLALC, CCL, CCdL, BNP, BNB"
    "</p>", unsafe_allow_html=True
)
st.markdown(
    "<div class='source-tag'>⚠️ Los datos de 2025 son estimaciones basadas en tendencias de 2024.</div>",
    unsafe_allow_html=True
)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — FILTROS GLOBALES
# ══════════════════════════════════════════════════════════════════════════════
# Todo lo que está dentro de "with st.sidebar:" aparece en el panel lateral.
# Los filtros aquí afectan a TODOS los gráficos y secciones de la app.

with st.sidebar:
    st.markdown("### 🔎 Filtros globales")
    st.markdown("---")

    # Slider: el usuario arrastra para elegir el rango de años
    anio_min, anio_max = st.slider(
        "📅 Rango de años",
        min_value=2000, max_value=2025,
        value=(2000, 2025), step=1
    )

    st.markdown("---")

    # Multiselect: el usuario puede marcar/desmarcar países
    paises_disponibles = sorted(df["pais"].unique())
    paises_sel = st.multiselect(
        "🌎 Países",
        options=paises_disponibles,
        default=paises_disponibles
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem; color:#555; text-align:center;'>"
        "Streamlit + Plotly<br>Datos: CAL · CANIEM · CERLALC"
        "</div>", unsafe_allow_html=True
    )


# ── APLICAR FILTROS ───────────────────────────────────────────────────────────
# Filtramos el DataFrame original con los valores de los controles del sidebar.
# El operador & significa "Y" (ambas condiciones deben cumplirse).
# .isin() verifica que el país esté dentro de la lista seleccionada.

df_f = df[
    (df["anio"] >= anio_min) &
    (df["anio"] <= anio_max) &
    (df["pais"].isin(paises_sel))
].copy()

# Si el usuario desseleccionó todo, mostramos aviso y cortamos la ejecución
if df_f.empty:
    st.warning("⚠️ Seleccioná al menos un país para ver los datos.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
# Las "tarjetas métricas" muestran los números más importantes de un vistazo.
# st.columns(5) divide el ancho de la pantalla en 5 columnas iguales.

st.markdown("---")

total_ejemplares  = df_f["ejemplares_producidos_millones"].sum()
total_facturacion = df_f["facturacion_estimada_millones_usd"].sum()
max_per_capita    = df_f["ejemplares_per_capita"].max()
total_titulos     = df_f["titulos_registrados_isbn"].sum()
pais_lider        = df_f.loc[df_f["facturacion_estimada_millones_usd"].idxmax(), "pais"]
pais_lider_anio   = int(df_f.loc[df_f["facturacion_estimada_millones_usd"].idxmax(), "anio"])

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("📦 Ejemplares totales (M)", f"{total_ejemplares:,.0f}",
              help="Suma de ejemplares producidos en el período/países seleccionados")
with c2:
    st.metric("💵 Facturación total (USD M)", f"{total_facturacion:,.0f}",
              help="Suma estimada en millones de dólares")
with c3:
    st.metric("📖 Títulos ISBN", f"{total_titulos:,.0f}",
              help="Total de títulos registrados con ISBN")
with c4:
    st.metric("📊 Máx. per cápita", f"{max_per_capita:.2f}",
              help="Pico de ejemplares por habitante en el período")
with c5:
    st.metric("🥇 País líder", pais_lider, delta=f"Pico en {pais_lider_anio}")


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — PRODUCCIÓN EDITORIAL
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.header("📦 Sección 1 · Producción Editorial")
st.markdown(
    "<div class='insight-box'>💡 <strong>¿Qué muestra esta sección?</strong> "
    "La cantidad de libros fabricados y títulos nuevos registrados por año. "
    "México lidera en volumen bruto, pero Argentina es quien más produce en relación a su población.</div>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    # Gráfico de líneas: evolución de ejemplares producidos por país a lo largo del tiempo
    fig1a = px.line(df_f, x="anio", y="ejemplares_producidos_millones", color="pais",
                    markers=True, title="Ejemplares producidos (millones)",
                    labels={"ejemplares_producidos_millones": "Millones", "anio": "Año", "pais": "País"},
                    color_discrete_map=COLORES_PAISES)
    fig1a = apply_dark_theme(fig1a)
    st.plotly_chart(fig1a, use_container_width=True)

with col2:
    # Gráfico de líneas: cantidad de títulos nuevos con ISBN por año
    fig1b = px.line(df_f, x="anio", y="titulos_registrados_isbn", color="pais",
                    markers=True, title="Títulos ISBN registrados por año",
                    labels={"titulos_registrados_isbn": "Títulos", "anio": "Año", "pais": "País"},
                    color_discrete_map=COLORES_PAISES)
    fig1b = apply_dark_theme(fig1b)
    st.plotly_chart(fig1b, use_container_width=True)

# Área apilada: muestra la contribución de cada país al total regional
# Cada área se acumula sobre la anterior — se ve la participación proporcional
fig1c = px.area(df_f, x="anio", y="ejemplares_producidos_millones", color="pais",
                title="Participación regional acumulada — Ejemplares (área apilada)",
                labels={"ejemplares_producidos_millones": "Millones", "anio": "Año", "pais": "País"},
                color_discrete_map=COLORES_PAISES)
fig1c = apply_dark_theme(fig1c, height=380)
st.plotly_chart(fig1c, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — FACTURACIÓN Y ECONOMÍA DEL LIBRO
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.header("💰 Sección 2 · Facturación y Economía del Libro")
st.markdown(
    "<div class='insight-box'>💡 <strong>¿Qué muestra esta sección?</strong> "
    "El dinero que mueve la industria. El mapa de calor permite ver de un golpe "
    "en qué años y países fue mejor o peor el negocio editorial.</div>",
    unsafe_allow_html=True
)

col3, col4 = st.columns(2)

with col3:
    # Barras agrupadas: barmode="group" pone las barras de cada país una al lado de la otra
    fig2a = px.bar(df_f, x="anio", y="facturacion_estimada_millones_usd", color="pais",
                   barmode="group", title="Facturación estimada (USD millones)",
                   labels={"facturacion_estimada_millones_usd": "USD M", "anio": "Año", "pais": "País"},
                   color_discrete_map=COLORES_PAISES)
    fig2a = apply_dark_theme(fig2a)
    st.plotly_chart(fig2a, use_container_width=True)

with col4:
    # Líneas de per cápita con línea de referencia en y=1
    fig2b = px.line(df_f, x="anio", y="ejemplares_per_capita", color="pais",
                    markers=True, title="Ejemplares por habitante (per cápita)",
                    labels={"ejemplares_per_capita": "Ej./hab.", "anio": "Año", "pais": "País"},
                    color_discrete_map=COLORES_PAISES)
    # Línea horizontal de referencia — "1 libro por habitante" como benchmark
    fig2b.add_hline(y=1.0, line_dash="dot", line_color="rgba(255,255,255,0.25)",
                    annotation_text="1 ej./hab.", annotation_font_color="#888")
    fig2b = apply_dark_theme(fig2b)
    st.plotly_chart(fig2b, use_container_width=True)

# Mapa de calor (heatmap): reorganizamos los datos en una tabla país x año
# pivot_table convierte filas en columnas — ideal para el mapa de calor
pivot_fact = df_f.pivot_table(
    index="pais", columns="anio",
    values="facturacion_estimada_millones_usd", aggfunc="mean"
)
fig2c = px.imshow(
    pivot_fact,
    title="Mapa de calor — Facturación (USD M) · Dorado = mayor, oscuro = menor",
    labels=dict(color="USD M", x="Año", y="País"),
    color_continuous_scale=[[0.0, "#1a1d27"], [0.3, "#2d3a5c"],
                             [0.6, "#c17f24"], [1.0, "#f5c842"]],
    aspect="auto", text_auto=".0f"
)
fig2c.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(26,29,39,0.8)",
    font=dict(family="DM Sans", color="#c0c8d8"),
    title_font=dict(family="Playfair Display, serif", size=16, color="#f0f0f0"),
    height=320, margin=dict(t=50, b=30, l=100, r=20),
    coloraxis_colorbar=dict(tickfont=dict(color="#aaa"),
                            title=dict(text="USD M", font=dict(color="#aaa")))
)
fig2c.update_traces(textfont=dict(size=9, color="#fff"))
st.plotly_chart(fig2c, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — TIRADA Y DIGITALIZACIÓN
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.header("📐 Sección 3 · Tirada Promedio y Digitalización")
st.markdown(
    "<div class='insight-box'>💡 <strong>¿Qué muestra esta sección?</strong> "
    "Dos transformaciones estructurales: la caída de la tirada promedio (cuántos ejemplares "
    "se imprimen por título) y el avance del libro digital desde 2012.</div>",
    unsafe_allow_html=True
)

col5, col6 = st.columns(2)

with col5:
    # Tirada promedio: cuántos ejemplares se imprimen de cada título nuevo
    fig3a = px.line(df_f, x="anio", y="tirada_promedio_ejemplares", color="pais",
                    markers=True, title="Tirada promedio por título",
                    labels={"tirada_promedio_ejemplares": "Ej./título", "anio": "Año", "pais": "País"},
                    color_discrete_map=COLORES_PAISES)
    fig3a = apply_dark_theme(fig3a)
    st.plotly_chart(fig3a, use_container_width=True)

with col6:
    # Digitalización: solo disponible desde 2012, filtramos valores vacíos (NaN)
    df_dig = df_f[df_f["formato_digital_pct"].notna()].copy()
    if not df_dig.empty:
        fig3b = px.line(df_dig, x="anio", y="formato_digital_pct", color="pais",
                        markers=True, title="Adopción de formato digital (%)",
                        labels={"formato_digital_pct": "% Digital", "anio": "Año", "pais": "País"},
                        color_discrete_map=COLORES_PAISES)
        fig3b.add_hline(y=25, line_dash="dot", line_color="rgba(255,255,255,0.25)",
                        annotation_text="25% umbral madurez", annotation_font_color="#888")
        fig3b = apply_dark_theme(fig3b)
        st.plotly_chart(fig3b, use_container_width=True)
    else:
        st.info("Sin datos de digitalización en el período seleccionado (disponible desde 2012).")


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4 — COMPARATIVA ENTRE PAÍSES EN UN AÑO
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.header("🏆 Sección 4 · Comparativa entre Países")
st.markdown(
    "<div class='insight-box'>💡 <strong>¿Qué muestra esta sección?</strong> "
    "Un ranking de países en un año puntual. El gráfico de burbujas muestra 3 variables "
    "a la vez: facturación (eje X), per cápita (eje Y) y cantidad de títulos (tamaño de burbuja).</div>",
    unsafe_allow_html=True
)

# Selector de año independiente del filtro global del sidebar
anio_comp = st.select_slider(
    "📅 Elegí el año para la comparativa",
    options=sorted(df_f["anio"].unique()),
    value=min(2024, df_f["anio"].max())
)

# Filtramos solo ese año
df_anio = df_f[df_f["anio"] == anio_comp].copy()

col7, col8 = st.columns(2)

with col7:
    # Barras horizontales ordenadas de menor a mayor
    # orientation="h" hace las barras horizontales
    df_sorted = df_anio.sort_values("facturacion_estimada_millones_usd", ascending=True)
    fig4a = px.bar(df_sorted, x="facturacion_estimada_millones_usd", y="pais",
                   orientation="h", color="pais", color_discrete_map=COLORES_PAISES,
                   title=f"Ranking de facturación en {anio_comp}",
                   labels={"facturacion_estimada_millones_usd": "USD millones", "pais": "País"},
                   text="facturacion_estimada_millones_usd")
    fig4a.update_traces(texttemplate="USD %{text:.0f}M", textposition="outside",
                        textfont=dict(color="#ddd", size=11))
    fig4a.update_layout(showlegend=False)
    fig4a = apply_dark_theme(fig4a, height=380)
    st.plotly_chart(fig4a, use_container_width=True)

with col8:
    # Gráfico de burbujas (scatter): 3 variables simultáneas
    # Eje X = facturación, Eje Y = per cápita, Tamaño burbuja = títulos ISBN
    fig4b = px.scatter(df_anio, x="facturacion_estimada_millones_usd", y="ejemplares_per_capita",
                       size="titulos_registrados_isbn", color="pais",
                       color_discrete_map=COLORES_PAISES, text="pais",
                       title=f"Facturación vs. Per cápita — {anio_comp}",
                       labels={"facturacion_estimada_millones_usd": "Facturación (USD M)",
                                "ejemplares_per_capita": "Ej./habitante"},
                       size_max=60)
    fig4b.update_traces(textposition="top center", textfont=dict(color="#ddd", size=11))
    fig4b.update_layout(showlegend=False)
    fig4b = apply_dark_theme(fig4b, height=380)
    st.plotly_chart(fig4b, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 5 — IMPACTO DE CRISIS Y EVENTOS HISTÓRICOS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.header("🔴 Sección 5 · Impacto de Crisis y Eventos")
st.markdown(
    "<div class='insight-box'>💡 <strong>¿Qué muestra esta sección?</strong> "
    "Cómo los grandes eventos históricos (crisis, pandemias, estallidos) impactaron "
    "en la producción de libros. Las líneas punteadas rojas marcan los momentos de ruptura.</div>",
    unsafe_allow_html=True
)

# Selector de país para esta sección
pais_crisis = st.selectbox("🌎 Elegí un país", options=paises_sel, index=0)

df_pais   = df_f[df_f["pais"] == pais_crisis].copy()
df_crisis = df_pais[df_pais["contexto"].notna() & (df_pais["contexto"].str.strip() != "")]

# go.Figure() crea un gráfico vacío al que le agregamos trazas una por una
# Esto es más flexible que px.line cuando necesitamos dos ejes Y distintos
fig5 = go.Figure()

# Traza principal: área rellena bajo la línea de ejemplares
fig5.add_trace(go.Scatter(
    x=df_pais["anio"], y=df_pais["ejemplares_producidos_millones"],
    mode="lines+markers", name="Ejemplares producidos",
    line=dict(color=COLORES_PAISES.get(pais_crisis, "#f5c842"), width=3),
    marker=dict(size=7), fill="tozeroy", fillcolor="rgba(245,200,66,0.08)"
))

# Segunda traza: facturación en el eje Y derecho (yaxis="y2")
fig5.add_trace(go.Scatter(
    x=df_pais["anio"], y=df_pais["facturacion_estimada_millones_usd"],
    mode="lines", name="Facturación (USD M)",
    line=dict(color="#ff6b6b", width=2, dash="dash"), yaxis="y2"
))

# Agregamos líneas verticales y anotaciones en los años de crisis
for _, row in df_crisis.iterrows():
    fig5.add_vline(x=row["anio"], line_dash="dot",
                   line_color="rgba(255,107,107,0.5)", line_width=1.5)
    fig5.add_annotation(
        x=row["anio"],
        y=df_pais["ejemplares_producidos_millones"].max() * 0.95,
        text=f"⚡ {row['contexto']}", showarrow=False,
        textangle=-90, font=dict(size=9, color="#ff6b6b"), xanchor="right"
    )

fig5.update_layout(
    title=f"{pais_crisis} · Producción y facturación con eventos históricos",
    yaxis=dict(title="Millones de ejemplares"),
    yaxis2=dict(title="Facturación (USD M)", overlaying="y", side="right", showgrid=False),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(26,29,39,0.8)",
    font=dict(family="DM Sans", color="#c0c8d8"),
    title_font=dict(family="Playfair Display, serif", size=16, color="#f0f0f0"),
    hovermode="x unified", height=440,
    margin=dict(t=50, b=80, l=60, r=80),
    legend=dict(bgcolor="rgba(26,29,39,0.9)", bordercolor="rgba(245,200,66,0.2)",
                borderwidth=1, orientation="h", y=-0.2, x=0.5, xanchor="center")
)
st.plotly_chart(fig5, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 6 — TABLA DE DATOS Y DESCARGA
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.header("🗂 Sección 6 · Datos y Descarga")
st.markdown(
    "<div class='insight-box'>💡 Explorá los datos crudos y descargá el CSV "
    "filtrado según los países y años que seleccionaste en el panel lateral.</div>",
    unsafe_allow_html=True
)

# Multiselect para que el usuario elija qué columnas ver en la tabla
columnas_disponibles = [
    "pais", "anio", "titulos_registrados_isbn", "ejemplares_producidos_millones",
    "facturacion_estimada_millones_usd", "tirada_promedio_ejemplares",
    "variacion_anual_pct", "formato_digital_pct", "ejemplares_per_capita",
    "contexto", "fuente_principal", "notas"
]
cols_mostrar = st.multiselect(
    "📊 Columnas a mostrar",
    options=columnas_disponibles,
    default=columnas_disponibles[:8]
)

if cols_mostrar:
    # st.dataframe muestra una tabla interactiva — se puede ordenar por columna
    st.dataframe(
        df_f[cols_mostrar].sort_values(["pais", "anio"]),
        use_container_width=True, height=420, hide_index=True
    )

# Botón de descarga: convierte el DataFrame a CSV y lo ofrece para descargar
st.download_button(
    label="⬇️ Descargar CSV filtrado",
    data=df_f.to_csv(index=False).encode("utf-8"),
    file_name=f"latam_libros_{anio_min}_{anio_max}.csv",
    mime="text/csv",
    help="Descarga los datos con los filtros actuales aplicados"
)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#444; font-size:0.78rem; padding:1rem 0;'>"
    "📚 <strong style='color:#555'>Mercado Editorial LATAM Dashboard</strong> · "
    "Fuentes: CAL · CANIEM · CCL · CCdL · CERLALC · BNP · BNB · BCE<br>"
    "⚠️ Los datos de 2025 son estimaciones. Uso educativo."
    "</div>", unsafe_allow_html=True
)
