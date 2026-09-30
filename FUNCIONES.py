import random
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import json


st.set_page_config(page_title="Mathematical Functions", page_icon="📊", layout="centered")

FUNCTION_TYPES = [
    "Constant function",
    "Linear function",
    "Quadratic function",
    "Cubic function",
    "Rational function",
    "Exponential function",
    "Absolute value function",
]


def generate_identification_questions(target_type="All", amount=8):
    templates = {
        "Constant function": [
            {
                "statement": "A club charges a fixed fee of 25 pesos to enter, regardless of how many people attend that day.",
                "answer": "Constant function",
            },
            {
                "statement": "The monthly fee for an internet service is always 300 pesos, whether the user browses more or less.",
                "answer": "Constant function",
            },
            {
                "statement": "A parking lot charges a single flat fee of 50 pesos for the entire day, regardless of how many hours the car is parked.",
                "answer": "Constant function",
            },
            {
                "statement": "The temperature in a refrigerated chamber remains fixed at 4 degrees Celsius throughout the weekend.",
                "answer": "Constant function",
            },
            {
                "statement": "A company pays a punctuality bonus of 500 pesos per month to all employees, without exception.",
                "answer": "Constant function",
            },
            {
                "statement": "The speed of a particle is recorded as 15 m/s at all times during a control test.",
                "answer": "Constant function",
            },
            {
                "statement": "The state property tax is 1,200 pesos per year, regardless of the appraised value of the house.",
                "answer": "Constant function",
            },
            {
                "statement": "A vending machine dispenses tickets that always cost 10 pesos, regardless of the time of purchase.",
                "answer": "Constant function",
            },
            {
                "statement": "The standard shipping cost for any package within the city is 45 pesos, regardless of weight or size.",
                "answer": "Constant function",
            },
            {
                "statement": "A digital magazine subscription costs exactly 150 pesos per month, with no additional charges for special articles.",
                "answer": "Constant function",
            },
            {
                "statement": "The gym membership fee is a flat and invariant 600 pesos per month, regardless of how often you attend.",
                "answer": "Constant function",
            },
            {
                "statement": "The movie ticket price at the local cinema stays fixed at 80 pesos every day of the week, with no exceptions.",
                "answer": "Constant function",
            },
            {
                "statement": "A traffic ticket for improper parking has a single amount of 1,500 pesos, regardless of the area of the violation.",
                "answer": "Constant function",
            },
            {
                "statement": "A trainee's daily salary is fixed at 200 pesos net, regardless of overtime hours worked.",
                "answer": "Constant function",
            },
            {
                "statement": "The storage cost on a server is 50 pesos per month, regardless of the gigabytes used.",
                "answer": "Constant function",
            },
            {
                "statement": "A school scholarship provides a constant monetary support of 1,000 pesos each month during the school cycle.",
                "answer": "Constant function",
            },
            {
                "statement": "The fee for issuing a study certificate is a single and permanent amount of 120 pesos.",
                "answer": "Constant function",
            },
            {
                "statement": "The annual maintenance fee for the neighborhood is 2,400 pesos, without variation by the location of the house.",
                "answer": "Constant function",
            },
            {
                "statement": "A toll road charges a fixed fee of 35 pesos to all private cars that pass through.",
                "answer": "Constant function",
            },
            {
                "statement": "The basic fixed telephone line charge is 199 pesos per month, regardless of the local calls made.",
                "answer": "Constant function",
            },
        ],
        "Linear function": [
            {
                "statement": "A taxi charges 8 pesos for the flag drop plus 3 pesos for each kilometer traveled.",
                "answer": "Linear function",
            },
            {
                "statement": "A printer produces 12 sheets per minute, so the number of printed sheets grows at a constant rate with time.",
                "answer": "Linear function",
            },
            {
                "statement": "A bricklayer charges a base fee of 200 pesos per visit plus 150 pesos for each hour of work.",
                "answer": "Linear function",
            },
            {
                "statement": "A tank with 50 liters of water fills at a rate of 5 additional liters per minute.",
                "answer": "Linear function",
            },
            {
                "statement": "The production cost of notebooks is 12 pesos per unit, with no fixed operating cost.",
                "answer": "Linear function",
            },
            {
                "statement": "A runner advances at a constant speed of 8 km per hour from the beginning of the race.",
                "answer": "Linear function",
            },
            {
                "statement": "A savings account receives a constant weekly deposit of 250 pesos without generating complex additional interest.",
                "answer": "Linear function",
            },
            {
                "statement": "The length of a spring stretches 2 cm for each additional kilogram of weight hung from it.",
                "answer": "Linear function",
            },
            {
                "statement": "A moving company charges 500 pesos for the basic service plus 50 pesos for each floor to go up.",
                "answer": "Linear function",
            },
            {
                "statement": "A fuel tank starts with 10 liters and receives a constant supply of 4 liters per minute.",
                "answer": "Linear function",
            },
            {
                "statement": "The production cost of a toy factory is 30 pesos per piece, with an initial fixed cost of 0 pesos.",
                "answer": "Linear function",
            },
            {
                "statement": "A streaming service charges a fixed fee of 20 pesos plus 5 pesos for each extra movie rented.",
                "answer": "Linear function",
            },
            {
                "statement": "A candle burns at a constant rate of 1.5 cm for each hour it remains lit.",
                "answer": "Linear function",
            },
            {
                "statement": "A technician charges 150 pesos for the home diagnosis plus 80 pesos per hour of repair.",
                "answer": "Linear function",
            },
            {
                "statement": "The water level in a well rises 12 cm for each hour of continuous pumping.",
                "answer": "Linear function",
            },
            {
                "statement": "A person walks at a constant speed of 5 km per hour from the central park.",
                "answer": "Linear function",
            },
            {
                "statement": "The electricity bill includes a fixed charge of 40 pesos plus 2 pesos per kilowatt-hour consumed.",
                "answer": "Linear function",
            },
            {
                "statement": "A mobile phone plan includes 100 base minutes plus 1.5 pesos for each additional minute used.",
                "answer": "Linear function",
            },
            {
                "statement": "The temperature of a substance increases uniformly at a rate of 3 degrees Celsius per minute.",
                "answer": "Linear function",
            },
            {
                "statement": "A salesperson receives a base salary of 4,000 pesos plus a fixed commission of 200 pesos for each item sold.",
                "answer": "Linear function",
            },
        ],
        "Quadratic function": [
            {
                "statement": "A rectangular garden has a fixed perimeter, and its area depends on width x as A(x) = x(20 - x).",
                "answer": "Quadratic function",
            },
            {
                "statement": "The height of an object thrown into the air is modeled by h(t) = -5t² + 30t + 2.",
                "answer": "Quadratic function",
            },
            {
                "statement": "The monthly income of a store as a function of the price of its main product is described by I(x) = -2x² + 100x.",
                "answer": "Quadratic function",
            },
            {
                "statement": "The trajectory of water in an ornamental fountain follows the parabolic equation f(x) = -x² + 6x.",
                "answer": "Quadratic function",
            },
            {
                "statement": "The total area of a square lot as a function of the length of its side increased is modeled by A(l) = (l + 4)².",
                "answer": "Quadratic function",
            },
            {
                "statement": "The net profit of a company as a function of advertising investment x is given by G(x) = -3x² + 120x - 400.",
                "answer": "Quadratic function",
            },
            {
                "statement": "The fuel consumption of a car as a function of its constant speed is modeled using C(v) = 0.05v² - 4v + 90.",
                "answer": "Quadratic function",
            },
            {
                "statement": "The electrical power dissipated in a circuit as a function of current is calculated using P(i) = 4i².",
                "answer": "Quadratic function",
            },
            {
                "statement": "The area of a rectangular lot as a function of width x is modeled by A(x) = x(15 - x).",
                "answer": "Quadratic function",
            },
            {
                "statement": "The height of a projectile as a function of time is given by h(t) = -4.9t² + 20t.",
                "answer": "Quadratic function",
            },
            {
                "statement": "The revenue of a company from selling a product at price x is described by I(x) = -3x² + 120x.",
                "answer": "Quadratic function",
            },
            {
                "statement": "The trajectory of a soccer ball when kicked is represented by f(x) = -0.1x² + 2x.",
                "answer": "Quadratic function",
            },
            {
                "statement": "The total production cost of a company depends on the number of batches x according to C(x) = 2x² - 10x + 50.",
                "answer": "Quadratic function",
            },
            {
                "statement": "The total area of a square whose side increases by 5 units is expressed as A(x) = (x + 5)².",
                "answer": "Quadratic function",
            },
            {
                "statement": "The net profit of an airline as a function of ticket price is modeled by G(p) = -4p² + 240p - 1000.",
                "answer": "Quadratic function",
            },
            {
                "statement": "The gasoline consumption of a truck as a function of its speed is governed by C(v) = 0.02v² - 1.5v + 80.",
                "answer": "Quadratic function",
            },
            {
                "statement": "The power dissipated in a resistor as a function of current is given by P(i) = 5i² + 2i.",
                "answer": "Quadratic function",
            },
            {
                "statement": "The number of connections in a network as a function of active nodes is modeled by f(n) = n(n - 1) / 2.",
                "answer": "Quadratic function",
            },
            {
                "statement": "The depth of a crater as a function of distance from the center is approximated by d(x) = x² - 9.",
                "answer": "Quadratic function",
            },
            {
                "statement": "The profit of a store depends on advertising investment x via the function B(x) = -x² + 14x - 24.",
                "answer": "Quadratic function",
            },
        ],
        "Cubic function": [
            {
                "statement": "The volume of an open box is calculated with V(x) = x(18 - 2x)², where x represents the cut on each corner.",
                "answer": "Cubic function",
            },
            {
                "statement": "The volume of a cube is expressed as V(l) = l³, where l is the edge length.",
                "answer": "Cubic function",
            },
            {
                "statement": "The growth of a physical phenomenon is modeled with the polynomial function f(x) = 2x³ - 5x² + x - 3.",
                "answer": "Cubic function",
            },
            {
                "statement": "The deformation of a beam under a certain load is governed by D(x) = x³ - 3x.",
                "answer": "Cubic function",
            },
            {
                "statement": "The accumulated profit of a technology startup during its first years is represented by B(t) = t³ - 6t² + 9t.",
                "answer": "Cubic function",
            },
            {
                "statement": "The flow rate of a fluid through a special conduit varies with radius according to Q(r) = 4r³.",
                "answer": "Cubic function",
            },
            {
                "statement": "The volumetric expansion of a material with respect to temperature is approximated by V(T) = 0.5T³ + 10.",
                "answer": "Cubic function",
            },
            {
                "statement": "A complex cost function for mass manufacturing is given by C(q) = q³ - 4q² + 20q + 150.",
                "answer": "Cubic function",
            },
            {
                "statement": "The volume of a box with corner cuts of size x is modeled by V(x) = x(10 - 2x)(15 - 2x).",
                "answer": "Cubic function",
            },
            {
                "statement": "The growth of the volume of a uniformly inflated spherical balloon is related to its radius by V(r) = (4/3)πr³.",
                "answer": "Cubic function",
            },
            {
                "statement": "The accumulated gain of a corporation in its first quarters is modeled by G(t) = t³ - 4t² + 5t.",
                "answer": "Cubic function",
            },
            {
                "statement": "The deflection of a structure under cubic load is described by D(x) = 2x³ - 6x.",
                "answer": "Cubic function",
            },
            {
                "statement": "The cost of manufacturing components on a large scale follows the polynomial function C(x) = 0.5x³ - 3x² + 10x.",
                "answer": "Cubic function",
            },
            {
                "statement": "The volume of a special cubic container is expressed as V(x) = (x + 2)³, where x is the initial base.",
                "answer": "Cubic function",
            },
            {
                "statement": "The flow of a viscous liquid through a pipe depends on the radius according to Q(r) = 3r³ - r.",
                "answer": "Cubic function",
            },
            {
                "statement": "The thermal volumetric expansion of a polymer is governed by V(T) = 0.1T³ + 2T.",
                "answer": "Cubic function",
            },
            {
                "statement": "A complex business profit function is defined by B(q) = q³ - 12q² + 36q.",
                "answer": "Cubic function",
            },
            {
                "statement": "The variation in altitude of an aircraft during a specific maneuver follows f(t) = t³ - 3t² + 2.",
                "answer": "Cubic function",
            },
            {
                "statement": "The dynamic behavior of a mechanical system is modeled by the polynomial function S(x) = 4x³ - x.",
                "answer": "Cubic function",
            },
            {
                "statement": "The volume of a pyramid with variable base is described by V(x) = (1/3)x³.",
                "answer": "Cubic function",
            },
        ],
        "Rational function": [
            {
                "statement": "The average cost per unit of a product is described by C(x) = 120/(x + 4) + 6.",
                "answer": "Rational function",
            },
            {
                "statement": "The average speed of a trip depends on distance and time by v = 150/(t + 5).",
                "answer": "Rational function",
            },
            {
                "statement": "The concentration of a medication in the bloodstream over time is modeled by C(t) = 50 / (t² + 1).",
                "answer": "Rational function",
            },
            {
                "statement": "The time several workers need to build a wall is expressed by T(x) = 40/x, where x is the number of workers.",
                "answer": "Rational function",
            },
            {
                "statement": "The equivalent electrical resistance in parallel of two components is governed by R(x) = 10x / (x + 10).",
                "answer": "Rational function",
            },
            {
                "statement": "The perceived light intensity at a certain distance from a source is modeled by I(d) = 500 / d².",
                "answer": "Rational function",
            },
            {
                "statement": "The percentage of impurities in a purification tank is calculated with P(t) = (20t + 5) / (t + 2).",
                "answer": "Rational function",
            },
            {
                "statement": "The efficiency ratio of an industrial machine is described by E(x) = (100x - 5) / (x + 1).",
                "answer": "Rational function",
            },
            {
                "statement": "The average cost per item of a production is modeled by C(x) = 500 / (x + 10).",
                "answer": "Rational function",
            },
            {
                "statement": "The concentration of a drug in the body over time is described by f(t) = 100 / (t + 2).",
                "answer": "Rational function",
            },
            {
                "statement": "The time needed to finish a job as a function of the number of workers is governed by T(x) = 120 / x.",
                "answer": "Rational function",
            },
            {
                "statement": "The average speed of a trip of fixed distance is calculated by v(t) = 300 / (t + 1).",
                "answer": "Rational function",
            },
            {
                "statement": "The electrical resistance in a parallel circuit is expressed as R(x) = 15x / (x + 5).",
                "answer": "Rational function",
            },
            {
                "statement": "The percentage of purity of a chemical substance mixed is modeled by P(t) = (50t + 10) / (t + 5).",
                "answer": "Rational function",
            },
            {
                "statement": "The perceived light intensity at distance d is modeled by I(d) = 1000 / d².",
                "answer": "Rational function",
            },
            {
                "statement": "The efficiency of an industrial machine as a function of hours used is described by E(x) = 100x / (x + 20).",
                "answer": "Rational function",
            },
            {
                "statement": "The ratio of profits to costs of a company is modeled by R(x) = (200x + 50) / (x + 2).",
                "answer": "Rational function",
            },
            {
                "statement": "The cooling temperature of a liquid in an open container follows T(t) = 80 / (t + 1) + 20.",
                "answer": "Rational function",
            },
            {
                "statement": "The average points per game of a player is modeled by P(x) = (15x + 5) / x.",
                "answer": "Rational function",
            },
            {
                "statement": "The distortion of an audio signal is represented by S(x) = 50 / (x² + 4).",
                "answer": "Rational function",
            },
        ],
        "Exponential function": [
            {
                "statement": "A colony of bacteria doubles its population every hour, so P(t) = 5·2^t.",
                "answer": "Exponential function",
            },
            {
                "statement": "The money in an investment account with continuous compound interest grows according to A(t) = 1000·e^(0.05t).",
                "answer": "Exponential function",
            },
            {
                "statement": "The depreciation of the value of machinery decreases by 15% each year, modeled as V(t) = 50000·(0.85)^t.",
                "answer": "Exponential function",
            },
            {
                "statement": "The amount of radioactive material follows a decomposition process where M(t) = 200·(1/2)^(t/3).",
                "answer": "Exponential function",
            },
            {
                "statement": "The spread of a rumor on a social network follows explosive growth given by R(d) = 10·3^d.",
                "answer": "Exponential function",
            },
            {
                "statement": "Atmospheric pressure decreases exponentially as altitude h increases, expressed as P(h) = 1013·e^(-0.12h).",
                "answer": "Exponential function",
            },
            {
                "statement": "The number of active users of a web platform triples each month according to N(m) = 500·3^m.",
                "answer": "Exponential function",
            },
            {
                "statement": "A chemical reaction doubles its catalysis rate every 10 degrees of temperature, modeled by V(T) = 2^(T/10).",
                "answer": "Exponential function",
            },
            {
                "statement": "A population of insects triples each week, modeled by P(t) = 100·3^t.",
                "answer": "Exponential function",
            },
            {
                "statement": "The growth of an investment with annual compound interest is described by A(t) = 5000·(1.06)^t.",
                "answer": "Exponential function",
            },
            {
                "statement": "The radioactive decay of an isotope follows M(t) = 1000·(0.5)^(t/5).",
                "answer": "Exponential function",
            },
            {
                "statement": "The number of downloads of an application grows by 20% daily, modeled by D(d) = 200·(1.2)^d.",
                "answer": "Exponential function",
            },
            {
                "statement": "Atmospheric pressure at different heights is calculated with P(h) = 1000·e^(-0.15h).",
                "answer": "Exponential function",
            },
            {
                "statement": "The spread of a computer virus on a network follows the function V(t) = 50·2^t.",
                "answer": "Exponential function",
            },
            {
                "statement": "The annual depreciation of a car is modeled by the value V(t) = 25000·(0.80)^t.",
                "answer": "Exponential function",
            },
            {
                "statement": "The amount of bacteria in a culture decreases by half every 3 hours according to C(t) = 400·(1/2)^(t/3).",
                "answer": "Exponential function",
            },
            {
                "statement": "The number of subscribers to a streaming channel grows exponentially with N(m) = 1000·(1.05)^m.",
                "answer": "Exponential function",
            },
            {
                "statement": "The intensity of light passing through successive glass layers is governed by I(x) = 100·(0.7)^x.",
                "answer": "Exponential function",
            },
            {
                "statement": "The increase in temperature of a chemical reactor is modeled with T(t) = 25·e^(0.1t).",
                "answer": "Exponential function",
            },
            {
                "statement": "The amount of energy released in a nuclear reaction follows E(t) = 500·3^(0.5t).",
                "answer": "Exponential function",
            },
        ],
        "Absolute value function": [
            {
                "statement": "The distance of a point from zero is modeled by d(x) = |x - 3|.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The margin of error allowed in the manufacture of a metal part is calculated using E(x) = |x - 10|.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The thermal variation relative to an ideal temperature of 22 degrees is represented by f(T) = |T - 22|.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The absolute deviation of sales data from the mean is defined by D(x) = |x - 150|.",
                "answer": "Absolute value function",
            },
            {
                "statement": "A sensor measures the symmetric potential difference using V(x) = 3|x| - 5.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The height of a ball's bounce symmetric with respect to its fall axis is modeled by h(t) = -|t - 2| + 4.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The deviation cost of a delivery route is calculated as a function of extra kilometers as C(x) = 15|x - 5|.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The absolute gain or loss in the stock market for a specific asset is described by G(x) = |2x - 10|.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The allowable deviation in cutting a metal plate is described by D(x) = |x - 5|.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The distance of a vehicle from a reference post is modeled by d(t) = |2t - 10|.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The variation in ambient temperature relative to the ideal 20 degrees is represented by f(T) = |T - 20|.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The absolute error in measuring a length is calculated using E(x) = |x - 100|.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The symmetric gain or loss of a stock asset is modeled by G(x) = |3x - 15|.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The height of a symmetric bounce of a ball is given by h(t) = -|t - 4| + 5.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The additional cost for exceeding speed limits is modeled by C(v) = 50|v - 80|.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The symmetric position of an oscillating particle relative to the origin is described by s(t) = |t - 6| - 2.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The tolerance margin in filling soda bottles is modeled by M(x) = |x - 500|.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The absolute variation in blood pressure during a medical exam is modeled by P(x) = |x - 120|.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The deviation cost of a transport route is calculated by C(x) = 20|x - 10|.",
                "answer": "Absolute value function",
            },
            {
                "statement": "The symmetric difference of two related variables is represented by f(x) = |x + 3|.",
                "answer": "Absolute value function",
            },
        ],
    }

    def create_options(correct_answer):
        distractors = [func_type for func_type in FUNCTION_TYPES if func_type != correct_answer]
        options = random.sample(distractors, 3) + [correct_answer]
        random.shuffle(options)
        return options

    if target_type == "All":
        questions = []
        for func_type, item_list in templates.items():
            for item in item_list:
                questions.append(
                    {
                        "type": func_type,
                        **item,
                        "options": create_options(item["answer"]),
                    }
                )
        random.shuffle(questions)
        return questions[:amount]

    available_questions = templates.get(target_type, [])
    if not available_questions:
        return []

    generated_questions = []
    for _ in range(amount):
        item = random.choice(available_questions)
        generated_questions.append(
            {
                "type": target_type,
                **item,
                "options": create_options(item["answer"]),
            }
        )

    return generated_questions


