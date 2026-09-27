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


def generar_preguntas_identificacion(tipo_objetivo="Todos", cantidad=8):
    plantillas = {
        "Función constante": [
            {
                "enunciado": "Un club cobra una tarifa fija de 25 pesos por entrar, sin importar la cantidad de personas que asistan ese día.",
                "respuesta": "Función constante",
            },
            {
                "enunciado": "La mensualidad de un servicio de internet cuesta siempre 300 pesos, aunque el usuario navegue más o menos.",
                "respuesta": "Función constante",
            },
            {
                "enunciado": "Un estacionamiento cobra una tarifa única y plana de 50 pesos por todo el día, sin importar las horas que se deje el auto.",
                "respuesta": "Función constante",
            },
            {
                "enunciado": "La temperatura en una cámara frigorífica se mantiene fija a 4 grados Celsius durante todo el fin de semana.",
                "respuesta": "Función constante",
            },
            {
                "enunciado": "Una empresa paga un bono de puntualidad invariable de 500 pesos mensuales a todos sus empleados, sin excepción.",
                "respuesta": "Función constante",
            },
            {
                "enunciado": "La velocidad de una partícula se registra como 15 m/s en todo momento durante una prueba de control.",
                "respuesta": "Función constante",
            },
            {
                "enunciado": "El impuesto fijo estatal para la propiedad es de 1,200 pesos anuales, independientemente del valor catastral de la casa.",
                "respuesta": "Función constante",
            },
            {
                "enunciado": "Una máquina expendedora dispensa boletos que cuestan siempre 10 pesos, sin importar el horario de compra.",
                "respuesta": "Función constante",
            },
        ],
        "Función lineal": [
            {
                "enunciado": "Un taxi cobra 8 pesos por banderazo más 3 pesos por cada kilómetro recorrido.",
                "respuesta": "Función lineal",
            },
            {
                "enunciado": "Una impresora entrega 12 hojas por minuto, así que la cantidad de hojas impresas crece de manera constante con el tiempo.",
                "respuesta": "Función lineal",
            },
            {
                "enunciado": "Un albañil cobra un cargo base por visita de 200 pesos más 150 pesos por cada hora de trabajo.",
                "respuesta": "Función lineal",
            },
            {
                "enunciado": "Un tanque con 50 litros de agua se llena a razón de 5 litros adicionales por cada minuto que transcurre.",
                "respuesta": "Función lineal",
            },
            {
                "enunciado": "El costo de producción de cuadernos es de 12 pesos por unidad, con un costo fijo de operación nulo.",
                "respuesta": "Función lineal",
            },
            {
                "enunciado": "Un corredor avanza a una velocidad constante de 8 km por hora desde el inicio de la competencia.",
                "respuesta": "Función lineal",
            },
            {
                "enunciado": "Una cuenta de ahorros recibe un depósito semanal constante de 250 pesos sin generar intereses adicionales complejos.",
                "respuesta": "Función lineal",
            },
            {
                "enunciado": "La longitud de un resorte se estira 2 cm por cada kilogramo de peso adicional que se le cuelga.",
                "respuesta": "Función lineal",
            },
        ],
        "Función cuadrática": [
            {
                "enunciado": "Un jardín rectangular tiene perímetro fijo y su área depende del ancho x como A(x) = x(20 - x).",
                "respuesta": "Función cuadrática",
            },
            {
                "enunciado": "La altura de un objeto lanzado al aire se modela con h(t) = -5t² + 30t + 2.",
                "respuesta": "Función cuadrática",
            },
            {
                "enunciado": "Los ingresos mensuales de una tienda en función del precio de su producto principal se describen mediante I(x) = -2x² + 100x.",
                "respuesta": "Función cuadrática",
            },
            {
                "enunciado": "La trayectoria del agua en una fuente ornamental sigue la ecuación parabólica f(x) = -x² + 6x.",
                "respuesta": "Función cuadrática",
            },
            {
                "enunciado": "El área total de un terreno cuadrado en función de la longitud de su lado incrementada se modela con A(l) = (l + 4)².",
                "respuesta": "Función cuadrática",
            },
            {
                "enunciado": "La ganancia neta de una empresa en función de la inversión publicitaria x está dada por G(x) = -3x² + 120x - 400.",
                "respuesta": "Función cuadrática",
            },
            {
                "enunciado": "El consumo de combustible de un auto en función de su velocidad constante se modela mediante C(v) = 0.05v² - 4v + 90.",
                "respuesta": "Función cuadrática",
            },
            {
                "enunciado": "La potencia eléctrica disipada en un circuito en función de la corriente se calcula mediante P(i) = 4i².",
                "respuesta": "Función cuadrática",
            },
        ],
        "Función cúbica": [
            {
                "enunciado": "El volumen de una caja abierta se calcula con V(x) = x(18 - 2x)², donde x representa el recorte de cada esquina.",
                "respuesta": "Función cúbica",
            },
            {
                "enunciado": "El volumen de un cubo se expresa como V(l) = l³, donde l es la longitud de la arista.",
                "respuesta": "Función cúbica",
            },
            {
                "enunciado": "El crecimiento de un fenómeno físico se modela con la función polinómica f(x) = 2x³ - 5x² + x - 3.",
                "respuesta": "Función cúbica",
            },
            {
                "enunciado": "La deformación de una viga bajo cierta carga se rige por la ecuación polinómica D(x) = x³ - 3x.",
                "respuesta": "Función cúbica",
            },
            {
                "enunciado": "El beneficio acumulado de una startup tecnológica durante sus primeros años se representa por B(t) = t³ - 6t² + 9t.",
                "respuesta": "Función cúbica",
            },
            {
                "enunciado": "El caudal de un fluido a través de un conducto especial varía en función del radio según la expresión Q(r) = 4r³.",
                "respuesta": "Función cúbica",
            },
            {
                "enunciado": "La expansión volumétrica de un material con respecto a la temperatura se aproxima mediante V(T) = 0.5T³ + 10.",
                "respuesta": "Función cúbica",
            },
            {
                "enunciado": "Una función de costos complejos para la fabricación en masa está dada por C(q) = q³ - 4q² + 20q + 150.",
                "respuesta": "Función cúbica",
            },
        ],
        "Función racional": [
            {
                "enunciado": "El costo promedio por unidad de un producto se describe con C(x) = 120/(x + 4) + 6.",
                "respuesta": "Función racional",
            },
            {
                "enunciado": "La velocidad promedio de un viaje depende de la distancia y el tiempo mediante v = 150/(t + 5).",
                "respuesta": "Función racional",
            },
            {
                "enunciado": "La concentración de un medicamento en el torrente sanguíneo a lo largo del tiempo se modela con C(t) = 50 / (t² + 1).",
                "respuesta": "Función racional",
            },
            {
                "enunciado": "El tiempo que tardan varios obreros en construir una barda se expresa mediante T(x) = 40/x, donde x es el número de trabajadores.",
                "respuesta": "Función racional",
            },
            {
                "enunciado": "La resistencia eléctrica equivalente en paralelo de dos componentes se rige por la fórmula R(x) = 10x / (x + 10).",
                "respuesta": "Función racional",
            },
            {
                "enunciado": "La intensidad luminosa percibida a cierta distancia de una fuente se modela con I(d) = 500 / d².",
                "respuesta": "Función racional",
            },
            {
                "enunciado": "El porcentaje de impurezas en un tanque de purificación se calcula con P(t) = (20t + 5) / (t + 2).",
                "respuesta": "Función racional",
            },
            {
                "enunciado": "La razón de eficiencia de una máquina industrial se describe mediante E(x) = (100x - 5) / (x + 1).",
                "respuesta": "Función racional",
            },
        ],
        "Función exponencial": [
            {
                "enunciado": "Una colonia de bacterias duplica su población cada hora, por lo que P(t) = 5·2^t.",
                "respuesta": "Función exponencial",
            },
            {
                "enunciado": "El dinero en una cuenta de inversión con interés compuesto continuo crece según la fórmula A(t) = 1000·e^(0.05t).",
                "respuesta": "Función exponencial",
            },
            {
                "enunciado": "La depreciación del valor de una maquinaria disminuye un 15% cada año, modelándose como V(t) = 50000·(0.85)^t.",
                "respuesta": "Función exponencial",
            },
            {
                "enunciado": "La cantidad de material radiactivo remonta un proceso de descomposición donde M(t) = 200·(1/2)^(t/3).",
                "respuesta": "Función exponencial",
            },
            {
                "enunciado": "La propagación de un rumor en una red social sigue un crecimiento explosivo dado por R(d) = 10·3^d.",
                "respuesta": "Función exponencial",
            },
            {
                "enunciado": "La presión atmosférica disminuye exponencialmente a medida que aumenta la altitud h, expresada como P(h) = 1013·e^(-0.12h).",
                "respuesta": "Función exponencial",
            },
            {
                "enunciado": "El número de usuarios activos de una plataforma web se triplica cada mes según N(m) = 500·3^m.",
                "respuesta": "Función exponencial",
            },
            {
                "enunciado": "Una reacción química duplica su velocidad de catálisis cada 10 grados de temperatura, modelada por V(T) = 2^(T/10).",
                "respuesta": "Función exponencial",
            },
        ],
        "Función valor absoluto": [
            {
                "enunciado": "La distancia de un punto a cero se modela con d(x) = |x - 3|.",
                "respuesta": "Función valor absoluto",
            },
            {
                "enunciado": "El margen de error permitido en la fabricación de una pieza metálica se calcula mediante E(x) = |x - 10|.",
                "respuesta": "Función valor absoluto",
            },
            {
                "enunciado": "La variación térmica respecto a una temperatura ideal de 22 grados se representa con f(T) = |T - 22|.",
                "respuesta": "Función valor absoluto",
            },
            {
                "enunciado": "La desviación absoluta de los datos de ventas respecto a la media se define por D(x) = |x - 150|.",
                "respuesta": "Función valor absoluto",
            },
            {
                "enunciado": "Un sensor mide la diferencia de potencial simétrica mediante V(x) = 3|x| - 5.",
                "respuesta": "Función valor absoluto",
            },
            {
                "enunciado": "La altura del rebote de una pelota simétrica respecto a su eje de caída se modela con h(t) = -|t - 2| + 4.",
                "respuesta": "Función valor absoluto",
            },
            {
                "enunciado": "El costo de desvío de una ruta de entrega se calcula en función de los kilómetros extra como C(x) = 15|x - 5|.",
                "respuesta": "Función valor absoluto",
            },
            {
                "enunciado": "La ganancia o pérdida absoluta en la bolsa para un activo específico se describe por G(x) = |2x - 10|.",
                "respuesta": "Función valor absoluto",
            },
        ]
    }

    # Función auxiliar para generar opciones incluyendo distractores
    def crear_opciones(respuesta_correcta):
        distractores = [tf for tf in TIPOS_FUNCION if tf != respuesta_correcta]
        opciones = random.sample(distractores, 3) + [respuesta_correcta]
        random.shuffle(opciones)
        return opciones

    if tipo_objetivo == "Todos":
        preguntas = []
        for tipo, lista in plantillas.items():
            for item in lista:
                preguntas.append({
                    "tipo": tipo,
                    **item,
                    "opciones": crear_opciones(item["respuesta"])
                })
        random.shuffle(preguntas)
        return preguntas[:cantidad]

    preguntas_disponibles = plantillas.get(tipo_objetivo, [])
    if not preguntas_disponibles:
        return []

    # Genera exactamente 'cantidad' preguntas, permitiendo repeticiones
    preguntas_generadas = []
    for _ in range(cantidad):
        item = random.choice(preguntas_disponibles)
        preguntas_generadas.append({
            "tipo": tipo_objetivo,
            **item,
            "opciones": crear_opciones(item["respuesta"])
        })
    
    return preguntas_generadas


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
              genai.configure(api_key=st.secrets["GEMINI_API_KEY_1"])
              modelo = genai.GenerativeModel("gemini-3-flash-preview")

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
        tipo_quiz = st.selectbox("Selecciona el tipo para practicar", ["Todos"] + TIPOS_FUNCION)
        cantidad_quiz = st.slider("Número de preguntas", min_value=3, max_value=8, value=5, key="cantidad_quiz")
        
        if st.button("Generar preguntas de opción múltiple", key="generar_quiz"):
            st.session_state.quiz_identificacion = generar_preguntas_identificacion(tipo_quiz, cantidad_quiz)
            st.session_state.quiz_respuestas = {}

        if "quiz_identificacion" in st.session_state and st.session_state.quiz_identificacion:
            preguntas = st.session_state.quiz_identificacion

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
            st.info("Genera un conjunto de preguntas para practicar la identificación de tipos de función.")

# ==========================================================
#  OPCIÓN 7: GRÁFICAS CON DESMOS
# ==========================================================
if st.session_state.vista == "desmos":
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
