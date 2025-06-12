import streamlit as st
import numpy as np
from runtime.symbolic_simulator import run_symbolic_simulation

st.set_page_config(layout="wide")
st.title("ULRC Symbolic Field Diagnostic Interface")

st.markdown("""
This interface lets you upload raw symbolic collapse field data (e.g., 1D EEG trace, spatial scan) and view:
- Field drift \(\delta\Psi\)
- Collapse zone detection (CIZ)
- Glyph viability map
""")

uploaded_file = st.file_uploader("Upload raw field data (.npy file)", type=["npy"])
scale = st.slider("Physical scale multiplier", 0.01, 10.0, 1.0)
sigma = st.slider("Smoothing (σ)", 0.1, 5.0, 1.0)
k = st.slider("Drift sensitivity (k)", 0.5, 5.0, 2.0)

if uploaded_file:
    data = np.load(uploaded_file)
    st.success("Data loaded. Running simulation...")

    results = run_symbolic_simulation(data, scale=scale, sigma=sigma, k=k)

    st.subheader("Collapse Intercept Zone Map")
    st.line_chart(results["CIZMask"])

    st.subheader("Symbolic Drift (δΨ)")
    st.line_chart(results["δΨ"])

    st.subheader("Field (Ψ) and Entropy (S)")
    st.line_chart({
        "Ψ": results["Ψ"],
        "S": results["S"]
    })

    st.markdown("**Collapse viability:** ✓ = stable zone, ✗ = outside CIZ")
    st.code(f"Viable glyph points: {np.sum(results['CIZMask'])} / {len(results['CIZMask'])}")