# ==========================================================
#  INITIAL STATE
# ==========================================================
if "view" not in st.session_state:
    st.session_state.view = "start"

if "game" not in st.session_state:
    st.session_state.game = None  # will store m1, b1, m2, b2, t, d1, d2, winner

if "launch" not in st.session_state:
    st.session_state.launch = None  # quadratic function game

if "box" not in st.session_state:
    st.session_state.box = None  # cubic function game

if "price_war" not in st.session_state:
    st.session_state.price_war = None  # rational function game

st.title("📊 Options Menu")

# ==========================================================
#  MENU
# ==========================================================
row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)

with row1_col1:
    if st.button("1️⃣ Constant"):
        st.session_state.view = "constant"

with row1_col2:
    if st.button("2️⃣ Linear (game)"):
        st.session_state.view = "game"
        st.session_state.game = None  # new game when entering

with row1_col3:
    if st.button("3️⃣ Quadratic"):
        st.session_state.view = "quadratic"

with row1_col4:
    if st.button("4️⃣ Cubic"):
        st.session_state.view = "cubic"

row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    if st.button("5️⃣ Rational"):
        st.session_state.view = "rational"

with row2_col2:
    if st.button("6️⃣ Problems (AI)"):
        st.session_state.view = "ai"

with row2_col3:
    if st.button("7️⃣ Graphs (Desmos)"):
        st.session_state.view = "desmos"

