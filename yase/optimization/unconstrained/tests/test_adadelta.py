import numpy as np
import pytest

from yase.optimization.optimizer import quad1, quad2, Rosenbrock
from yase.optimization.unconstrained.stochastic import AdaDelta


def test_AdaDelta_quadratic():
    assert np.allclose(AdaDelta(quad1).minimize()[0], quad1.x_star(), rtol=0.1)
    assert np.allclose(AdaDelta(quad2).minimize()[0], quad2.x_star(), rtol=0.1)


def test_AdaDelta_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(AdaDelta(rosen, step_size=0.1).minimize()[0], rosen.x_star(), rtol=0.1)


def test_AdaDelta_standard_momentum_quadratic():
    assert np.allclose(AdaDelta(quad1, momentum_type='standard').minimize()[0], quad1.x_star(), rtol=0.1)
    assert np.allclose(AdaDelta(quad2, momentum_type='standard').minimize()[0], quad2.x_star(), rtol=0.1)


def test_AdaDelta_standard_momentum_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(AdaDelta(rosen, momentum_type='standard').minimize()[0], rosen.x_star(), rtol=0.1)


def test_AdaDelta_nesterov_momentum_quadratic():
    assert np.allclose(AdaDelta(quad1, momentum_type='nesterov').minimize()[0], quad1.x_star(), rtol=0.1)
    assert np.allclose(AdaDelta(quad2, momentum_type='nesterov').minimize()[0], quad2.x_star(), rtol=0.1)


def test_AdaDelta_nesterov_momentum_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(AdaDelta(rosen, momentum_type='nesterov').minimize()[0], rosen.x_star(), rtol=0.01)


if __name__ == "__main__":
    pytest.main()
