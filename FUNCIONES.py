import random
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

st.set_page_config(page_title="Funciones Matemáticas", page_icon="📊", layout="centered")

TIPOS_FUNCION = [
    "Función constante",
    "Función lineal",
    "Función cuadrática",
    "Función cúbica",
    "Función racional",
    "Función exponencial",
    "Función valor absoluto",
]


def generar_preguntas_identificacion(tipo_objetivo="Todos", cantidad=5):
    """Genera preguntas usando IA para garantizar variedad y cantidad exacta."""
    
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        modelo = genai.GenerativeModel("gemini-3-flash")
        
        if tipo_objetivo == "Todos":
            prompt = (
                f"Genera EXACTAMENTE {cantidad} problemas de identificación de tipos de funciones matemáticas. "
                "Cada problema debe ser un escenario real de la vida cotidiana que se pueda modelar con UNO de estos tipos: "
                "Función constante, Función lineal, Función cuadrática, Función cúbica, Función racional, "
                "Función exponencial, Función valor absoluto, Función logarítmica. "
                "\n\nPara cada problema, devuelve EXACTAMENTE en este formato (sin variaciones):\n"
                "PROBLEMA: [descripción del escenario]\n"
                "TIPO: [el tipo de función correcto]\n"
                "---\n"
                "\nAsegúrate de que cada tipo de función aparezca DISTRIBUIDO entre los problemas. "
                "Números pares de problemas = dos tipos de función solo. Números impares = variación más distribuida. "
                "Escribe en español claro y accesible para estudiantes de secundaria."
            )
        else:
            prompt = (
                f"Genera EXACTAMENTE {cantidad} problemas diferentes que se modelan con una {tipo_objetivo.lower()}. "
                "Cada problema debe ser un escenario real y diferente de los demás. "
                "\n\nPara cada problema, devuelve EXACTAMENTE en este formato (sin variaciones):\n"
                "PROBLEMA: [descripción del escenario]\n"
                "TIPO: {tipo_objetivo}\n"
                "---\n"
                "\nEscribe en español claro y accesible para estudiantes de secundaria."
            )
        
        respuesta = modelo.generate_content(prompt)
        texto = respuesta.text
        
        # Parsear la respuesta
        problemas = []
        bloques = texto.split("---")
        
        for bloque in bloques:
            bloque = bloque.strip()
            if not bloque:
                continue
            
            lineas = bloque.split("\n")
            problema_texto = None
            tipo_respuesta = None
            
            for linea in lineas:
                if linea.startswith("PROBLEMA:"):
                    problema_texto = linea.replace("PROBLEMA:", "").strip()
                elif linea.startswith("TIPO:"):
                    tipo_respuesta = linea.replace("TIPO:", "").strip()
            
            if problema_texto and tipo_respuesta:
                # Validar que el tipo sea correcto
                tipo_limpio = tipo_respuesta.lower().strip()
                tipo_valido = None
                
                for tf in TIPOS_FUNCION:
                    if tf.lower() in tipo_limpio or tipo_limpio in tf.lower():
                        tipo_valido = tf
                        break
                
                if tipo_valido:
                    # Generar opciones con distractores
                    distractores = [t for t in TIPOS_FUNCION if t != tipo_valido]
                    opciones = random.sample(distractores, min(3, len(distractores)))
                    opciones.append(tipo_valido)
                    random.shuffle(opciones)
                    
                    problemas.append({
                        "tipo": tipo_valido,
                        "enunciado": problema_texto,
                        "respuesta": tipo_valido,
                        "opciones": opciones
                    })
        
        # Si no se parsean suficientes problemas, retornar lo que se pudo generar
        if len(problemas) > 0:
            return problemas[:cantidad]
        else:
            st.error("No se pudieron generar problemas válidos. Intenta nuevamente.")
            return []
    
    except Exception as e:
        st.error(f"Error al generar preguntas con IA: {e}")
        return []


# ==========================================================
#  ESTADO INICIAL
# ==========================================================
if "vista" not in st.session_state:
    st.session_state.vista = "inicio"

