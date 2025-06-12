import numpy as np
import matplotlib.pyplot as plt
from calibration.empirical_mapping import calibrate_and_extract

def run_symbolic_simulation(raw_data: np.ndarray, scale: float = 1.0, sigma: float = 1.0, k: float = 2.0):
    """
    Run symbolic collapse field simulation from raw data using ULRC calibration.
    """
    results = calibrate_and_extract(raw_data, scale=scale, sigma=sigma, k=k)

    x = results["x_phys"]
    psi = results["Ψ"]
    dpsi = results["δΨ"]
    f = results["F"]
    s = results["S"]
    ciz = results["CIZMask"]
    artifact = results["ArtifactMask"]

    # Plotting results
    plt.figure(figsize=(12, 8))

    plt.subplot(4, 1, 1)
    plt.plot(x, psi, label='Ψ(x)')
    plt.title("Symbolic Field Ψ(x)")
    plt.grid(True)

    plt.subplot(4, 1, 2)
    plt.plot(x, dpsi, label='δΨ(x)', color='orange')
    plt.axhline(results["DriftThreshold"], color='red', linestyle='--', label='Drift Threshold')
    plt.title("Symbolic Drift δΨ(x)")
    plt.grid(True)

    plt.subplot(4, 1, 3)
    plt.plot(x, f, label='Fidelity F(x)', color='green')
    plt.plot(x, s, label='Entropy S(x)', color='purple')
    plt.title("Fidelity and Entropy")
    plt.legend()
    plt.grid(True)

    plt.subplot(4, 1, 4)
    plt.plot(x, ciz, label='Alive (CIZ)', color='blue')
    plt.plot(x, artifact, label='Artifact Mask', color='gray', linestyle='--')
    plt.title("Collapse Intercept Zone (CIZ) & Artifact Detection")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    return results
