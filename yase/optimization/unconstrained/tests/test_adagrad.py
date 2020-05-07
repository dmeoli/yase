import numpy as np
import pytest

from yase.optimization.optimizer import quad1, quad2, Rosenbrock
from yase.optimization.unconstrained.stochastic import AdaGrad


def test_AdaGrad_quadratic():
    assert np.allclose(AdaGrad(quad1, step_size=0.1).minimize()[0], quad1.x_star(), rtol=0.1)
    assert np.allclose(AdaGrad(quad2, step_size=0.15).minimize()[0], quad2.x_star(), rtol=0.1)


def test_AdaGrad_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(AdaGrad(rosen, step_size=0.1).minimize()[0], rosen.x_star(), rtol=0.1)


def test_AdaGrad_standard_momentum_quadratic():
    assert np.allclose(AdaGrad(quad1, momentum_type='standard').minimize()[0], quad1.x_star(), rtol=0.1)
    assert np.allclose(AdaGrad(quad2, step_size=0.1, momentum_type='standard').minimize()[0], quad2.x_star(), rtol=0.1)


def test_AdaGrad_standard_momentum_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(AdaGrad(rosen, momentum_type='standard').minimize()[0], rosen.x_star(), rtol=0.1)


def test_AdaGrad_nesterov_momentum_quadratic():
    assert np.allclose(AdaGrad(quad1, momentum_type='nesterov').minimize()[0], quad1.x_star(), rtol=0.1)
    assert np.allclose(AdaGrad(quad2, step_size=0.1, momentum_type='nesterov').minimize()[0], quad2.x_star(), rtol=0.1)


def test_AdaGrad_nesterov_momentum_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(AdaGrad(rosen, momentum_type='nesterov').minimize()[0], rosen.x_star(), rtol=0.1)


if __name__ == "__main__":
    pytest.main()