if "juego" not in st.session_state:
    st.session_state.juego = None  # guardará m1, b1, m2, b2, t, d1, d2, ganador

if "lanzamiento" not in st.session_state:
    st.session_state.lanzamiento = None  # juego de función cuadrática

if "caja" not in st.session_state:
    st.session_state.caja = None  # juego de función cúbica

if "guerra_precios" not in st.session_state:
    st.session_state.guerra_precios = None  # juego de función racional

st.title("📊 Menú de Opciones")

# ==========================================================
#  MENÚ
# ==========================================================
fila1_col1, fila1_col2, fila1_col3, fila1_col4 = st.columns(4)

with fila1_col1:
    if st.button("1️⃣ Constante"):
        st.session_state.vista = "constante"

with fila1_col2:
    if st.button("2️⃣ Lineal (juego)"):
        st.session_state.vista = "juego"
        st.session_state.juego = None  # nueva partida al entrar

with fila1_col3:
    if st.button("3️⃣ Cuadrática"):
        st.session_state.vista = "cuadratica"

with fila1_col4:
    if st.button("4️⃣ Cúbica"):
        st.session_state.vista = "cubica"

fila2_col1, fila2_col2, fila2_col3 = st.columns(3)

with fila2_col1:
    if st.button("5️⃣ Racional"):
        st.session_state.vista = "racional"

with fila2_col2:
    if st.button("6️⃣ Problemas (IA)"):
        st.session_state.vista = "ia"

with fila2_col3:
    if st.button("7️⃣ Gráficas (Desmos)"):
        st.session_state.vista = "desmos"

st.divider()

# ==========================================================
#  OPCIÓN 1: FUNCIÓN CONSTANTE
# ==========================================================
if st.session_state.vista == "constante":
    st.subheader("📈 Función constante")

    valor = st.number_input("Dame un número", value=0.0, step=1.0)

    if st.button("Graficar"):
        try:
            fig = plt.figure(figsize=(8, 6))
            x = [-10, 10]
            y = [valor, valor]

            plt.plot(x, y, label=f"y = {valor}")
            plt.title("Función constante")
            plt.xlabel("Eje x")
            plt.ylabel("Eje y")
            plt.grid(True)
            plt.legend()

            st.pyplot(fig)
            plt.close(fig)
        except Exception as ex:
            st.error(f"❌ Error inesperado: {ex}")

# ==========================================================
#  OPCIÓN 2: JUEGO DE FUNCIÓN LINEAL
# ==========================================================
elif st.session_state.vista == "juego":
    st.subheader("🏁 Carrera de funciones 🏁")

    if st.session_state.juego is None:
        m1 = random.randint(2, 8)
        b1 = random.randint(0, 10)
        m2 = random.randint(2, 8)
        b2 = random.randint(0, 10)
        t = random.randint(-10, 10)

        d1 = m1 * t + b1
        d2 = m2 * t + b2

        if d1 > d2:
            ganador = "rojo"
        elif d2 > d1:
            ganador = "azul"
        else:
            ganador = "empate"

        st.session_state.juego = dict(
            m1=m1, b1=b1, m2=m2, b2=b2, t=t, d1=d1, d2=d2, ganador=ganador
        )

    j = st.session_state.juego

    st.write("🏁 BIENVENIDO A LA CARRERA MATEMÁTICA 🏁")
    st.write("Hoy competirán dos autos usando funciones lineales:")
    st.write("Distancia = velocidad × tiempo + ventaja inicial")
    st.write("Forma matemática: y = mx + b")
    st.write(f"Rojo🚗: y = {j['m1']}x + {j['b1']}")
    st.write(f"Azul🚙: y = {j['m2']}x + {j['b2']}")
    st.write(f"Tiempo t: {j['t']}")

    c1, c2, c3 = st.columns(3)
    eleccion = None
    with c1:
        if st.button("Rojo"):
            eleccion = "rojo"
    with c2:
        if st.button("Azul"):
            eleccion = "azul"
    with c3:
        if st.button("Empate"):
            eleccion = "empate"

    if eleccion:
        if eleccion == j["ganador"]:
            st.success("🎉 Correcto")
        else:
            st.error(f"❌ Era: {j['ganador']}")
        st.write(f"Rojo: {j['d1']} | Azul: {j['d2']}")

    if st.button("🔄 Reiniciar"):
        st.session_state.juego = None
        st.rerun()

