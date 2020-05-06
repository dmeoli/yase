# Machine Learning & Numerical Optimization 
[![Build Status](https://travis-ci.org/dmeoli/MachineLearningNumericalOptimization.svg?branch=master)](https://travis-ci.org/dmeoli/MachineLearningNumericalOptimization) [![Coverage Status](https://coveralls.io/repos/github/dmeoli/MachineLearningNumericalOptimization/badge.svg?branch=master)](https://coveralls.io/github/dmeoli/MachineLearningNumericalOptimization?branch=master) [![Python Version](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)

This code is a simple and modular implementation of some of the most important optimization algorithms used as core 
solver for many machine learning models developed during the Machine Learning & Numerical Methods and Optimization 
courses @ [Department of Computer Science](https://www.di.unipi.it/en/) @ [University of Pisa](https://www.unipi.it/index.php/english).

## Contents

- Numerical Optimization
    - Unconstrained Optimization
        - Line Search Methods [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dmeoli/MachineLearningNumericalOptimization/blob/master/LineSearchMethods.ipynb)
            - Exact Line Search Methods
                - [x] Quadratic Steepest Gradient Descent
                - [x] Quadratic Conjugate Gradient
            - Inexact Line Search Methods
                - 0th Order Methods
                    - [x] Subgradient
                - 1st Order Methods
                    - [x] Steepest Gradient Descent
                    - [ ] Conjugate Gradient
                        - [ ] Fletcher–Reeves formula
                        - [ ] Polak–Ribière formula
                        - [ ] Hestenes-Stiefel formula
                        - [ ] Dai-Yuan formula
                    - [x] Nonlinear Conjugate Gradient
                        - [x] Fletcher–Reeves formula
                        - [x] Polak–Ribière formula
                        - [x] Hestenes-Stiefel formula
                        - [x] Dai-Yuan formula
                    - [x] Heavy Ball Gradient
                - 2nd Order Methods
                    - [x] Newton
                    - [x] BFGS quasi-Newton
                    - [ ] L-BFGS quasi-Newton
        - Stochastic Methods [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dmeoli/MachineLearningNumericalOptimization/blob/master/StochasticMethods.ipynb)
            - [x] Stochastic Gradient Descent
                - [x] standard momentum
                - [x] Nesterov momentum
                - [ ] learning rate decay
                - [ ] momentum decay
            - [x] Adam
                - [x] standard momentum
                - [x] Nadam
                - [ ] learning rate decay
                - [ ] momentum decay
            - [x] AMSGrad
                - [x] standard momentum
                - [x] Nesterov momentum
                - [ ] learning rate decay
                - [ ] momentum decay
            - [x] AdaMax
                - [x] standard momentum
                - [x] NadaMax
                - [ ] learning rate decay
                - [ ] momentum decay
            - [x] AdaGrad
                - [x] standard momentum
                - [x] Nesterov momentum
                - [ ] learning rate decay
                - [ ] momentum decay
            - [x] AdaDelta
                - [x] standard momentum
                - [x] Nesterov momentum
                - [ ] learning rate decay
                - [ ] momentum decay
            - [x] RProp
                - [x] standard momentum
                - [x] Nesterov momentum
                - [ ] learning rate decay
                - [ ] momentum decay
            - [x] RMSProp
                - [x] standard momentum
                - [x] Nesterov momentum
                - [ ] learning rate decay
                - [ ] momentum decay
        - [x] Proximal Bundle with [cvxpy](https://github.com/cvxgrp/cvxpy) interface
             - [x] standard momentum
             - [x] Nesterov momentum
        - [x] [scipy.optimize](https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html) interface
    - Constrained Optimization
        - Box-Constrained Quadratic Optimization Methods
            - [x] Projected Gradient
            - [x] Frank-Wolfe or Conditional Gradient
            - [x] Active Set
            - [x] Interior Point
            - [x] Lagrangian Dual
            - [x] Sequential Minimal Optimization (ad hoc for SVMs)
            - [x] BCQP solver with [scipy.optimize.slsqp](https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html#sequential-least-squares-programming-slsqp-algorithm-method-slsqp) interface
        - Quadratic Optimization
            - [x] QP solver with [qpsolvers](https://github.com/stephane-caron/qpsolvers) interface
            - [x] QP solver with [scipy.optimize.slsqp](https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html#sequential-least-squares-programming-slsqp-algorithm-method-slsqp) interface

    - Optimization Functions
        - Unconstrained
            - [x] Rosenbrock
            - [x] Quadratic
                - [x] Lagrangian Box-Constrained
        - Constrained
            - [x] Quadratic Box-Constrained

- Machine Learning Models
    - [x] Support Vector Machines [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dmeoli/MachineLearningNumericalOptimization/blob/master/SupportVectorMachines.ipynb)
        - [x] Support Vector Classifier
        - [x] Support Vector Regression
        - Kernels
            - [x] linear kernel
            - [x] polynomial kernel
            - [x] rbf kernel
            - [x] laplacian kernel
            - [x] sigmoid kernel
    - [x] Neural Networks
        - Losses
            - [x] Mean Squared Error
            - [x] Categorical Cross Entropy
            - [x] Sparse Categorical Cross Entropy
            - [x] Binary Cross Entropy
        - Regularizers
            - [x] L1 or Lasso
            - [x] L2 or Ridge or Tikhonov
        - Activations
            - [x] Sigmoid
            - [x] Tanh
            - [x] ReLU
            - [x] SoftMax
        - Layers
            - [x] Fully Connected
            - [x] Convolutional [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dmeoli/MachineLearningNumericalOptimization/blob/master/ConvolutionalNeuralNetworks.ipynb)
                - [x] Conv 2D
                - [x] Max Pooling
                - [x] Avg Pooling
                - [x] Flatten
            - [ ] Recurrent
                - [ ] Long Short-Term Memory (LSTM)
                - [ ] Gated Recurrent Units (GRU)
            - Normalization
                - [x] Dropout
                - [ ] Batch Normalization
        - Initializers
            - [x] Xavier or Glorot normal and uniform
            - [x] He normal and uniform

## License [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This software is released under the MIT License. See the [LICENSE](LICENSE) file for details.
