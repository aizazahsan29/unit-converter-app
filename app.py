import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="Unit Converter", page_icon="🔄", layout="centered")
st.title("🔄 Unit Converter")
st.caption("Simple, fast conversions for Length, Mass, Volume, and Temperature.")

# ---------- Conversion data ----------
# Length -> base meter
LENGTH_TO_M = {
    "km": 1000.0, "m": 1.0, "cm": 0.01, "mm": 0.001,
    "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344,
}
# Mass -> base kilogram
MASS_TO_KG = {
    "t (metric tonne)": 1000.0, "kg": 1.0, "g": 0.001, "mg": 1e-6,
    "lb": 0.45359237, "oz": 0.028349523125,
}
# Volume -> base liter
VOLUME_TO_L = {
    "L": 1.0, "mL": 0.001, "gal_us": 3.785411784, "qt_us": 0.946352946,
    "pt_us": 0.473176473, "cup_us": 0.2365882365, "fl_oz_us": 0.0295735295625,
}
TEMP_UNITS = ["Celsius", "Fahrenheit", "Kelvin"]

CATEGORIES = ["Length", "Mass", "Volume", "Temperature"]
CATEGORY_MAP = {
    "Length": LENGTH_TO_M,
    "Mass": MASS_TO_KG,
    "Volume": VOLUME_TO_L,
}

# ---------- Helpers ----------
def units_for_category(cat: str):
    return TEMP_UNITS if cat == "Temperature" else list(CATEGORY_MAP[cat].keys())

def convert_temperature(val, from_u, to_u):
    # to Celsius
    if from_u == "Celsius": c = val
    elif from_u == "Fahrenheit": c = (val - 32.0) * 5.0 / 9.0
    elif from_u == "Kelvin": c = val - 273.15
    else: return None
    # from Celsius
    if to_u == "Celsius": return c
    if to_u == "Fahrenheit": return c * 9.0 / 5.0 + 32.0
    if to_u == "Kelvin": return c + 273.15
    return None

def convert_value(category, from_unit, to_unit, value):
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    if category == "Temperature":
        return convert_temperature(x, from_unit, to_unit)
    factors = CATEGORY_MAP[category]
    base = x * factors[from_unit]      # to base
    return base / factors[to_unit]     # to target

# ---------- UI state ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- UI ----------
with st.container():
    colA, colB = st.columns(2)
    category = colA.selectbox("Category", CATEGORIES, index=0)
    precision = colB.number_input("Decimal places", min_value=0, max_value=10, value=4, step=1)

    units = units_for_category(category)
    default_from = ("m" if category == "Length" else
                    "kg" if category == "Mass" else
                    "L" if category == "Volume" else
                    "Celsius")
    default_to = ("ft" if category == "Length" else
                  "lb" if category == "Mass" else
                  "gal_us" if category == "Volume" else
                  "Fahrenheit")

    col1, col2 = st.columns([3, 1])
    from_unit = col1.selectbox("From unit", units, index=units.index(default_from) if default_from in units else 0, key=f"from_{category}")
    to_unit = col1.selectbox("To unit", units, index=units.index(default_to) if default_to in units else min(1, len(units)-1), key=f"to_{category}")

    if col2.button("↔️ Swap"):
        from_unit, to_unit = to_unit, from_unit
        # re-render with swapped defaults by updating session state
        st.session_state[f"from_{category}"] = from_unit
        st.session_state[f"to_{category}"] = to_unit
        st.experimental_rerun()

    value = st.number_input("Value", value=1.0, format="%.6f")

    if st.button("Convert"):
        y = convert_value(category, from_unit, to_unit, value)
        if y is None:
            st.error("Please enter a valid number.")
        else:
            out = f"{value} {from_unit} = {round(y, precision)} {to_unit}"
            st.success(out)
            st.session_state.history.insert(0, out)

st.divider()
st.subheader("🧾 Recent conversions")
if st.session_state.history:
    for i, row in enumerate(st.session_state.history[:8], start=1):
        st.write(f"{i}. {row}")
else:
    st.caption("No conversions yet. Try one above!")

