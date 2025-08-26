import streamlit as st

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(page_title="Unit Converter", page_icon="🔄", layout="centered")
st.title("🔄 Unit Converter")
st.caption("Convert between common units for Length, Mass, Volume, and Temperature.")

# -------------------------------
# Conversion data
# -------------------------------
# Length -> base: meter (m)
LENGTH_TO_M = {
    "km": 1000.0,
    "m": 1.0,
    "cm": 0.01,
    "mm": 0.001,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.344,
}

# Mass -> base: kilogram (kg)
MASS_TO_KG = {
    "t (metric tonne)": 1000.0,
    "kg": 1.0,
    "g": 0.001,
    "mg": 1e-6,
    "lb": 0.45359237,
    "oz": 0.028349523125,
}

# Volume -> base: liter (L)
VOLUME_TO_L = {
    "L": 1.0,
    "mL": 0.001,
    "gal_us": 3.785411784,
    "qt_us": 0.946352946,
    "pt_us": 0.473176473,
    "cup_us": 0.2365882365,
    "fl_oz_us": 0.0295735295625,
}

# Temperature handled with formulas
TEMP_UNITS = ["Celsius", "Fahrenheit", "Kelvin"]

CATEGORIES = ["Length", "Mass", "Volume", "Temperature"]
CATEGORY_MAP = {
    "Length": LENGTH_TO_M,
    "Mass": MASS_TO_KG,
    "Volume": VOLUME_TO_L,
}

DEFAULTS = {
    "Length": ("m", "ft"),
    "Mass": ("kg", "lb"),
    "Volume": ("L", "gal_us"),
    "Temperature": ("Celsius", "Fahrenheit"),
}

# -------------------------------
# Helper functions
# -------------------------------
def units_for_category(cat: str):
    return TEMP_UNITS if cat == "Temperature" else list(CATEGORY_MAP[cat].keys())

def convert_temperature(val, from_u, to_u):
    # to Celsius
    if from_u == "Celsius":
        c = val
    elif from_u == "Fahrenheit":
        c = (val - 32.0) * 5.0 / 9.0
    elif from_u == "Kelvin":
        c = val - 273.15
    else:
        return None
    # from Celsius
    if to_u == "Celsius":
        return c
    if to_u == "Fahrenheit":
        return c * 9.0 / 5.0 + 32.0
    if to_u == "Kelvin":
        return c + 273.15
    return None

def convert_value(category, from_unit, to_unit, value):
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None

    if category == "Temperature":
        if from_unit not in TEMP_UNITS or to_unit not in TEMP_UNITS:
            return None
        return convert_temperature(x, from_unit, to_unit)

    # multiplicative categories
    factors = CATEGORY_MAP[category]
    if from_unit not in factors or to_unit not in factors:
        return None
    base = x * factors[from_unit]      # to base
    return base / factors[to_unit]     # to target

def fmt(num, decimals):
    try:
        return f"{num:.{decimals}f}"
    except Exception:
        return str(num)

# -------------------------------
# Session state (to support swap)
# -------------------------------
if "selections" not in st.session_state:
    st.session_state.selections = {k: {"from": v[0], "to": v[1]} for k, v in DEFAULTS.items()}

# -------------------------------
# UI
# -------------------------------
col_top_a, col_top_b = st.columns([2, 1])
category = col_top_a.selectbox("Category", CATEGORIES, index=0)
precision = col_top_b.number_input("Decimal places", min_value=0, max_value=10, value=4, step=1)

units = units_for_category(category)
# Ensure stored units exist for current category; if not, reset to defaults
if st.session_state.selections[category]["from"] not in units:
    st.session_state.selections[category]["from"] = DEFAULTS[category][0]
if st.session_state.selections[category]["to"] not in units:
    st.session_state.selections[category]["to"] = DEFAULTS[category][1]

col_units, col_swap = st.columns([4, 1])
from_unit = col_units.selectbox("From unit", units, index=units.index(st.session_state.selections[category]["from"]))
to_unit = col_units.selectbox("To unit", units, index=units.index(st.session_state.selections[category]["to"]))

if col_swap.button("↔️ Swap"):
    st.session_state.selections[category]["from"], st.session_state.selections[category]["to"] = (
        to_unit, from_unit
    )
    st.rerun()

value = st.number_input("Value", value=1.0, step=1.0, format="%.6f")

if st.button("Convert"):
    # persist latest selections
    st.session_state.selections[category]["from"] = from_unit
    st.session_state.selections[category]["to"] = to_unit

    result = convert_value(category, from_unit, to_unit, value)
    if result is None:
        st.error("Please enter a valid number and make sure units/category are supported.")
    else:
        st.success(f"{fmt(value, precision)} {from_unit} = {fmt(result, precision)} {to_unit}")

st.divider()
st.caption("Tip: You can change the number of decimal places from the top-right selector.")
