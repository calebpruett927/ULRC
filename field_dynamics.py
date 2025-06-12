import numpy as np
import math
from typing import List, Dict

# Core symbolic invariants (Tier I)
def delta_psi(psi_t, psi_prev_t):
    return np.abs(psi_t - psi_prev_t)

def fidelity(psi_t, psi_prev_t):
    return 1.0 - delta_psi(psi_t, psi_prev_t)

def entropy(psi_t, psi_prev_t):
    dpsi = delta_psi(psi_t, psi_prev_t)
    return np.log(1 + dpsi + (1 - (1.0 - dpsi)))  # Simplifies to log(1 + 2*dpsi)

def reentry_delay(psi_history, t_now):
    for τ in range(1, len(psi_history)):
        if np.allclose(psi_history[t_now], psi_history[t_now - τ]):
            return τ
    return np.inf

# Tier II–III: Structural collapse metrics
def collapse_integrity(f, s, dpsi):
    return f * np.exp(-s) * (1 - dpsi)

def collapse_curvature(psi_field, x, neighbors, weights):
    return sum([(psi_field[x] - psi_field[xn])**2 * weights[i]
                for i, xn in enumerate(neighbors)])

def survival_probability(ic, curvature):
    return ic / (ic + curvature)

def collapse_index(s, dpsi, f):
    return s * dpsi * (1 - f)

# Tier IV-A: Symbolic logic gates
def discretio(dpsi_i, dpsi_j):
    return int(dpsi_i != dpsi_j)

def negatio(dpsi):
    return -dpsi

# Tier IV-B: Collapse communication packet
def structura(psi_t, dpsi, f, s, τr):
    return {
        'Ψ': psi_t,
        'δΨ': dpsi,
        'F': f,
        'S': s,
        'τR': τr
    }

# Collapse Intercept Zone
def is_alive(dpsi, f, s):
    return (dpsi < 0.29) and (f > 0.21) and (s < 3.5)

# Main symbolic agent update
def update_symbolic_field(psi_history: List[np.ndarray], t_now: int, weights: List[float], neighbor_map: Dict[int, List[int]]):
    psi_t = psi_history[t_now]
    psi_prev = psi_history[t_now - 1]
    state = []

    for x in range(len(psi_t)):
        dpsi = delta_psi(psi_t[x], psi_prev[x])
        f = fidelity(psi_t[x], psi_prev[x])
        s = entropy(psi_t[x], psi_prev[x])
        τr = reentry_delay(psi_history, t_now)
        ic = collapse_integrity(f, s, dpsi)
        neighbors = neighbor_map[x]
        curvature = collapse_curvature(psi_t, x, neighbors, weights)
        ps = survival_probability(ic, curvature)
        zc = collapse_index(s, dpsi, f)
        alive = is_alive(dpsi, f, s)
        packet = structura(psi_t[x], dpsi, f, s, τr)

        state.append({
            'x': x,
            'δΨ': dpsi,
            'F': f,
            'S': s,
            'τR': τr,
            'IC': ic,
            'Curvature': curvature,
            'P(S)': ps,
            'ZC': zc,
            'Alive': alive,
            'Packet': packet
        })

    return state
