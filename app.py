import os
import streamlit as st
import base64
from openai import OpenAI


# Function to encode the image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")


st.set_page_config(
    page_title="Cuarto Oscuro",
    page_icon="📷",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# ESTILOS (TEMÁTICA: CUARTO OSCURO FOTOGRÁFICO)
# ============================================================

st.markdown("""
<style>

    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

    :root {
        --fondo: #120A0A;
        --fondo-claro: #221414;
        --rojo: #E63946;
        --rojo-oscuro: #8C1C26;
        --crema: #F5EBDD;
        --gris: #B8A99A;
    }

    /* Fondo: oscuridad con luz roja de revelado */
    .stApp {
        background:
            radial-gradient(circle at 50% 0%, rgba(230, 57, 70, 0.22) 0%, transparent 50%),
            radial-gradient(circle at 90% 100%, rgba(140, 28, 38, 0.25) 0%, transparent 45%),
            var(--fondo);
        font-family: 'Space Mono', monospace;
    }

    /* Texto general */
    .stMarkdown p, .stMarkdown li, label, .stCaption, span {
        color: var(--crema);
        font-family: 'Space Mono', monospace;
    }

    /* Título */
    h1 {
        font-family: 'Special Elite', cursive !important;
        color: var(--rojo) !important;
        text-align: center;
        font-size: 42px !important;
        letter-spacing: 2px;
        text-shadow: 0 0 14px rgba(230, 57, 70, 0.7);
    }

    h2, h3 {
        font-family: 'Special Elite', cursive !important;
        color: var(--crema) !important;
    }

    /* Campo de la clave */
    .stTextInput input {
        background-color: var(--fondo-claro) !important;
        border: 2px solid var(--rojo-oscuro) !important;
        border-radius: 8px !important;
        color: var(--crema) !important;
        font-family: 'Space Mono', monospace !important;
    }

    .stTextInput input:focus {
        border-color: var(--rojo) !important;
        box-shadow: 0 0 12px rgba(230, 57, 70, 0.6) !important;
    }

    /* Cargador de imagen: bandeja de revelado */
    [data-testid="stFileUploader"] {
        background-color: var(--fondo-claro);
        border: 2px dashed var(--rojo);
        border-radius: 14px;
        padding: 15px;
        box-shadow: 0 0 18px rgba(230, 57, 70, 0.25);
    }

    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p {
        color: var(--gris) !important;
    }

    /* Imagen: marco de foto instantánea */
    [data-testid="stImage"] img {
        border: 14px solid var(--crema);
        border-bottom: 48px solid var(--crema);
        border-radius: 4px;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.7);
    }

    [data-testid="stImageCaption"] {
        color: var(--gris) !important;
        font-style: italic;
    }

    /* Expander */
    [data-testid="stExpander"] {
        background: var(--fondo-claro);
        border: 1px solid var(--rojo-oscuro);
        border-radius: 12px;
    }

    /* Caja de texto adicional */
    textarea {
        background-color: var(--fondo-claro) !important;
        border: 2px solid var(--rojo-oscuro) !important;
        border-radius: 10px !important;
        color: var(--crema) !important;
        font-family: 'Space Mono', monospace !important;
    }

    textarea:focus {
        border-color: var(--rojo) !important;
        box-shadow: 0 0 12px rgba(230, 57, 70, 0.6) !important;
    }

    /* Botón: obturador */
    .stButton > button {
        background: linear-gradient(135deg, var(--rojo-oscuro), var(--rojo));
        color: var(--crema);
        font-family: 'Special Elite', cursive;
        font-size: 18px;
        border: 2px solid var(--crema);
        border-radius: 50px;
        padding: 10px 30px;
        box-shadow: 0 0 16px rgba(230, 57, 70, 0.6);
        transition: 0.2s;
    }

    .stButton > button:hover {
        background: var(--crema);
        color: var(--rojo-oscuro);
        box-shadow: 0 0 26px rgba(245, 235, 221, 0.7);
    }

    /* Caja de resultado */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--rojo-oscuro) !important;
        background: rgba(34, 20, 20, 0.7);
        border-radius: 14px;
    }

    /* Alertas */
    [data-testid="stAlert"] {
        background: var(--fondo-claro);
        border: 1px solid var(--rojo-oscuro);
        border-radius: 12px;
    }

    hr { border-color: var(--rojo-oscuro) !important; }

    /* Decoración */
    .subtitulo {
        text-align: center;
        color: var(--gris);
        font-style: italic;
        font-size: 15px;
        margin-bottom: 4px;
    }

    .tira {
        text-align: center;
        color: var(--rojo);
        font-size: 20px;
        letter-spacing: 10px;
        margin: 6px 0 20px 0;
        text-shadow: 0 0 10px rgba(230, 57, 70, 0.7);
    }

    .pie {
        text-align: center;
        color: var(--gris);
        font-size: 12px;
        font-style: italic;
        margin-top: 30px;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# TÍTULO
# ============================================================

st.title("📷 Cuarto Oscuro")
st.markdown(
    "<p class='subtitulo'>La IA revela lo que hay en tu imagen</p>"
    "<div class='tira'>▪ ▫ ▪ ▫ ▪ ▫ ▪</div>",
    unsafe_allow_html=True
)

# ============================================================
# CLAVE
# ============================================================

ke = st.text_input('🔑 Ingresa tu Clave', type="password")

api_key = ke.strip()

if api_key:
    os.environ['OPENAI_API_KEY'] = api_key
    client = OpenAI(api_key=api_key)
else:
    client = None

# ============================================================
# CARGAR IMAGEN
# ============================================================

uploaded_file = st.file_uploader(
    "🎞️ Sube tu negativo (imagen)",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file:
    with st.expander("🖼️ Tu fotografía", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# ============================================================
# PREGUNTA ESPECÍFICA
# ============================================================

show_details = st.toggle("🔍 Pregunta algo específico sobre la imagen", value=False)

additional_details = ""

if show_details:
    additional_details = st.text_area(
        "Adiciona contexto de la imagen aquí:"
    )

# ============================================================
# BOTÓN
# ============================================================

analyze_button = st.button("📸 Revelar imagen", type="secondary")

# ============================================================
# ANÁLISIS
# ============================================================

if analyze_button:

    if not api_key:
        st.warning("🔑 Por favor ingresa tu API key.")

    elif uploaded_file is None:
        st.warning("📂 Por favor sube una imagen.")

    else:
        with st.spinner("🔴 Revelando en el cuarto oscuro..."):
            base64_image = encode_image(uploaded_file)

            prompt_text = "Describe what you see in the image in spanish"

            if show_details and additional_details:
                prompt_text += (
                    f"\n\nAdditional Context Provided by the User:\n{additional_details}"
                )

            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                    ],
                }
            ]

            try:
                st.markdown("### 🖨️ Resultado del revelado")

                with st.container(border=True):
                    full_response = ""
                    message_placeholder = st.empty()
                    for completion in client.chat.completions.create(
                        model="gpt-4o", messages=messages,
                        max_tokens=1200, stream=True
                    ):
                        if completion.choices and completion.choices[0].delta.content is not None:
                            full_response += completion.choices[0].delta.content
                            message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)

            except Exception as e:
                st.error(f"❌ Ocurrió un error: {e}")

# ============================================================
# PIE DE PÁGINA
# ============================================================

st.markdown(
    "<div class='tira'>▪ ▫ ▪ ▫ ▪ ▫ ▪</div>"
    "<p class='pie'>Cuarto Oscuro · cada imagen guarda una historia</p>",
    unsafe_allow_html=True
)