# ==========================================================
#  OPCIÓN 3: JUEGO DE FUNCIÓN CUADRÁTICA — CARRERA DE LANZAMIENTOS
# ==========================================================
elif st.session_state.vista == "cuadratica":
    st.subheader("🚀 Carrera de lanzamientos 🚀")

    if st.session_state.lanzamiento is None:
        # a en rango amplio de -10 a 10 (excluyendo 0 para mantener la parábola)
        posibles_a = [round(v, 1) for v in np.arange(-10.0, 10.5, 0.5) if v != 0]
        a1 = random.choice(posibles_a)
        b1 = random.randint(-10, 20)
        c1 = random.randint(-10, 10)

        a2 = random.choice(posibles_a)
        b2 = random.randint(-10, 20)
        c2 = random.randint(-10, 10)

        # t en rango de -10 a 10
        t = random.randint(-10, 10)

        h1 = a1 * t**2 + b1 * t + c1
        h2 = a2 * t**2 + b2 * t + c2

        if h1 > h2:
            ganador = "objeto1"
        elif h2 > h1:
            ganador = "objeto2"
        else:
            ganador = "empate"

        st.session_state.lanzamiento = dict(
            a1=a1, b1=b1, c1=c1, a2=a2, b2=b2, c2=c2, t=t, h1=h1, h2=h2, ganador=ganador
        )

    j = st.session_state.lanzamiento

    st.write("🎯 Dos objetos siguen una trayectoria que se puede modelar con una función cuadrática.")
    st.write("La forma general es y = ax² + bx + c. El valor de a puede variar ampliamente de -10 a 10.")
    st.write("Si a > 0, la parábola abre hacia arriba; si a < 0, la parábola abre hacia abajo.")
    st.write("La altura de cada objeto depende del valor de t:")
    st.write(f"🔴 Objeto 1: h(t) = {j['a1']}t² + ({j['b1']})t + ({j['c1']})")
    st.write(f"🔵 Objeto 2: h(t) = {j['a2']}t² + ({j['b2']})t + ({j['c2']})")
    st.write(f"⏱️ Tiempo/Valor t: {j['t']}")
    st.write("¿Cuál objeto alcanza un valor más alto en ese instante?")

    c1, c2, c3 = st.columns(3)
    eleccion = None
    with c1:
        if st.button("🔴 Objeto 1"):
            eleccion = "objeto1"
    with c2:
        if st.button("🔵 Objeto 2"):
            eleccion = "objeto2"
    with c3:
        if st.button("Empate"):
            eleccion = "empate"

    if eleccion:
        if eleccion == j["ganador"]:
            st.success("🎉 Correcto")
        else:
            st.error(f"❌ Era: {j['ganador']}")
        st.write(f"Valor Objeto 1: {j['h1']:.2f} | Valor Objeto 2: {j['h2']:.2f}")

        # Gráfica adaptada al rango de t de -10 a 10
        x = np.linspace(-12, 12, 400)
        y1 = j["a1"] * x**2 + j["b1"] * x + j["c1"]
        y2 = j["a2"] * x**2 + j["b2"] * x + j["c2"]

        fig = plt.figure(figsize=(8, 6))
        plt.plot(x, y1, color="red", label="Objeto 1")
        plt.plot(x, y2, color="blue", label="Objeto 2")
        plt.scatter([j["t"]], [j["h1"]], color="red", zorder=5)
        plt.scatter([j["t"]], [j["h2"]], color="blue", zorder=5)
        plt.axvline(j["t"], color="gray", linestyle="--", linewidth=1)
        plt.axhline(0, color="black", linewidth=0.8)
        plt.title("Trayectoria / Función de los dos objetos")
        plt.xlabel("Tiempo/Variable t")
        plt.ylabel("Valor h(t)")
        plt.grid(True)
        plt.legend()
        st.pyplot(fig)
        plt.close(fig)

    if st.button("🔄 Nuevo lanzamiento"):
        st.session_state.lanzamiento = None
        st.rerun()

