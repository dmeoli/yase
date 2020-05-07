import numpy as np
import pytest

from yase.optimization.optimizer import quad2, quad1, Rosenbrock
from yase.optimization.unconstrained.stochastic import RProp


def test_RProp_quadratic():
    assert np.allclose(RProp(quad1).minimize()[0], quad1.x_star())
    assert np.allclose(RProp(quad2).minimize()[0], quad2.x_star())


def test_RProp_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(RProp(rosen).minimize()[0], rosen.x_star(), rtol=0.1)


def test_RProp_standard_momentum_quadratic():
    assert np.allclose(RProp(quad1, momentum_type='standard', momentum=0.6).minimize()[0], quad1.x_star())
    assert np.allclose(RProp(quad2, momentum_type='standard', momentum=0.6).minimize()[0], quad2.x_star())


def test_RProp_standard_momentum_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(RProp(rosen, momentum_type='standard', momentum=0.6).minimize()[0], rosen.x_star(), rtol=0.1)


def test_RProp_nesterov_momentum_quadratic():
    assert np.allclose(RProp(quad1, momentum_type='nesterov').minimize()[0], quad1.x_star())
    assert np.allclose(RProp(quad2, momentum_type='nesterov').minimize()[0], quad2.x_star())


def test_RProp_nesterov_momentum_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(RProp(rosen, momentum_type='nesterov').minimize()[0], rosen.x_star(), rtol=0.1)


if __name__ == "__main__":
    pytest.main()
