import streamlit as st
import os
import base64
from datetime import datetime
import re

# Archivo donde se guarda el feedback de los usuarios
FEEDBACK_FILE = "feedback.txt"
def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        califs = []
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "Calificación" in line:
                    match = re.search(r'Calificación (\d+)/5', line)
                    if match:
                        califs.append(int(match.group(1)))
        if califs:
            promedio = sum(califs) / len(califs)
            return f"He mejorado gracias a feedback anterior. Promedio: {promedio:.1f}/5"
    return "¡Soy nuevo! Ayúdame a mejorar con tu feedback."


def save_feedback(calificacion, comentario=""):
    with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()}: Calificación {calificacion}/5 | {comentario}\n")
def get_iniciales(nombre):
    if not nombre:
        return "T.N."
    partes = nombre.strip().split()
    if len(partes) >= 2:
        return f"{partes[0][0].upper()}.{partes[-1][0].upper()}."
    return nombre[0].upper() + "."
def generar_cv_modelo(perfil, foto_data=None):
    iniciales = get_iniciales(perfil.get('nombre', 'Tu Nombre'))

    foto_html = ""
    if foto_data:
        b64 = base64.b64encode(foto_data.read()).decode()
        foto_html = f'<img src="data:image/jpeg;base64,{b64}" style="width:120px; height:120px; border-radius:50%; border: 4px solid white; margin-bottom: 20px;">'

    telefono_html = f'<p><i class="fas fa-phone"></i> {perfil.get("telefono", "")}</p>' if perfil.get('telefono') else ''
    email_html = f'<p><i class="fas fa-envelope"></i> {perfil.get("email", "")}</p>' if perfil.get('email') else ''
    ubicacion_html = f'<p><i class="fas fa-map-marker-alt"></i> {perfil.get("ubicacion", "")}</p>' if perfil.get('ubicacion') else ''
    linkedin_html = f'<p><i class="fab fa-linkedin"></i> {perfil.get("linkedin", "")}</p>' if perfil.get('linkedin') else ''

    idiomas = perfil.get('idiomas', 'No especificados')
    referencias = perfil.get('referencias', 'Disponibles a pedido')
    perfil_profesional = perfil.get('perfil_profesional', 'Estudiante motivada en constante aprendizaje, buscando oportunidades en Paraguay para contribuir con compromiso y responsabilidad.')
    educacion = perfil.get('educacion', perfil.get('estudios', 'No especificado'))
    habilidades_tecnicas = perfil.get('habilidades_tecnicas', perfil.get('habilidades', 'No especificadas'))
    habilidades_blandas = perfil.get('habilidades_blandas', 'No especificadas')
    proyectos = perfil.get('proyectos', 'No especificados')

    css = """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .cv-container { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); overflow: hidden; }
        .header { background: linear-gradient(to right, #1e3a8a, #3b82f6); color: white; padding: 30px; text-align: center; }
        .header h1 { margin: 0; font-size: 2.2em; }
        .header h2 { margin: 5px 0 0; font-size: 1.4em; opacity: 0.9; }
        .content { display: flex; }
        .left-column { width: 35%; background: #1e40af; color: white; padding: 30px; }
        .circle { width: 120px; height: 120px; background: white; color: #1e40af; border-radius: 50%; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center; font-size: 2.5em; font-weight: bold; border: 4px solid #3b82f6; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        .right-column { width: 65%; padding: 30px; background: #f8fafc; }
        .section-title { color: #1e40af; font-size: 1.4em; border-bottom: 2px solid #1e40af; padding-bottom: 8px; margin-bottom: 15px; }
    </style>
    """

    html = f"""
    {css}
    <div class="cv-container">
        <div class="header">
            <h1>CURRICULUM VITAE</h1>
            <h2>{perfil.get('nombre', 'Tu Nombre Completo')}</h2>
        </div>
        
        <div class="content">
            <div class="left-column">
                <div class="circle">{iniciales}</div>
                
                <h3 class="section-title">DATOS DE CONTACTO</h3>
                {telefono_html}
                {email_html}
                {ubicacion_html}
                {linkedin_html}
                
                <h3 class="section-title">IDIOMAS</h3>
                <p>{idiomas}</p>
                
                <h3 class="section-title">REFERENCIAS</h3>
                <p>{referencias}</p>
            </div>
            
            <div class="right-column">
                <h3 class="section-title">PERFIL PROFESIONAL</h3>
                <p>{perfil_profesional}</p>
                
                <h3 class="section-title">EDUCACIÓN</h3>
                <p>{educacion}</p>
                
                <h3 class="section-title">HABILIDADES TÉCNICAS</h3>
                <p>{habilidades_tecnicas}</p>
                
                <h3 class="section-title">HABILIDADES BLANDAS</h3>
                <p>{habilidades_blandas}</p>
                
                <h3 class="section-title">PROYECTOS DESTACADOS</h3>
                <p>{proyectos}</p>
            </div>
        </div>
        
        <div style="text-align: center; padding: 15px; background: #1e40af; color: white; font-size: 0.9em;">
            Generado por JobEvo PY - Tu asistente que evoluciona contigo
        </div>
    </div>
    """

    return html