# ==========================================================
#  OPCIÓN 4: JUEGO DE FUNCIÓN CÚBICA — EL RETO DE LA CAJA
# ==========================================================
elif st.session_state.vista == "cubica":
    st.subheader("📈 Reto de función cúbica")

    if st.session_state.caja is None:
        # a en rango amplio de -10 a 10 (excluyendo 0)
        a = random.choice([v for v in range(-10, 11) if v != 0])
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        d = random.randint(-10, 10)
        # x en el rango de -10 a 10
        x = random.randint(-10, 10)
        resultado = a * x**3 + b * x**2 + c * x + d
        st.session_state.caja = dict(a=a, b=b, c=c, d=d, x=x, resultado=resultado)

    j = st.session_state.caja

    st.write("Una función cúbica tiene la forma:")
    st.latex(r"f(x)=ax^3+bx^2+cx+d,\quad a\ne 0")
    st.write(
        f"Sustituye x = {j['x']} en f(x) = ({j['a']})x³ + ({j['b']})x² + "
        f"({j['c']})x + ({j['d']})."
    )

    respuesta = st.number_input(
        "¿Cuál es el valor de f(x)?", step=1.0, format="%.2f", key="respuesta_cubica"
    )

    if st.button("✅ Comprobar función cúbica"):
        st.write(
            f"Sustitución: f({j['x']}) = ({j['a']})({j['x']})³ + "
            f"({j['b']})({j['x']})² + ({j['c']})({j['x']}) + ({j['d']})"
        )
        st.write(f"Resultado correcto: f({j['x']}) = {j['resultado']}")
        if abs(respuesta - j["resultado"]) < 0.01:
            st.success("🎉 Correcto. Sustituiste x correctamente.")
        else:
            st.error("❌ Revisa las potencias, los signos y la sustitución de x.")

        xs = np.linspace(-12, 12, 400)
        ys = j["a"] * xs**3 + j["b"] * xs**2 + j["c"] * xs + j["d"]

        fig = plt.figure(figsize=(8, 6))
        plt.plot(xs, ys, label="f(x) = ax³ + bx² + cx + d")
        plt.scatter([j["x"]], [j["resultado"]], color="red", zorder=5, label="Valor calculado")
        plt.title("Gráfica de la función cúbica")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.grid(True)
        plt.legend()
        st.pyplot(fig)
        plt.close(fig)

    if st.button("🔄 Nueva lámina"):
        st.session_state.caja = None
        st.rerun()

