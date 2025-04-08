
import streamlit as st
import math

# Set light theme via config block
st.set_page_config(
    page_title="Pipe Head Loss Calculator",
    layout="centered"
)

# --- Logo and Heading Side by Side ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://www.hungpump.com/images/340357", width=150)
    st.markdown("<h2 style='color: #1E90FF; margin-top: -30px;'>HUNG PUMP</h2>", unsafe_allow_html=True)
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

# Fittings section
st.header("Optional Fittings")
cols = st.columns(7)
fittings = {
    "elbows90": cols[0].number_input("90° Elbows", min_value=0, value=0),
    "elbows45": cols[1].number_input("45° Elbows", min_value=0, value=0),
    "teeThrough": cols[2].number_input("Tee (Through)", min_value=0, value=0),
    "teeBranch": cols[3].number_input("Tee (Branch)", min_value=0, value=0),
    "gateValve": cols[4].number_input("Gate Valves", min_value=0, value=0),
    "globeValve": cols[5].number_input("Globe Valves", min_value=0, value=0),
    "checkValve": cols[6].number_input("Check Valves", min_value=0, value=0)
}

st.divider()

# Calculate head loss
if st.button("Calculate Head Loss"):
    Q = flow_rate * flow_unit_factors[flow_unit]
    D = diameter * diameter_unit_factors[diam_unit]
    L = length * length_unit_factors[length_unit]

    if Q > 0 and D > 0:
        # Velocity
        area = math.pi * (D ** 2) / 4
        velocity = Q / area

        # Equivalent length from fittings
        total_K = sum(fittings[k] * fitting_k[k] for k in fittings)
        equiv_length = (total_K * D) / 0.02
        total_length = L + equiv_length

        # Hazen-Williams head loss
        head_loss = 10.67 * total_length * (Q / c_factor) ** 1.85 / D ** 4.87

        st.success("Results")
        st.write(f"**Flow Velocity (v):** {'{:.2f}'.format(velocity)} m/s" if velocity >= 0.01 else f"**Flow Velocity (v):** {'{:.2e}'.format(velocity)} m/s")
        st.write(f"**Head Loss (hf):** {'{:.3f}'.format(head_loss)} meters" if head_loss >= 0.01 else f"**Head Loss (hf):** {'{:.3e}'.format(head_loss)} meters")
        st.write(f"**Equivalent Length from Fittings:** {equiv_length:.2f} meters")
    else:
        st.error("Please enter valid positive numbers for flow and diameter.")
