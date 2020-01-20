import numpy as np
import pytest

from ml.datasets import DataSet
from ml.learning import WeightedLearner, ada_boost, grade_learner, err_ratio, LinearLearner
from ml.neural_network import PerceptronLearner


def test_ada_boost():
    iris = DataSet(name='iris')
    classes = ['setosa', 'versicolor', 'virginica']
    iris.classes_to_numbers(classes)
    wl = WeightedLearner(PerceptronLearner)
    ab = ada_boost(iris, wl, 5)
    tests = [([5, 3, 1, 0.1], 0),
             ([5, 3.5, 1, 0], 0),
             ([6, 3, 4, 1.1], 1),
             ([6, 2, 3.5, 1], 1),
             ([7.5, 4, 6, 2], 2),
             ([7, 3, 6, 2.5], 2)]
    assert grade_learner(ab, tests) > 2 / 3
    assert err_ratio(ab, iris) < 0.25


def test_linear_learner():
    iris = DataSet(name='iris')
    classes = ['setosa', 'versicolor', 'virginica']
    iris.classes_to_numbers(classes)
    n_samples, n_features = len(iris.examples), iris.target
    X, y = np.array([x[:n_features] for x in iris.examples]), \
           np.array([x[n_features] for x in iris.examples])
    ll = LinearLearner()
    ll.fit(X, y)
    tests = [([5, 3, 1, 0.1], 0),
             ([5, 3.5, 1, 0], 0),
             ([6, 3, 4, 1.1], 1),
             ([6, 2, 3.5, 1], 1),
             ([7.5, 4, 6, 2], 2),
             ([7, 3, 6, 2.5], 2)]
    assert ll.predict([[5.0, 3.1, 0.9, 0.1]]) == 0
    assert ll.predict([[5.1, 3.5, 1.0, 0.0]]) == 0
    assert ll.predict([[4.9, 3.3, 1.1, 0.1]]) == 0
    assert ll.predict([[6.0, 3.0, 4.0, 1.1]]) == 1
    assert ll.predict([[6.1, 2.2, 3.5, 1.0]]) == 1
    assert ll.predict([[5.9, 2.5, 3.3, 1.1]]) == 1
    assert ll.predict([[7.5, 4.1, 6.2, 2.3]]) == 2
    assert ll.predict([[7.3, 4.0, 6.1, 2.4]]) == 2
    assert ll.predict([[7.0, 3.3, 6.1, 2.5]]) == 2
    assert grade_learner(ll, tests) > 2 / 3
    assert err_ratio(ll, iris) < 0.25


def test_logistic_linear_learner():
    iris = DataSet(name='iris')
    classes = ['setosa', 'versicolor', 'virginica']
    iris.classes_to_numbers(classes)
    n_samples, n_features = len(iris.examples), iris.target
    X, y = np.array([x[:n_features] for x in iris.examples]), \
           np.array([x[n_features] for x in iris.examples])
    ll = LinearLearner(iris)
    ll.fit(X, y)
    tests = [([5, 3, 1, 0.1], 0),
             ([5, 3.5, 1, 0], 0),
             ([6, 3, 4, 1.1], 1),
             ([6, 2, 3.5, 1], 1),
             ([7.5, 4, 6, 2], 2),
             ([7, 3, 6, 2.5], 2)]
    assert ll.predict([[5.0, 3.1, 0.9, 0.1]]) == 0
    assert ll.predict([[5.1, 3.5, 1.0, 0.0]]) == 0
    assert ll.predict([[4.9, 3.3, 1.1, 0.1]]) == 0
    assert ll.predict([[6.0, 3.0, 4.0, 1.1]]) == 1
    assert ll.predict([[6.1, 2.2, 3.5, 1.0]]) == 1
    assert ll.predict([[5.9, 2.5, 3.3, 1.1]]) == 1
    assert ll.predict([[7.5, 4.1, 6.2, 2.3]]) == 2
    assert ll.predict([[7.3, 4.0, 6.1, 2.4]]) == 2
    assert ll.predict([[7.0, 3.3, 6.1, 2.5]]) == 2
    assert grade_learner(ll, tests) > 2 / 3
    assert err_ratio(ll, iris) < 0.25


if __name__ == "__main__":
    pytest.main()