st.divider()

# ==========================================================
#  OPTION 1: CONSTANT FUNCTION
# ==========================================================
if st.session_state.view == "constant":
    st.subheader("📈 Constant function")

    value = st.number_input("Give me a number", value=0.0, step=1.0)

    if st.button("Graph"):
        try:
            fig = plt.figure(figsize=(8, 6))
            x = [-10, 10]
            y = [value, value]

            plt.plot(x, y, label=f"y = {value}")
            plt.title("Constant function")
            plt.xlabel("x-axis")
            plt.ylabel("y-axis")
            plt.grid(True)
            plt.legend()

            st.pyplot(fig)
            plt.close(fig)
        except Exception as ex:
            st.error(f"❌ Unexpected error: {ex}")

# ==========================================================
#  OPTION 2: LINEAR FUNCTION GAME
# ==========================================================
elif st.session_state.view == "game":
    st.subheader("🏁 Function race 🏁")

    if st.session_state.game is None:
        m1 = random.randint(2, 8)
        b1 = random.randint(0, 10)
        m2 = random.randint(2, 8)
        b2 = random.randint(0, 10)
        t = random.randint(-10, 10)

        d1 = m1 * t + b1
        d2 = m2 * t + b2

        if d1 > d2:
            winner = "red"
        elif d2 > d1:
            winner = "blue"
        else:
            winner = "tie"

        st.session_state.game = dict(
            m1=m1, b1=b1, m2=m2, b2=b2, t=t, d1=d1, d2=d2, winner=winner
        )

    j = st.session_state.game

    st.write("🏁 WELCOME TO THE MATHEMATICAL RACE 🏁")
    st.write("Today two cars will compete using linear functions:")
    st.write("Distance = speed × time + initial advantage")
    st.write("Mathematical form: y = mx + b")
    st.write(f"Red🚗: y = {j['m1']}x + {j['b1']}")
    st.write(f"Blue🚙: y = {j['m2']}x + {j['b2']}")
    st.write(f"Time t: {j['t']}")

    col1, col2, col3 = st.columns(3)
    choice = None
    with col1:
        if st.button("Red"):
            choice = "red"
    with col2:
        if st.button("Blue"):
            choice = "blue"
    with col3:
        if st.button("Tie"):
            choice = "tie"

    if choice:
        if choice == j["winner"]:
            st.success("🎉 Correct")
        else:
            st.error(f"❌ It was: {j['winner']}")
        st.write(f"Red: {j['d1']} | Blue: {j['d2']}")

    if st.button("🔄 Reset"):
        st.session_state.game = None
        st.rerun()

