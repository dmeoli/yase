import numpy as np
import pytest

from yase.optimization.optimizer import quad2, quad1, Rosenbrock
from yase.optimization.unconstrained.line_search import QuadraticSteepestGradientDescent, SteepestGradientDescent
from yase.optimization.unconstrained.stochastic import StochasticGradientDescent


def test_QuadraticSteepestGradientDescent():
    assert np.allclose(QuadraticSteepestGradientDescent(quad1).minimize()[0], quad1.x_star())
    assert np.allclose(QuadraticSteepestGradientDescent(quad2).minimize()[0], quad2.x_star())


def test_SteepestGradientDescent_quadratic():
    assert np.allclose(SteepestGradientDescent(quad1).minimize()[0], quad1.x_star())
    assert np.allclose(SteepestGradientDescent(quad2).minimize()[0], quad2.x_star())


def test_SteepestGradientDescent_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(SteepestGradientDescent(rosen).minimize()[0], rosen.x_star())


def test_GradientDescent_quadratic():
    assert np.allclose(StochasticGradientDescent(quad1).minimize()[0], quad1.x_star())
    assert np.allclose(StochasticGradientDescent(quad2).minimize()[0], quad2.x_star())


def test_GradientDescent_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(StochasticGradientDescent(rosen).minimize()[0], rosen.x_star(), rtol=0.1)


def test_GradientDescent_standard_momentum_quadratic():
    assert np.allclose(StochasticGradientDescent(quad1, momentum_type='standard').minimize()[0], quad1.x_star())
    assert np.allclose(StochasticGradientDescent(quad2, momentum_type='standard').minimize()[0], quad2.x_star())


def test_GradientDescent_standard_momentum_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(StochasticGradientDescent(rosen, momentum_type='standard').minimize()[0], rosen.x_star())


def test_GradientDescent_Nesterov_momentum_quadratic():
    assert np.allclose(StochasticGradientDescent(quad1, momentum_type='nesterov').minimize()[0], quad1.x_star())
    assert np.allclose(StochasticGradientDescent(quad2, momentum_type='nesterov').minimize()[0], quad2.x_star())


def test_GradientDescent_Nesterov_momentum_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(StochasticGradientDescent(rosen, momentum_type='nesterov').minimize()[0], rosen.x_star())


if __name__ == "__main__":
    pytest.main()
