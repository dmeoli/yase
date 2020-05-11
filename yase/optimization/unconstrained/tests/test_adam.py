import numpy as np
import pytest

from yase.optimization.optimizer import quad1, quad2, Rosenbrock
from yase.optimization.unconstrained.stochastic import Adam


def test_Adam_quadratic():
    assert np.allclose(Adam(f=quad1, x=np.random.uniform(size=2), step_size=0.1).minimize().x,
                       quad1.x_star(), rtol=0.1)
    assert np.allclose(Adam(f=quad2, x=np.random.uniform(size=2), step_size=0.1).minimize().x,
                       quad2.x_star(), rtol=0.1)


def test_Adam_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(Adam(f=rosen, x=np.random.uniform(size=2), step_size=0.1).minimize().x,
                       rosen.x_star(), rtol=0.1)


def test_Adam_standard_momentum_quadratic():
    assert np.allclose(Adam(f=quad1, x=np.random.uniform(size=2), momentum_type='standard').minimize().x,
                       quad1.x_star(), rtol=0.1)
    assert np.allclose(Adam(f=quad2, x=np.random.uniform(size=2), momentum_type='standard').minimize().x,
                       quad2.x_star(), rtol=0.1)


def test_Adam_standard_momentum_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(Adam(f=rosen, x=np.random.uniform(size=2), step_size=0.1, epochs=2000,
                            momentum_type='standard').minimize().x, rosen.x_star(), rtol=0.1)


def test_Nadam_quadratic():
    assert np.allclose(Adam(f=quad1, x=np.random.uniform(size=2), momentum_type='nesterov').minimize().x,
                       quad1.x_star(), rtol=0.1)
    assert np.allclose(Adam(f=quad2, x=np.random.uniform(size=2), step_size=0.1, momentum_type='nesterov',
                            momentum=0.5).minimize().x, quad2.x_star(), rtol=0.1)


def test_Nadam_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(Adam(f=rosen, x=np.random.uniform(size=2), momentum_type='nesterov').minimize().x,
                       rosen.x_star(), rtol=0.1)


if __name__ == "__main__":
    pytest.main()