# ==========================================================
#  OPTION 3: QUADRATIC FUNCTION GAME — LAUNCH RACE
# ==========================================================
elif st.session_state.view == "quadratic":
    st.subheader("🚀 Launch race 🚀")

    if st.session_state.launch is None:
        possible_a = [round(v, 1) for v in np.arange(-10.0, 10.5, 0.5) if v != 0]
        a1 = random.choice(possible_a)
        b1 = random.randint(-10, 20)
        c1 = random.randint(-10, 10)

        a2 = random.choice(possible_a)
        b2 = random.randint(-10, 20)
        c2 = random.randint(-10, 10)

        t = random.randint(-10, 10)

        h1 = a1 * t**2 + b1 * t + c1
        h2 = a2 * t**2 + b2 * t + c2

        if h1 > h2:
            winner = "object1"
        elif h2 > h1:
            winner = "object2"
        else:
            winner = "tie"

        st.session_state.launch = dict(
            a1=a1, b1=b1, c1=c1, a2=a2, b2=b2, c2=c2, t=t, h1=h1, h2=h2, winner=winner
        )

    j = st.session_state.launch

    st.write("🎯 Two objects follow a trajectory that can be modeled by a quadratic function.")
    st.write("The general form is y = ax² + bx + c. The value of a can vary widely from -10 to 10.")
    st.write("If a > 0, the parabola opens upward; if a < 0, it opens downward.")
    st.write("The height of each object depends on the value of t:")
    st.write(f"🔴 Object 1: h(t) = {j['a1']}t² + ({j['b1']})t + ({j['c1']})")
    st.write(f"🔵 Object 2: h(t) = {j['a2']}t² + ({j['b2']})t + ({j['c2']})")
    st.write(f"⏱️ Time/Value t: {j['t']}")
    st.write("Which object reaches a higher value at that instant?")

    col1, col2, col3 = st.columns(3)
    choice = None
    with col1:
        if st.button("🔴 Object 1"):
            choice = "object1"
    with col2:
        if st.button("🔵 Object 2"):
            choice = "object2"
    with col3:
        if st.button("Tie"):
            choice = "tie"

    if choice:
        if choice == j["winner"]:
            st.success("🎉 Correct")
        else:
            st.error(f"❌ It was: {j['winner']}")
        st.write(f"Value Object 1: {j['h1']:.2f} | Value Object 2: {j['h2']:.2f}")

        x = np.linspace(-12, 12, 400)
        y1 = j["a1"] * x**2 + j["b1"] * x + j["c1"]
        y2 = j["a2"] * x**2 + j["b2"] * x + j["c2"]

        fig = plt.figure(figsize=(8, 6))
        plt.plot(x, y1, color="red", label="Object 1")
        plt.plot(x, y2, color="blue", label="Object 2")
        plt.scatter([j["t"]], [j["h1"]], color="red", zorder=5)
        plt.scatter([j["t"]], [j["h2"]], color="blue", zorder=5)
        plt.axvline(j["t"], color="gray", linestyle="--", linewidth=1)
        plt.axhline(0, color="black", linewidth=0.8)
        plt.title("Trajectory / Function of the two objects")
        plt.xlabel("Time/Variable t")
        plt.ylabel("Value h(t)")
        plt.grid(True)
        plt.legend()
        st.pyplot(fig)
        plt.close(fig)

    if st.button("🔄 New launch"):
        st.session_state.launch = None
        st.rerun()

