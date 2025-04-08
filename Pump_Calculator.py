
import streamlit as st
import math

# Page setup
st.set_page_config(page_title="Pipe Head Loss Calculator", layout="centered")

# Inject custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: white;
        }
        .block-container {
            font-size: 18px;
        }
        h1, h2, h3, .stMarkdown {
            font-size: 22px !important;
        }
        label {
            font-size: 18px !important;
        }
        .blue-result {
            color: #1E90FF;
            font-weight: bold;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            border-radius: 8px;
            padding: 0.5em 1em;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

# --- Logo and Heading on Same Line ---
col1, col2 = st.columns([1, 6])
with col1:
    st.image("https://www.hungpump.com/images/340357", width=80)
with col2:
    st.markdown("### <span style='color:#1E90FF;'>HUNG PUMP</span>", unsafe_allow_html=True)

st.title("Pipe Head Loss Calculator")

st.markdown("This calculator determines the head loss (friction loss) in a pipe using the **Hazen-Williams equation**. It also includes equivalent lengths from fittings using K-values and a fixed friction factor (0.02).")

# Unit conversion factors
flow_unit_factors = {
    "m³/s": 1,
    "m³/hr": 1 / 3600,
    "GPM": 0.0000630902,
    "LPM": 0.0000166667
}
diameter_unit_factors = {
    "mm": 0.001,
    "inch": 0.0254
}
length_unit_factors = {
    "meters": 1,
    "millimeters": 0.001,
    "feet": 0.3048
}

# K-values for fittings
fitting_k = {
    "elbows90": 0.9,
    "elbows45": 0.4,
    "teeThrough": 0.3,
    "teeBranch": 1.0,
    "gateValve": 0.2,
    "globeValve": 10,
    "checkValve": 2
}

# Input section
st.header("Pipe & Flow Parameters")
flow_col1, flow_col2 = st.columns([2, 1])
flow_rate = flow_col1.number_input("Flow Rate", value=100.0)
flow_unit = flow_col2.selectbox("Flow Unit", list(flow_unit_factors.keys()))

diam_col1, diam_col2 = st.columns([2, 1])
diameter = diam_col1.number_input("Pipe Diameter", value=50.0)
diam_unit = diam_col2.selectbox("Diameter Unit", list(diameter_unit_factors.keys()))

len_col1, len_col2 = st.columns([2, 1])
length = len_col1.number_input("Pipe Length", value=100.0)
length_unit = len_col2.selectbox("Length Unit", list(length_unit_factors.keys()))

c_factor = st.number_input("Pipe Material (Hazen-Williams C-Factor)", value=150)

st.divider()

# Fittings section - vertically stacked layout
st.header("Optional Fittings")
fittings = {}
fittings["elbows90"] = st.number_input("90° Elbows", min_value=0, value=0)
fittings["elbows45"] = st.number_input("45° Elbows", min_value=0, value=0)
fittings["teeThrough"] = st.number_input("Tee (Through)", min_value=0, value=0)
fittings["teeBranch"] = st.number_input("Tee (Branch)", min_value=0, value=0)
fittings["gateValve"] = st.number_input("Gate Valves", min_value=0, value=0)
fittings["globeValve"] = st.number_input("Globe Valves", min_value=0, value=0)
fittings["checkValve"] = st.number_input("Check Valves", min_value=0, value=0)

st.divider()

# Calculate head loss
if st.button("Calculate Head Loss"):
    Q = flow_rate * flow_unit_factors[flow_unit]
    D = diameter * diameter_unit_factors[diam_unit]
    L = length * length_unit_factors[length_unit]

    if Q > 0 and D > 0:
        area = math.pi * (D ** 2) / 4
        velocity = Q / area

        total_K = sum(fittings[k] * fitting_k[k] for k in fittings)
        equiv_length = (total_K * D) / 0.02
        total_length = L + equiv_length

        head_loss = 10.67 * total_length * (Q / c_factor) ** 1.85 / D ** 4.87

        st.success("Results")
        st.markdown(f"**Flow Velocity (v):** <span class='blue-result'>{velocity:.2f} m/s</span>" if velocity >= 0.01 else f"**Flow Velocity (v):** <span class='blue-result'>{velocity:.2e} m/s</span>", unsafe_allow_html=True)
        st.markdown(f"**Head Loss (hf):** <span class='blue-result'>{head_loss:.3f} meters</span>" if head_loss >= 0.01 else f"**Head Loss (hf):** <span class='blue-result'>{head_loss:.3e} meters</span>", unsafe_allow_html=True)
        st.markdown(f"**Equivalent Length from Fittings:** <span class='blue-result'>{equiv_length:.2f} meters</span>", unsafe_allow_html=True)
    else:
        st.error("Please enter valid positive numbers for flow and diameter.")
