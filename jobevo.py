import streamlit as st
import os
import datetime
import io
from weasyprint import HTML
import base64

# ────────────────────────────────────────────────
# Archivos de persistencia
# ────────────────────────────────────────────────
FEEDBACK_FILE = "feedback.txt"
MEJORAS_FILE  = "mejoras.txt"

# ────────────────────────────────────────────────
# Funciones de feedback y mejoras
# ────────────────────────────────────────────────
def guardar_feedback(calif):
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
        f.write(f"{ahora} | {calif}/5\n")

def leer_promedio_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return 0, 0
    califs = []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if '|' in line and '/' in line:
                try:
                    cal = int(line.split('/')[0].split('|')[-1].strip())
                    califs.append(cal)
                except:
                    pass
    if not califs:
        return 0, 0
    promedio = sum(califs) / len(califs)
    return round(promedio, 1), len(califs)

def leer_feedback():
    promedio, total = leer_promedio_feedback()
    if total == 0:
        return "¡Tu opinión me ayuda a mejorar!"
    return f"Promedio: {promedio}/5 ({total} calificaciones) — Gracias por ayudarme a mejorar ⭐"

def registrar_mejora(motivo, cambio):
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(MEJORAS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{ahora} | Motivo: {motivo} | Cambio: {cambio}\n")

def leer_ultimas_mejoras(n=3):
    if not os.path.exists(MEJORAS_FILE):
        return "Aún no se han registrado mejoras automáticas."
    with open(MEJORAS_FILE, "r", encoding="utf-8") as f:
        lineas = f.readlines()[-n:]
    if not lineas:
        return "Aún no hay mejoras recientes."
    return "\n".join([f"- {l.strip()}" for l in lineas])

# ─── Fin Parte 1/6 ───
# Pega la Parte 2 justo después
# ────────────────────────────────────────────────
# Generar Perfil Profesional automáticamente (optimizado para 1 página)
# ────────────────────────────────────────────────
@st.cache_data
def generar_perfil_automatico(datos):
    edad = datos['edad']
    educ = datos['educacion'] or datos['titulo_universitario'] or "estudiante/joven profesional"
    puesto = datos['puesto_aspirado']
    empresa = datos['empresa_objetivo']
    habilidades_tec = ", ".join(datos['habilidades_tecnicas'][:4]) if datos['habilidades_tecnicas'] else "resolución de problemas, aprendizaje rápido y trabajo en equipo"  # reducido para caber
    certs = ", ".join(datos['certificaciones'][:2]) if datos['certificaciones'] else ""
    proyectos = datos['proyectos'][:150] + "..." if len(datos['proyectos']) > 150 else datos['proyectos']

    genero = datos['genero']
    if genero == "Femenino":
        motiv = "motivada"
        joven = "joven profesional"
        aportando = "aportando mi compromiso"
    elif genero == "Masculino":
        motiv = "motivado"
        joven = "joven profesional"
        aportando = "aportando mi compromiso"
    else:
        motiv = "motivad@"
        joven = "persona joven y profesional"
        aportando = "aportando compromiso"

    perfil = f"{joven.capitalize()} de {edad} años con formación en {educ}, muy {motiv} y enfocada en el crecimiento continuo.<br>"

    if puesto:
        perfil += f"Aspiro al puesto de {puesto} "
    if empresa:
        perfil += f"en {empresa}. "
    else:
        perfil += "en una organización líder de Paraguay. "

    perfil += f"Aporto mis habilidades en {habilidades_tec}. "

    if certs:
        perfil += f"Cuento con certificaciones como {certs}. "

    if proyectos:
        perfil += f"He desarrollado proyectos como {proyectos}. "

    perfil += f"{aportando.capitalize()}, responsabilidad y ganas de aprender, busco integrarme a un equipo dinámico para contribuir al éxito de la organización."

    return perfil

# ────────────────────────────────────────────────
# Consejos personalizados
# ────────────────────────────────────────────────
@st.cache_data
def dar_consejos_personalizados(puesto='', empresa=''):
    lineas = [
        "- Usa una foto profesional y actualizada en LinkedIn",
        "- Crea un titular atractivo con palabras clave del puesto (ej: IA, Python, automatización)"
    ]

    if empresa:
        lineas.append(f"- Postulate directamente en la página oficial de {empresa} o en sus redes sociales")
    else:
        lineas.append("- Postulate en Computrabajo, LinkedIn, Bumeran y portales de empleo paraguayos")

    if puesto:
        lineas.append(f"- Destaca habilidades, certificaciones y proyectos relacionados con {puesto.lower()}")
    else:
        lineas.append("- Destaca certificaciones, proyectos y habilidades técnicas — son muy valorados")

    if empresa and puesto:
        lineas.append(f"- Investiga la misión, proyectos y cultura de {empresa} para adaptar tu CV y entrevista al puesto de {puesto}")

    lineas += [
        "- Adjunta tu CV en PDF y una carta de presentación corta si la empresa lo solicita",
        "- Practica entrevistas con preguntas comunes del sector y del puesto al que aspiras"
    ]

    return lineas

# ─── Fin Parte 2/6 ───
# Pega la Parte 3 justo después
# ────────────────────────────────────────────────
# Generar HTML del CV (optimizado para caber en 1 página A4)
# ────────────────────────────────────────────────
def generar_html_cv(datos, foto_base64=None):
    nombre_upper = datos['nombre'].upper()
    foto_html = f'<img src="data:image/png;base64,{foto_base64}" alt="Foto">' if foto_base64 else datos['iniciales']

    contact_lines = []
    if datos['telefono']:    contact_lines.append(f"<p>📞 {datos['telefono']}</p>")
    if datos['email']:       contact_lines.append(f"<p>📧 {datos['email']}</p>")
    if datos['linkedin']:    contact_lines.append(f"<p>🔗 {datos['linkedin']}</p>")
    if datos['ubicacion']:   contact_lines.append(f"<p>📍 {datos['ubicacion']}, Paraguay</p>")
    contact_section = '<h2>DATOS DE CONTACTO</h2><div class="contact">' + ''.join(contact_lines) + '</div>' if contact_lines else ''

    idiomas_lines = []
    idiomas_lines.append('<p><strong>Español</strong> <span style="float:right;">Nativo</span></p>')
    idiomas_lines.append('<div class="bar"><div style="width:100%"></div></div>')
    
    if datos['idiomas']['guarani'] != "Ninguno":
        w = '90' if 'Nativo' in datos['idiomas']['guarani'] else '60' if 'Intermedio' in datos['idiomas']['guarani'] else '30'
        idiomas_lines.append(f'<p><strong>Guaraní</strong> <span style="float:right;">{datos["idiomas"]["guarani"]}</span></p>')
        idiomas_lines.append(f'<div class="bar"><div style="width:{w}%"></div></div>')
    
    if datos['idiomas']['ingles'] != "Ninguno":
        w = '80' if 'Avanzado' in datos['idiomas']['ingles'] else '50' if 'Intermedio' in datos['idiomas']['ingles'] else '25'
        idiomas_lines.append(f'<p><strong>Inglés</strong> <span style="float:right;">{datos["idiomas"]["ingles"]}</span></p>')
        idiomas_lines.append(f'<div class="bar"><div style="width:{w}%"></div></div>')
    
    idiomas_section = '<h2>IDIOMAS</h2><div class="languages">' + ''.join(idiomas_lines) + '</div>' if idiomas_lines else ''

    tec_section = ''
    if datos['habilidades_tecnicas']:
        items = ''.join(f'<li>{h}</li>' for h in datos['habilidades_tecnicas'][:4])  # reducido para caber
        tec_section = f'<h2>HABILIDADES TÉCNICAS</h2><ul>{items}</ul>'

    bland_section = ''
    if datos['habilidades_blandas']:
        items = ''.join(f'<li>{h}</li>' for h in datos['habilidades_blandas'][:4])
        bland_section = f'<h2>HABILIDADES BLANDAS</h2><ul>{items}</ul>'

    cert_section = ''
    if datos['certificaciones']:
        items = ''.join(f'<li>{h}</li>' for h in datos['certificaciones'][:3])
        cert_section = f'<h2>CERTIFICACIONES</h2><ul>{items}</ul>'

    perfil_text = generar_perfil_automatico(datos)
    perfil_section = f'<h2>PERFIL PROFESIONAL</h2><p style="white-space: pre-wrap; word-wrap: break-word; line-height: 1.5; font-size: 10.5pt;">{perfil_text}</p>'

    educ_section = ''
    if datos['educacion'] or datos['titulo_universitario']:
        educ_section = '<h2>EDUCACIÓN</h2>'
        if datos['educacion']:
            promo = datos.get('edad', 22) + 18 - 3
            educ_section += f'<p style="font-size: 10.5pt;"><strong>{datos["educacion"]}</strong></p><p style="font-size: 10pt;">Promoción aprox: {promo} | Asunción, Paraguay</p>'
        if datos['titulo_universitario']:
            educ_section += f'<p style="font-size: 10.5pt;"><strong>{datos["titulo_universitario"]}</strong></p>'

    proyectos_section = f'<h2>PROYECTOS DESTACADOS</h2><p style="white-space: pre-wrap; word-wrap: break-word; font-size: 10.5pt;">{datos["proyectos"]}</p>' if datos['proyectos'] else ''

    ref_section = ''
    if datos['referencias']:
        items = ''.join(f'<li style="font-size: 10pt;">{h}</li>' for h in datos['referencias'])
        ref_section = f'<h2>REFERENCIAS</h2><ul>{items}</ul>'

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>CV - {datos['nombre']}</title>
        <style>
            @page {{ size: A4; margin: 10mm 8mm; }}
            * {{ box-sizing: border-box; }}
            body {{ font-family: Arial, Helvetica, sans-serif; margin: 0; padding: 0; background: #ffffff; color: #333; font-size: 10.5pt; line-height: 1.5; word-wrap: break-word; }}
            .container {{ width: 100%; margin: 0; height: 100%; display: flex; flex-direction: column; }}
            .header {{ background: #0a2540; color: white; padding: 25px 35px 20px 35px; text-align: center; position: relative; }}
            .header h1 {{ margin: 0 0 3px 0; font-size: 20pt; letter-spacing: 1px; }}
            .header h2 {{ margin: 0; font-size: 14pt; font-weight: normal; }}
            .profile-photo {{ position: absolute; top: 15px; left: 35px; width: 80px; height: 80px; border-radius: 50%; overflow: hidden; background: #5da9e9; display: flex; align-items: center; justify-content: center; font-size: 28pt; font-weight: bold; color: white; border: 3px solid #fff; }}
            .profile-photo img {{ width: 100%; height: 100%; object-fit: cover; }}
            .content {{ display: flex; flex: 1; padding: 20px 35px 30px 35px; gap: 20px; page-break-inside: avoid; }}
            .left-column {{ width: 35%; padding-right: 20px; border-right: 1px solid #d8d8d8; }}
            .right-column {{ width: 65%; padding-left: 20px; }}
            h2 {{ color: #0a2540; font-size: 12pt; margin: 15px 0 6px; padding-bottom: 3px; border-bottom: 1px solid #5da9e9; }}
            ul {{ margin: 6px 0 10px 18px; padding-left: 0; list-style: none; }}
            ul li {{ margin: 5px 0; position: relative; padding-left: 18px; word-break: break-word; }}
            ul li::before {{ content: "•"; position: absolute; left: 0; color: #5da9e9; font-size: 13pt; }}
            .contact p, .languages p {{ margin: 6px 0; font-size: 10pt; }}
            .languages p {{ margin-bottom: 2px; }}
            .bar {{ background: #e0e0e0; height: 6px; margin: 0 0 8px 0; border-radius: 3px; }}
            .bar div {{ height: 100%; background: #5da9e9; border-radius: 3px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="profile-photo">{foto_html}</div>
                <h1>CURRICULUM VITAE</h1>
                <h2>{nombre_upper}</h2>
            </div>
            <div class="content">
                <div class="left-column">
                    {contact_section}
                    {idiomas_section}
                    {tec_section}
                    {bland_section}
                    {cert_section}
                    {ref_section}
                </div>
                <div class="right-column">
                    {perfil_section}
                    {educ_section}
                    {proyectos_section}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

# ─── Fin Parte 3/6 ───
# Pega la Parte 4 justo después
# ────────────────────────────────────────────────
# Generar PDF
# ────────────────────────────────────────────────
def generar_pdf(html_content):
    html_obj = HTML(string=html_content)
    pdf_io = io.BytesIO()
    html_obj.write_pdf(target=pdf_io)
    pdf_io.seek(0)
    return pdf_io

# ────────────────────────────────────────────────
# Simulación de entrevista (con feedback personalizado)
# ────────────────────────────────────────────────
def simular_entrevista(respuestas, puesto='', empresa=''):
    preguntas = [
        f"¿Por qué querés trabajar en {empresa} como {puesto}?" if empresa and puesto else 
        f"¿Por qué querés trabajar en {empresa}?" if empresa else 
        f"¿Por qué querés trabajar como {puesto}?" if puesto else "¿Por qué querés trabajar acá?",
        
        "¿Cuáles son tus debilidades?",
        
        f"¿Qué sabés sobre {empresa} y por qué te interesa el puesto de {puesto}?" if empresa and puesto else 
        f"¿Qué sabés sobre {empresa}?" if empresa else 
        f"¿Qué sabés sobre el puesto de {puesto}?" if puesto else "¿Qué sabés sobre nuestra empresa?",
        
        f"¿Cómo manejás el estrés en un rol como {puesto} o en una empresa como {empresa}?" if puesto or empresa else "¿Cómo manejás el estrés?"
    ]

    feedbacks = []
    for i, pregunta in enumerate(preguntas):
        respuesta = respuestas.get(i, "")
        base = [
            "Muestra entusiasmo real. Menciona algo específico de la empresa o del puesto.",
            "Elige debilidades que no sean críticas para el puesto y explica cómo las estás mejorando.",
            f"Investiga {empresa if empresa else 'la empresa'}: misión, productos, noticias recientes. Relaciona con {puesto if puesto else 'el rol'}.",
            "Da ejemplos concretos: priorización, comunicación, técnicas de relajación."
        ][i]

        personalizado = base
        respuesta_lower = respuesta.lower()
        if "motiv" in respuesta_lower or "entusiasm" in respuesta_lower:
            personalizado += " Excelente, mencionaste motivación/entusiasmo — eso transmite pasión."
        else:
            personalizado += " Sugerencia: agrega por qué estás motivada o qué te apasiona del puesto."

        if "ingenier" in puesto.lower() or "desarrollador" in puesto.lower() or "técnico" in puesto.lower():
            personalizado += " En roles técnicos, menciona software técnico, proyectos de ingeniería o herramientas específicas."

        feedbacks.append(personalizado)

    return preguntas, feedbacks

# ─── Fin Parte 4/6 ───
# Pega la Parte 5 justo después
# ────────────────────────────────────────────────
# Interfaz principal
# ────────────────────────────────────────────────
def main():
    st.set_page_config(page_title="JobEvo", layout="wide")
    st.title("JobEvo – Arandu Oguata Mbarete Ári")
    st.info(leer_feedback())

    if 'etapa' not in st.session_state: st.session_state.etapa = 0
    if 'datos' not in st.session_state: st.session_state.datos = {}
    if 'pdf' not in st.session_state:   st.session_state.pdf = None
    if 'respuestas_entrevista' not in st.session_state: st.session_state.respuestas_entrevista = {}

    # Sidebar con mejoras acumuladas
    if os.path.exists(MEJORAS_FILE):
        st.sidebar.markdown("### Evolución del sistema")
        st.sidebar.markdown(leer_ultimas_mejoras())

    if st.session_state.etapa == 0:
        st.subheader("Completa tu información")

        c1, c2 = st.columns(2)
        with c1:
            nombre    = st.text_input("Nombre completo", "")
            telefono  = st.text_input("Teléfono", "")
            email     = st.text_input("Email", "@mail.com")
            linkedin  = st.text_input("LinkedIn", "")

        with c2:
            ubicacion = st.text_input("Ciudad", "Asunción")
            edad      = st.number_input("Edad", 16, 40, 22)

        genero = st.selectbox("Género (para personalizar el CV)", ["Femenino", "Masculino", "Neutro"])

        puesto_aspirado = st.text_input("Qué puesto buscas?", "Ej: Desarrollador Python Junior")
        empresa_objetivo = st.text_input("Empresa objetivo (opcional)", "Ej: Itaipú Binacional")

        foto = st.file_uploader("Foto de perfil (opcional)", type=["jpg","png","jpeg"])
        foto_b64 = base64.b64encode(foto.read()).decode() if foto else None

        educacion = st.text_input("Educación secundaria o técnica", "Bachillerato Técnico en Informática (Promoción 2021)")
        titulo_uni = st.text_input("Título universitario o carrera (opcional)", "")

        st.subheader("Idiomas")
        g1, g2 = st.columns(2)
        with g1: guarani = st.selectbox("Guaraní", ["Nativo","Intermedio","Básico","Ninguno"], 1)
        with g2: ingles  = st.selectbox("Inglés",  ["Avanzado","Intermedio B1/B2","Básico A2","Ninguno"], 2)

        st.subheader("Habilidades (una por línea)")
        tec   = st.text_area("Técnicas", height=110, value="Manejo de IA Generativa (Prompts)\nExcel Intermedio\nGoogle Workspace")
        bland = st.text_area("Blandas", height=110, value="Adaptabilidad\nResolución de problemas\nTrabajo en equipo\nGestión del tiempo")

        cert  = st.text_area("Certificaciones (una por línea, opcional)", height=110)

        proyectos = st.text_area("Proyectos destacados", height=80)

        referencias = st.text_area("Referencias (una por línea, opcional, ej: Nombre - Cargo - Contacto)", height=110)

        if st.button("Generar mi CV en PDF"):
            if not nombre:
                st.error("Ingresa al menos tu nombre")
                return

            iniciales = ''.join(w[0].upper() for w in nombre.split()[:3] if w)
            datos = {
                'nombre': nombre,
                'iniciales': iniciales,
                'telefono': telefono.strip(),
                'email': email.strip(),
                'linkedin': linkedin.strip(),
                'ubicacion': ubicacion.strip(),
                'edad': edad,
                'genero': genero,
                'educacion': educacion.strip(),
                'titulo_universitario': titulo_uni.strip(),
                'idiomas': {'guarani': guarani, 'ingles': ingles},
                'habilidades_tecnicas': [h.strip() for h in tec.splitlines() if h.strip()],
                'habilidades_blandas': [h.strip() for h in bland.splitlines() if h.strip()],
                'certificaciones': [h.strip() for h in cert.splitlines() if h.strip()],
                'proyectos': proyectos.strip(),
                'referencias': [h.strip() for h in referencias.splitlines() if h.strip()],
                'puesto_aspirado': puesto_aspirado.strip(),
                'empresa_objetivo': empresa_objetivo.strip()
            }

            html = generar_html_cv(datos, foto_b64)
            with st.spinner("Creando PDF..."):
                st.session_state.pdf = generar_pdf(html)
                st.session_state.datos = datos
            st.session_state.etapa = 1

    # ─── Fin Parte 5/6 ───
    # Pega la Parte 6 al final
    if st.session_state.etapa == 1:
        st.success("¡PDF generado con éxito! 🎉")
        st.download_button(
            label="Descargar mi CV en PDF",
            data=st.session_state.pdf,
            file_name=f"CV_{st.session_state.datos['nombre'].replace(' ','_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        puesto = st.session_state.datos.get('puesto_aspirado', '')
        empresa = st.session_state.datos.get('empresa_objetivo', '')

        st.markdown("### Consejos rápidos para Paraguay (personalizados)")
        for linea in dar_consejos_personalizados(puesto, empresa):
            st.markdown(linea)

        if st.button("→ Practicar entrevista personalizada", use_container_width=True):
            st.session_state.etapa = 2
            st.rerun()

    if st.session_state.etapa == 2:
        st.subheader("Simulación de entrevista personalizada")
        puesto = st.session_state.datos.get('puesto_aspirado', '')
        empresa = st.session_state.datos.get('empresa_objetivo', '')

        preguntas = [
            f"¿Por qué querés trabajar en {empresa} como {puesto}?" if empresa and puesto else 
            f"¿Por qué querés trabajar en {empresa}?" if empresa else 
            f"¿Por qué querés trabajar como {puesto}?" if puesto else "¿Por qué querés trabajar acá?",
            
            "¿Cuáles son tus debilidades?",
            
            f"¿Qué sabés sobre {empresa} y por qué te interesa el puesto de {puesto}?" if empresa and puesto else 
            f"¿Qué sabés sobre {empresa}?" if empresa else 
            f"¿Qué sabés sobre el puesto de {puesto}?" if puesto else "¿Qué sabés sobre nuestra empresa?",
            
            f"¿Cómo manejás el estrés en un rol como {puesto} o en una empresa como {empresa}?" if puesto or empresa else "¿Cómo manejás el estrés?"
        ]

        resp = {}
        for i, q in enumerate(preguntas):
            resp[i] = st.text_input(q, key=f"int_{i}")

        if st.button("Ver feedback personalizado"):
            st.session_state.respuestas_entrevista = resp
            st.session_state.etapa = 3
            st.rerun()

    if st.session_state.etapa == 3:
        st.markdown("---")
        st.markdown("### 🎯 Resultado de tu práctica de entrevista")
        st.markdown("¡Excelente esfuerzo! Aquí tienes un resumen claro y detallado de cómo te fue:")

        puesto = st.session_state.datos.get('puesto_aspirado', '')
        empresa = st.session_state.datos.get('empresa_objetivo', '')

        preguntas, feedbacks = simular_entrevista(st.session_state.respuestas_entrevista, puesto, empresa)

        for i in range(len(preguntas)):
            respuesta = st.session_state.respuestas_entrevista.get(i, "—")
            feedback = feedbacks[i]

            with st.expander(f"**Pregunta {i+1}:** {preguntas[i]}", expanded=True):
                st.markdown(f"**Tu respuesta:** {respuesta}")
                st.markdown(f"**Feedback:** {feedback}")

        st.markdown("---")
        st.markdown("**¡Seguí practicando!** Cada intento te acerca más a esa entrevista exitosa. 💪")
        st.markdown(f"Estás preparándote para brillar en el puesto de **{puesto or 'tu rol deseado'}** {f'en ' + empresa if empresa else ''}.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reiniciar entrevista"):
                st.session_state.etapa = 2
                st.rerun()
        with col2:
            if st.button("← Volver al CV"):
                st.session_state.etapa = 1
                st.rerun()

        cal = st.slider("¿Te ayudó esta práctica? Calificá del 1 al 5", 1, 5, 3, key="calificacion_final")
        if st.button("Enviar calificación"):
            guardar_feedback(cal)
            st.balloons()

            if cal <= 3:
                motivo = f"Calificación baja ({cal}/5) en práctica de entrevista"
                cambio = "Mejoré la presentación de feedback: uso de expanders, emojis y mensajes motivadores"
                registrar_mejora(motivo, cambio)
                st.warning(f"Gracias por la calificación ({cal}/5). He registrado esta retroalimentación y ya estoy mejorando la presentación para la próxima vez.")
            else:
                st.success(f"¡Gracias por tu calificación ({cal}/5)! Me motiva seguir mejorando.")

            if st.button("Volver al inicio"):
                st.session_state.clear()
                st.rerun()

if __name__ == "__main__":
    main()