"""Sanity check tests."""


def test_environment_sanity():
    import numpy as np

    arr = np.array([1, 2, 3])
    assert arr.sum() == 6