def entrenamiento_entrevista(empresa, puesto):
    st.subheader(f"Entrenamiento de Entrevista para {empresa} - Puesto: {puesto}")
    
    preguntas = []
    if "itaipu" in empresa.lower() or "energía" in empresa.lower():
        preguntas = [
            "¿Por qué querés trabajar en Itaipú?",
            "¿Qué sabés sobre energía renovable en Paraguay?",
            "¿Cómo manejás proyectos en equipo?",
            "¿Cuáles son tus debilidades en un entorno técnico?"
        ]
    elif "banco" in empresa.lower() or "bbva" in empresa.lower() or "itau" in empresa.lower():
        preguntas = [
            "¿Por qué querés trabajar en un banco?",
            "¿Qué sabés sobre finanzas personales?",
            "¿Cómo manejás clientes difíciles?",
            "¿Cuáles son tus debilidades en ventas?"
        ]
    elif "call center" in empresa.lower() or "teleperformance" in empresa.lower():
        preguntas = [
            "¿Por qué querés trabajar en un call center?",
            "¿Cómo manejás llamadas de clientes enojados?",
            "¿Qué sabés sobre servicio al cliente?",
            "¿Cuáles son tus debilidades en comunicación?"
        ]
    else:
        preguntas = [
            "¿Por qué querés trabajar acá?",
            "¿Cuáles son tus debilidades?",
            "¿Qué sabés sobre nuestra empresa?",
            "¿Cómo manejás el estrés?"
        ]

    # Personalización extra según puesto
    if "ingeniero" in puesto.lower():
        preguntas.append("¿Qué experiencia tenés con software técnico?")
    elif "vendedor" in puesto.lower():
        preguntas.append("¿Cómo cerrás una venta?")
    elif "administrativo" in puesto.lower():
        preguntas.append("¿Cómo organizás tu tiempo?")

    if 'entrevista_index' not in st.session_state:
        st.session_state.entrevista_index = 0
        st.session_state.respuestas_ent = {}
        st.session_state.feedback_ent = []

    index = st.session_state.entrevista_index
    if index < len(preguntas):
        pregunta = preguntas[index]
        st.markdown(f"**Pregunta {index+1}/{len(preguntas)}:** {pregunta}")
        respuesta = st.text_area("Tu respuesta:", value=st.session_state.respuestas_ent.get(index, ""), height=120, key=f"resp_ent_{index}")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Obtener Feedback"):
                fb = ""
                if "por qué" in pregunta.lower():
                    if len(respuesta) < 50:
                        fb = "Respuesta corta. Consejo: Explica con pasión por qué {puesto} en {empresa} te motiva."
                    elif "motiv" in respuesta.lower() or "pasión" in respuesta.lower():
                        fb = "¡Excelente! Mencionaste motivación. Para mejorar: agrega cómo tus habilidades encajan en {empresa}."
                    else:
                        fb = "Mejora: Incluye motivación personal y cómo {puesto} en {empresa} alinea con tus metas."
                elif "debilidades" in pregunta.lower():
                    if "mejorando" in respuesta.lower():
                        fb = "Muy bien, mostraste autocrítica + acción. Consejo: elige debilidades no críticas para {puesto}."
                    else:
                        fb = "Mejora: Siempre menciona cómo estás trabajando en esa debilidad."
                elif "sabés sobre" in pregunta.lower():
                    if empresa.lower() in respuesta.lower():
                        fb = "Buen conocimiento de {empresa}. Consejo: agrega un dato específico (ej: impacto en Paraguay)."
                    else:
                        fb = "Mejora: Investiga {empresa} antes. Menciona algo concreto."
                st.info(fb)
                st.session_state.feedback_ent.append(fb)
        with col2:
            if st.button("Siguiente Pregunta"):
                st.session_state.respuestas_ent[index] = respuesta
                st.session_state.entrevista_index += 1
                st.experimental_rerun()
        with col3:
            if st.button("Repetir esta pregunta"):
                st.experimental_rerun()
    else:
        st.success("¡Entrenamiento completado!")
        st.write("Resumen de consejos:")
        for fb in st.session_state.feedback_ent:
            st.write(fb)
        if st.button("Reiniciar"):
            st.session_state.entrevista_index = 0
            st.session_state.respuestas_ent = {}
            st.session_state.feedback_ent = []
            st.experimental_rerun()