# ==========================================================
#  OPTION 4: CUBIC FUNCTION GAME — THE BOX CHALLENGE
# ==========================================================
elif st.session_state.view == "cubic":
    st.subheader("📈 Cubic function challenge")

    if st.session_state.box is None:
        a = random.choice([v for v in range(-10, 11) if v != 0])
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        d = random.randint(-10, 10)
        x = random.randint(-10, 10)
        result = a * x**3 + b * x**2 + c * x + d
        st.session_state.box = dict(a=a, b=b, c=c, d=d, x=x, result=result)

    j = st.session_state.box

    st.write("A cubic function has the form:")
    st.latex(r"f(x)=ax^3+bx^2+cx+d,\quad a\ne 0")
    st.write(
        f"Substitute x = {j['x']} into f(x) = ({j['a']})x³ + ({j['b']})x² + "
        f"({j['c']})x + ({j['d']})."
    )

    response = st.number_input(
        "What is the value of f(x)?", step=1.0, format="%.2f", key="response_cubic"
    )

    if st.button("✅ Check cubic function"):
        st.write(
            f"Substitution: f({j['x']}) = ({j['a']})({j['x']})³ + "
            f"({j['b']})({j['x']})² + ({j['c']})({j['x']}) + ({j['d']})"
        )
        st.write(f"Correct result: f({j['x']}) = {j['result']}")
        if abs(response - j["result"]) < 0.01:
            st.success("🎉 Correct. You substituted x correctly.")
        else:
            st.error("❌ Review the powers, signs, and substitution of x.")

        xs = np.linspace(-12, 12, 400)
        ys = j["a"] * xs**3 + j["b"] * xs**2 + j["c"] * xs + j["d"]

        fig = plt.figure(figsize=(8, 6))
        plt.plot(xs, ys, label="f(x) = ax³ + bx² + cx + d")
        plt.scatter([j["x"]], [j["result"]], color="red", zorder=5, label="Calculated value")
        plt.title("Graph of the cubic function")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.grid(True)
        plt.legend()
        st.pyplot(fig)
        plt.close(fig)

    if st.button("🔄 New sheet"):
        st.session_state.box = None
        st.rerun()

