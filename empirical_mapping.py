import numpy as np
from scipy.ndimage import gaussian_filter1d
from typing import Tuple, List

def extract_field_variable(data: np.ndarray, normalize: bool = True) -> np.ndarray:
    """
    Extracts and optionally normalizes the symbolic field Ψ(x) from raw data.
    """
    psi = data.copy().astype(float)
    if normalize:
        psi -= np.min(psi)
        psi /= np.max(psi)
    return psi

def calibrate_axis(x_data: np.ndarray, scale: float) -> np.ndarray:
    """
    Converts data indices to physical units using a known scale.
    """
    return x_data * scale

def filter_noise(psi: np.ndarray, sigma: float = 1.0) -> np.ndarray:
    """
    Applies Gaussian filtering to reduce high-frequency noise.
    """
    return gaussian_filter1d(psi, sigma)

def compute_noise_floor(psi: np.ndarray, method: str = "std", window: int = 10) -> float:
    """
    Estimates noise floor for drift thresholding.
    """
    if method == "std":
        return np.std(psi[:window])
    elif method == "mad":
        return np.median(np.abs(psi[:window] - np.median(psi[:window])))
    else:
        raise ValueError("Invalid method. Choose 'std' or 'mad'.")

def drift_threshold(noise_floor: float, k: float = 2.0) -> float:
    """
    Calculates drift threshold as noise floor + k * std.
    """
    return noise_floor * (1 + k)

def mask_artifacts(dpsi: np.ndarray, threshold: float) -> np.ndarray:
    """
    Masks regions with drift below threshold as artifacts.
    """
    return (dpsi >= threshold).astype(int)

def compute_delta_psi(psi: np.ndarray) -> np.ndarray:
    """
    Computes symbolic drift δΨ(x) across the field.
    """
    return np.abs(np.diff(psi, prepend=psi[0]))

def compute_fidelity(dpsi: np.ndarray) -> np.ndarray:
    """
    Computes fidelity F(x) from drift.
    """
    return 1.0 - dpsi

def compute_entropy(dpsi: np.ndarray, fidelity: np.ndarray) -> np.ndarray:
    """
    Computes collapse entropy S(x).
    """
    return np.log(1 + dpsi + (1 - fidelity))

def apply_ciz(dpsi: np.ndarray, fidelity: np.ndarray, entropy: np.ndarray) -> np.ndarray:
    """
    Applies Collapse Intercept Zone (CIZ) conditions.
    """
    return (dpsi < 0.29) & (fidelity > 0.21) & (entropy < 3.5)

def calibrate_and_extract(data: np.ndarray, scale: float = 1.0, sigma: float = 1.0, k: float = 2.0) -> dict:
    """
    Full pipeline for calibrating and extracting RCFT variables from raw data.
    """
    psi = extract_field_variable(data)
    psi_smoothed = filter_noise(psi, sigma=sigma)
    x_phys = calibrate_axis(np.arange(len(psi_smoothed)), scale)
    dpsi = compute_delta_psi(psi_smoothed)
    fidelity = compute_fidelity(dpsi)
    entropy = compute_entropy(dpsi, fidelity)
    noise_floor = compute_noise_floor(psi_smoothed)
    threshold = drift_threshold(noise_floor, k=k)
    artifact_mask = mask_artifacts(dpsi, threshold)
    ciz_mask = apply_ciz(dpsi, fidelity, entropy)

    return {
        "x_phys": x_phys,
        "Ψ": psi_smoothed,
        "δΨ": dpsi,
        "F": fidelity,
        "S": entropy,
        "ArtifactMask": artifact_mask,
        "CIZMask": ciz_mask,
        "DriftThreshold": threshold
    }