# Estilo general
st.markdown("""
<style>
    .main { background-color: #f0f8ff; padding: 20px; }
    h1, h2 { color: #1e40af; }
    .stButton > button { background-color: #1e40af; color: white; border: none; border-radius: 8px; padding: 10px 20px; }
    .stDownloadButton > button { background-color: #22c55e; color: white; border: none; }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.title("JobEvo PY - Tu Asistente de Empleo que Evoluciona Contigo")

feedback_anterior = load_feedback()
if feedback_anterior:
    st.info(feedback_anterior)

# Formulario de perfil
st.subheader("Cuéntame sobre ti")
nombre = st.text_input("Nombre Completo (ej: Lenys Rosalia Sánchez Cáceres)")
edad = st.text_input("Edad (ej: 22)")
estudios = st.text_input("Estudios (ej: Ingeniería en Informática en curso)")
experiencia = st.text_input("Experiencia (ej: Ninguna, o pasantía en X)")
habilidades_tecnicas = st.text_input("Habilidades Técnicas (ej: Python, prompts IA)")
habilidades_blandas = st.text_input("Habilidades Blandas (ej: Adaptabilidad, trabajo en equipo)")
proyectos = st.text_area("Proyectos Destacados (ej: Automatización con IA)")
telefono = st.text_input("Teléfono (ej: +595 981 123 456)")
email = st.text_input("Email (ej: lenys@email.com)")
ubicacion = st.text_input("Ubicación (ej: Asunción)")
linkedin = st.text_input("LinkedIn (ej: linkedin.com/lenys)")
idiomas = st.text_input("Idiomas (ej: Español nativo, guaraní básico, inglés intermedio)")
referencias = st.text_input("Referencias (ej: Disponibles a pedido)")
perfil_profesional = st.text_area("Perfil Profesional (resumen corto)")
empresa = st.text_input("¿En qué empresa o tipo de empresa querés trabajar? (ej: Itaipú, banco, call center)")
puesto = st.text_input("¿Qué puesto buscas? (ej: ingeniero, vendedor, administrativo)")

foto_subida = st.file_uploader("Sube tu foto (opcional - tipo carnet)", type=["jpg", "png", "jpeg"])

perfil = {
    'nombre': nombre,
    'edad': edad,
    'estudios': estudios,
    'experiencia': experiencia,
    'habilidades_tecnicas': habilidades_tecnicas,
    'habilidades_blandas': habilidades_blandas,
    'proyectos': proyectos,
    'telefono': telefono,
    'email': email,
    'ubicacion': ubicacion,
    'linkedin': linkedin,
    'idiomas': idiomas,
    'referencias': referencias,
    'perfil_profesional': perfil_profesional,
    'empresa': empresa
}

if st.button("Generar CV Profesional"):
    if nombre and edad and estudios and empresa:
        cv_html = generar_cv_modelo(perfil, foto_subida)
        st.markdown(cv_html, unsafe_allow_html=True)
        
        st.download_button(
            label="Descargar CV como HTML",
            data=cv_html,
            file_name="mi_cv_profesional.html",
            mime="text/html"
        )
    else:
        st.warning("Completa al menos nombre, edad, estudios y empresa.")

# Entrenamiento
if empresa and puesto:
    if st.button("Entrenar Entrevista Personalizada"):
        entrenamiento_entrevista(empresa, puesto)

# Feedback
st.subheader("¿Te ayudó?")
calif = st.slider("Califica 1-5", 1, 5, 3)
coment = st.text_input("Comentario (opcional)")
if st.button("Enviar Feedback"):
    save_feedback(calif, coment)
    st.success("¡Gracias! JobEvo ha aprendido de ti.")

st.caption("JobEvo PY v0.9 - Tu asistente que evoluciona contigo.")

                   

       
