import numpy as np
import pytest

from yase.optimization.optimizer import quad2, quad1, Rosenbrock
from yase.optimization.unconstrained.line_search import HeavyBallGradient


def test_quadratic():
    assert np.allclose(HeavyBallGradient(quad1).minimize()[0], quad1.x_star())
    assert np.allclose(HeavyBallGradient(quad2).minimize()[0], quad2.x_star())


def test_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(HeavyBallGradient(rosen).minimize()[0], rosen.x_star(), rtol=0.1)


if __name__ == "__main__":
    pytest.main()
