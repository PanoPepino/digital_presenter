"""Validated geometry operations, independent of presenter classes."""

import numpy as np


def vector3(value, name="vector") -> np.ndarray:
    """Return an owned finite three-dimensional vector."""
    result = np.array(value, dtype=float, copy=True)
    if result.shape != (3,) or not np.isfinite(result).all():
        raise ValueError(f"{name} must contain three finite coordinates")
    return result


def direction_vector(value, origin) -> np.ndarray:
    """Resolve a direction or object center to a unit vector; zero stays zero."""
    if hasattr(value, "get_center"):
        value = value.get_center() - vector3(origin, "origin")
    vector = vector3(value, "direction")
    length = np.linalg.norm(vector)
    return vector / length if length > 1e-12 else np.zeros(3)


def signed_planar_angle(source, target) -> float:
    """Return signed XY rotation from source to target."""
    source = vector3(source, "hand direction")[:2]
    target = vector3(target, "pointing direction")[:2]
    if np.linalg.norm(source) <= 1e-12:
        raise ValueError("Hand geometry must have a nonzero pointing axis")
    if np.linalg.norm(target) <= 1e-12:
        return 0.0
    source = source / np.linalg.norm(source)
    target = target / np.linalg.norm(target)
    cross = source[0] * target[1] - source[1] * target[0]
    return float(np.arctan2(cross, np.dot(source, target)))


def positive(value, name):
    """Validate a finite positive dimension or duration."""
    if not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return value