# ==========================================================
#  OPCIÓN 5: JUEGO DE FUNCIÓN RACIONAL — GUERRA DE PRECIOS
# ==========================================================
elif st.session_state.vista == "racional":
    st.subheader("💰 Guerra de precios 💰")

    if st.session_state.guerra_precios is None:
        a1 = random.randint(50, 150)
        b1 = random.randint(1, 5)
        c1 = random.randint(3, 10)

        a2 = random.randint(50, 150)
        b2 = random.randint(1, 5)
        c2 = random.randint(3, 10)

        x = random.randint(5, 30)

        costo1 = a1 / (x + b1) + c1
        costo2 = a2 / (x + b2) + c2

        if costo1 < costo2:
            ganador = "negocio1"
        elif costo2 < costo1:
            ganador = "negocio2"
        else:
            ganador = "empate"

        st.session_state.guerra_precios = dict(
            a1=a1, b1=b1, c1=c1, a2=a2, b2=b2, c2=c2, x=x, costo1=costo1, costo2=costo2, ganador=ganador
        )

    j = st.session_state.guerra_precios

    st.write("🏭 Dos negocios producen el mismo artículo. El costo por unidad se modela con una función racional.")
    st.write("La forma general es C(x) = a/(x + b) + c, donde a, b y c son constantes.")
    st.write("Cuando x aumenta, el término a/(x + b) disminuye y el costo se acerca a c. Por eso la gráfica tiene una asíntota horizontal.")
    st.write("Ejemplo: C(x) = 120/(x + 4) + 6. Si x = 10, entonces C(10) = 120/14 + 6 ≈ 14.57.")
    st.write(f"🏪 Negocio 1: costo(x) = {j['a1']}/(x + {j['b1']}) + {j['c1']}")
    st.write(f"🏬 Negocio 2: costo(x) = {j['a2']}/(x + {j['b2']}) + {j['c2']}")
    st.write(f"📦 Producción: x = {j['x']} unidades")
    st.write("Sustituye x en cada fórmula y calcula el costo por unidad.")
    respuesta_costo1 = st.number_input(
        "Costo del Negocio 1", min_value=0.0, step=0.01, format="%.2f", key="respuesta_costo1"
    )
    respuesta_costo2 = st.number_input(
        "Costo del Negocio 2", min_value=0.0, step=0.01, format="%.2f", key="respuesta_costo2"
    )

    if st.button("✅ Comprobar costos"):
        st.write(
            f"Sustitución 1: C({j['x']}) = {j['a1']}/({j['x']} + {j['b1']}) + {j['c1']}"
        )
        st.write(
            f"Sustitución 2: C({j['x']}) = {j['a2']}/({j['x']} + {j['b2']}) + {j['c2']}"
        )
        if abs(respuesta_costo1 - j["costo1"]) < 0.01 and abs(respuesta_costo2 - j["costo2"]) < 0.01:
            st.success("🎉 Correcto. Sustituiste x correctamente en las dos funciones.")
        else:
            st.error("❌ Revisa los paréntesis y la división en alguna sustitución.")
        st.write(f"Resultados correctos: Costo 1 = {j['costo1']:.2f} | Costo 2 = {j['costo2']:.2f}")

        x_vals = np.linspace(1, 50, 300)
        y1 = j["a1"] / (x_vals + j["b1"]) + j["c1"]
        y2 = j["a2"] / (x_vals + j["b2"]) + j["c2"]

        fig = plt.figure(figsize=(8, 6))
        plt.plot(x_vals, y1, color="orange", label="Negocio 1")
        plt.plot(x_vals, y2, color="purple", label="Negocio 2")
        plt.axhline(j["c1"], color="orange", linestyle="--", linewidth=1, label=f"Asíntota Negocio 1: y={j['c1']}")
        plt.axhline(j["c2"], color="purple", linestyle="--", linewidth=1, label=f"Asíntota Negocio 2: y={j['c2']}")
        plt.scatter([j["x"]], [j["costo1"]], color="orange", zorder=5)
        plt.scatter([j["x"]], [j["costo2"]], color="purple", zorder=5)
        plt.axvline(j["x"], color="gray", linestyle="--", linewidth=1)
        plt.title("Costo por unidad según producción")
        plt.xlabel("Unidades producidas (x)")
        plt.ylabel("Costo por unidad")
        plt.grid(True)
        plt.legend()
        st.pyplot(fig)
        plt.close(fig)

    if st.button("🔄 Nueva ronda"):
        st.session_state.guerra_precios = None
        st.rerun()