# ==========================================================
#  OPTION 5: RATIONAL FUNCTION GAME — PRICE WAR
# ==========================================================
elif st.session_state.view == "rational":
    st.subheader("💰 Price war 💰")

    if st.session_state.price_war is None:
        a1 = random.randint(50, 150)
        b1 = random.randint(1, 5)
        c1 = random.randint(3, 10)

        a2 = random.randint(50, 150)
        b2 = random.randint(1, 5)
        c2 = random.randint(3, 10)

        x = random.randint(5, 30)

        cost1 = a1 / (x + b1) + c1
        cost2 = a2 / (x + b2) + c2

        if cost1 < cost2:
            winner = "business1"
        elif cost2 < cost1:
            winner = "business2"
        else:
            winner = "tie"

        st.session_state.price_war = dict(
            a1=a1, b1=b1, c1=c1, a2=a2, b2=b2, c2=c2, x=x, cost1=cost1, cost2=cost2, winner=winner
        )

    j = st.session_state.price_war

    st.write("🏭 Two businesses produce the same item. The unit cost is modeled by a rational function.")
    st.write("The general form is C(x) = a/(x + b) + c, where a, b, and c are constants.")
    st.write("As x increases, the term a/(x + b) decreases and the cost approaches c. That is why the graph has a horizontal asymptote.")
    st.write("Example: C(x) = 120/(x + 4) + 6. If x = 10, then C(10) = 120/14 + 6 ≈ 14.57.")
    st.write(f"🏪 Business 1: cost(x) = {j['a1']}/(x + {j['b1']}) + {j['c1']}")
    st.write(f"🏬 Business 2: cost(x) = {j['a2']}/(x + {j['b2']}) + {j['c2']}")
    st.write(f"📦 Production: x = {j['x']} units")
    st.write("Substitute x into each formula and calculate the unit cost.")
    response_cost1 = st.number_input(
        "Cost of Business 1", min_value=0.0, step=0.01, format="%.2f", key="response_cost1"
    )
    response_cost2 = st.number_input(
        "Cost of Business 2", min_value=0.0, step=0.01, format="%.2f", key="response_cost2"
    )

    if st.button("✅ Check costs"):
        st.write(
            f"Substitution 1: C({j['x']}) = {j['a1']}/({j['x']} + {j['b1']}) + {j['c1']}"
        )
        st.write(
            f"Substitution 2: C({j['x']}) = {j['a2']}/({j['x']} + {j['b2']}) + {j['c2']}"
        )
        if abs(response_cost1 - j["cost1"]) < 0.01 and abs(response_cost2 - j["cost2"]) < 0.01:
            st.success("🎉 Correct. You substituted x correctly in both functions.")
        else:
            st.error("❌ Check the parentheses and division in one of the substitutions.")
        st.write(f"Correct results: Cost 1 = {j['cost1']:.2f} | Cost 2 = {j['cost2']:.2f}")

        x_vals = np.linspace(1, 50, 300)
        y1 = j["a1"] / (x_vals + j["b1"]) + j["c1"]
        y2 = j["a2"] / (x_vals + j["b2"]) + j["c2"]

        fig = plt.figure(figsize=(8, 6))
        plt.plot(x_vals, y1, color="orange", label="Business 1")
        plt.plot(x_vals, y2, color="purple", label="Business 2")
        plt.axhline(j["c1"], color="orange", linestyle="--", linewidth=1, label=f"Asymptote Business 1: y={j['c1']}")
        plt.axhline(j["c2"], color="purple", linestyle="--", linewidth=1, label=f"Asymptote Business 2: y={j['c2']}")
        plt.scatter([j["x"]], [j["cost1"]], color="orange", zorder=5)
        plt.scatter([j["x"]], [j["cost2"]], color="purple", zorder=5)
        plt.axvline(j["x"], color="gray", linestyle="--", linewidth=1)
        plt.title("Unit cost according to production")
        plt.xlabel("Units produced (x)")
        plt.ylabel("Unit cost")
        plt.grid(True)
        plt.legend()
        st.pyplot(fig)
        plt.close(fig)

    if st.button("🔄 New round"):
        st.session_state.price_war = None
        st.rerun()