# ==========================================================
#  OPCIÓN 6: PROBLEMAS GENERADOS CON IA
# ==========================================================
elif st.session_state.vista == "ia":
    st.subheader("🤖 Generar problemas")

    tab_ia, tab_quiz = st.tabs(["Problemas con IA", "Identifica la función"])

    with tab_ia:
        opciones_finales = ["Todos"] + TIPOS_FUNCION
        tipo = st.selectbox("Elige el tipo de función", opciones_finales)
        cantidad = st.slider("Cantidad de ejercicios", min_value=3, max_value=10, value=5)

        if st.button("Generar con IA"):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                modelo = genai.GenerativeModel("gemini-1.5-flash")

                prompt = (
                    f"Genera {cantidad} situaciones problema de la vida real que se puedan modelar "
                    f"con una {tipo.lower()}. "
                    "Cada situación debe estar bien contextualizada (un escenario claro, con datos "
                    "concretos y coherentes: nombres, cantidades, unidades), redactada de forma clara "
                    "para estudiantes de secundaria, y debe plantear una pregunta explícita al final "
                    "que el estudiante deba resolver planteando la función correspondiente. "
                    "NO incluyas las respuestas ni el desarrollo de los problemas, solo el enunciado. "
                    "Numera cada situación del 1 al "
                    f"{cantidad}. "
                    "Escribe en texto plano, sin asteriscos, sin emojis, sin formato markdown."
                )

                r = modelo.generate_content(prompt)
                st.write(r.text)
            except Exception as error:
                st.error(f"Error: {error}")

    with tab_quiz:
        st.write("### 📝 Quiz: Identifica el tipo de función")
        st.write("Generado con IA - respuestas ilimitadas")
        
        tipo_quiz = st.selectbox("Selecciona el tipo para practicar", ["Todos"] + TIPOS_FUNCION, key="tipo_quiz_select")
        cantidad_quiz = st.slider("Número de preguntas", min_value=3, max_value=10, value=5, key="cantidad_quiz_slider")
        
        if st.button("Generar preguntas de opción múltiple", key="generar_quiz"):
            with st.spinner("Generando preguntas con IA..."):
                st.session_state.quiz_identificacion = generar_preguntas_identificacion(tipo_quiz, cantidad_quiz)
                st.session_state.quiz_respuestas = {}
        
        if "quiz_identificacion" in st.session_state and st.session_state.quiz_identificacion:
            preguntas = st.session_state.quiz_identificacion
            
            if len(preguntas) == 0:
                st.warning("No se pudieron generar preguntas. Intenta nuevamente.")
            else:
                st.success(f"✅ Se generaron {len(preguntas)} preguntas")
                
                for i, pregunta in enumerate(preguntas):
                    st.markdown(f"### Pregunta {i + 1}")
                    st.write(pregunta["enunciado"])

                    respuesta = st.radio(
                        "Selecciona la respuesta correcta:",
                        pregunta["opciones"],
                        index=None,
                        key=f"pregunta_{i}",
                    )

                    if respuesta is not None:
                        st.session_state.quiz_respuestas[i] = respuesta

                if st.button("Corregir respuestas", key="corregir_quiz"):
                    aciertos = 0
                    total = len(preguntas)

                    for i, pregunta in enumerate(preguntas):
                        respuesta_usuario = st.session_state.get(f"pregunta_{i}")
                        if respuesta_usuario == pregunta["respuesta"]:
                            aciertos += 1

                    st.success(f"Tu resultado: {aciertos}/{total} respuestas correctas.")

                    for i, pregunta in enumerate(preguntas):
                        respuesta_usuario = st.session_state.get(f"pregunta_{i}")
                        estado = "✅ Correcta" if respuesta_usuario == pregunta["respuesta"] else "❌ Incorrecta"
                        st.write(f"Pregunta {i + 1}: {estado}. Respuesta correcta: {pregunta['respuesta']}")

                    if aciertos == total:
                        st.balloons()
        else:
            st.info("Haz clic en 'Generar preguntas de opción múltiple' para comenzar.")

# ==========================================================
#  OPCIÓN 7: GRÁFICAS CON DESMOS
# ==========================================================
elif st.session_state.vista == "desmos":
    st.subheader("📐 Gráficas con Desmos")

    desmos_html = """
    <div id="calculator" style="width: 100%; height: 500px;"></div>
    <script src="https://www.desmos.com/api/v1.12/calculator.js?apiKey=9bda5869329f43429dddd48875ee6168"></script>
    <script>
    var elt = document.getElementById('calculator');
    var calculator = Desmos.GraphingCalculator(elt);

    // Definición de expresiones en Desmos
    calculator.setExpression({id: 'graph1', latex: 'y = x^2'});
    calculator.setExpression({id: 'slider', latex: 'a = 3'});
    calculator.setExpression({id: 'graph2', latex: 'y = a * x'});
    </script>
    """

    components.html(desmos_html, height=700)