# ==========================================================
#  OPTION 6: PROBLEMS GENERATED WITH AI
# ==========================================================
elif st.session_state.view == "ai":
    st.subheader("🤖 Generate problems")

    ai_tab, quiz_tab = st.tabs(["Problems with AI", "Identify the function"])

    with ai_tab:
        final_options = ["All"] + FUNCTION_TYPES
        func_type = st.selectbox("Choose the type of function", final_options)
        amount = st.slider("Number of exercises", min_value=3, max_value=10, value=5)

        if st.button("Generate with AI"):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY_3"])
                model = genai.GenerativeModel("gemini-3-flash-preview")

                prompt = (
                    f"Generate {amount} real-life situations that can be modeled "
                    f"with a {func_type.lower()}. "
                    "Each situation must be well contextualized (a clear scenario, with concrete and coherent data: names, quantities, units), "
                    "written clearly for middle-school students, and must ask an explicit final question that the student should solve by formulating the corresponding function. "
                    "Do not include answers or the problem-solving process, only the statement. "
                    "Number each situation from 1 to "
                    f"{amount}. "
                    "Write in plain text, without asterisks, without emojis, without markdown formatting."
                )
                result = model.generate_content(prompt)
                st.write(result.text)
            except Exception as error:
                st.error(f"Error: {error}")

    with quiz_tab:
        quiz_type = st.selectbox("Select the type to practice", ["All"] + FUNCTION_TYPES)
        quiz_amount = st.slider("Number of questions", min_value=3, max_value=8, value=5, key="quiz_amount")

        if st.button("Generate multiple-choice questions", key="generate_quiz"):
            st.session_state.quiz_identification = generate_identification_questions(quiz_type, quiz_amount)
            st.session_state.quiz_answers = {}

        if "quiz_identification" in st.session_state and st.session_state.quiz_identification:
            questions = st.session_state.quiz_identification

            for i, question in enumerate(questions):
                st.markdown(f"### Question {i + 1}")
                st.write(question["statement"])

                answer = st.radio(
                    "Select the correct answer:",
                    question["options"],
                    index=None,
                    key=f"question_{i}",
                )

                if answer is not None:
                    st.session_state.quiz_answers[i] = answer

            if st.button("Check answers", key="check_quiz"):
                correct_answers = 0
                total = len(questions)

                for i, question in enumerate(questions):
                    user_answer = st.session_state.quiz_answers.get(i)
                    if user_answer == question["answer"]:
                        correct_answers += 1

                st.success(f"Your result: {correct_answers}/{total} correct answers.")

                for i, question in enumerate(questions):
                    user_answer = st.session_state.quiz_answers.get(i)
                    status = "✅ Correct" if user_answer == question["answer"] else "❌ Incorrect"
                    st.write(f"Question {i + 1}: {status}. Correct answer: {question['answer']}")

                if correct_answers == total:
                    st.balloons()
                else:
                    st.info("Generate another set of questions to practice identifying function types.")
        else:
            st.info("Generate a set of questions to practice identifying function types.")

# ==========================================================
#  OPTION 7: GRAPHS WITH DESMOS
# ==========================================================
if st.session_state.view == "desmos":
    st.subheader("📐 Graphs with Desmos")

    desmos_html = """
    <div id="calculator" style="width: 100%; height: 500px;"></div>
    <script src="https://www.desmos.com/api/v1.12/calculator.js?apiKey=9bda5869329f43429dddd48875ee6168"></script>
    <script>
    var elt = document.getElementById('calculator');
    var calculator = Desmos.GraphingCalculator(elt);

    // Definition of expressions in Desmos
    calculator.setExpression({id: 'graph1', latex: 'y = x^2'});
    calculator.setExpression({id: 'slider', latex: 'a = 3'});
    calculator.setExpression({id: 'graph2', latex: 'y = a * x'});
    </script>
    """
    components.html(desmos_html, height=550)
