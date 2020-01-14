import matplotlib.pyplot as plt
import numpy as np

from optimization.optimizer import Optimizer, LineSearchOptimizer


class SteepestGradientDescentQuadratic(Optimizer):
    """
    Apply the Steepest Gradient Descent algorithm with exact line search to the quadratic function.

        f(x) = 1/2 x^T Q x - q^T x

    :param f:        the objective function.
    :param wrt:      ([n x 1] real column vector): the point where to start the algorithm from
    :return x:       ([n x 1] real column vector): either the best solution found so far (possibly the
                     optimal one) or a direction proving the problem is unbounded below, depending on case
    :return status:  (string): a string describing the status of the algorithm at termination:
                        - 'optimal': the algorithm terminated having proven that x is a(n approximately) optimal
                     solution, i.e., the norm of the gradient at x is less than the required threshold;
                        - 'unbounded': the algorithm terminated having proven that the problem is unbounded below:
                     x contains a direction along which f is decreasing to -inf, either because f is linear
                     along x and the directional derivative is not zero, or because x is a direction with
                     negative curvature;
                        - 'stopped': the algorithm terminated having exhausted the maximum number of iterations:
                     x is the best solution found so far, but not necessarily the optimal one.
    """

    def __init__(self, f, wrt=None, f_star=np.inf, eps=1e-6, max_iter=1000, verbose=False, plot=False):
        super().__init__(f, wrt, eps, max_iter, verbose, plot)
        if self.wrt.size != self.f.hessian().shape[0]:
            raise ValueError('x size does not match with Q')
        if not np.isrealobj(f_star) or not np.isscalar(f_star):
            raise ValueError('f_star is not a real scalar')
        self.f_star = f_star

    def minimize(self):
        if self.verbose:
            print('iter\tf(x)\t\t\t||g(x)||', end='')
        if self.f_star < np.inf:
            if self.verbose:
                print('\tf(x) - f*\trate', end='')
            prev_v = np.inf
        if self.verbose:
            print()

        if self.plot and self.n == 2:
            surface_plot, contour_plot, contour_plot, contour_axes = self.f.plot()

        while True:
            # compute function value and gradient
            v, g = self.f.function(self.wrt), self.f.jacobian(self.wrt)
            ng = np.linalg.norm(g)

            # output statistics
            if self.verbose:
                print('{:4d}\t{:1.8e}\t\t{:1.4e}'.format(self.iter, v, ng), end='')
            if self.f_star < np.inf:
                if self.verbose:
                    print('\t{:1.4e}'.format(v - self.f_star), end='')
                if prev_v < np.inf:
                    if self.verbose:
                        print('\t{:1.4e}'.format((v - self.f_star) / (prev_v - self.f_star)), end='')
                prev_v = v
            if self.verbose:
                print()

            # stopping criteria
            if ng <= self.eps:
                status = 'optimal'
                break

            if self.iter > self.max_iter:
                status = 'stopped'
                break

            d = -g

            # check if f is unbounded below
            den = d.T.dot(self.f.hessian()).dot(d)

            if den <= 1e-12:
                # this is actually two different cases:
                #
                # - d.T.dot(Q).dot(d) = 0, i.e., f is linear along d, and since the
                #   gradient is not zero, it is unbounded below;
                #
                # - d.T.dot(Q).dot(d) < 0, i.e., d is a direction of negative curvature
                #   for f, which is then necessarily unbounded below.
                status = 'unbounded'
                break

            # compute step size
            a = d.T.dot(d) / den  # or ng ** 2 / den

            # assert np.isclose(d.T.dot(d), ng ** 2)

            # compute new point
            last_wrt = self.wrt + a * d

            # plot the trajectory
            if self.plot and self.n == 2:
                p_xy = np.vstack((self.wrt, last_wrt))
                contour_axes.plot(p_xy[:, 0], p_xy[:, 1], color='k')

            # <\nabla f(x_i), \nabla f(x_i+1)> = 0
            # assert np.isclose(self.f.jacobian(self.wrt).T.dot(self.f.jacobian(last_wrt)), 0)

            self.wrt = last_wrt
            self.iter += 1

        if self.verbose:
            print()
        if self.plot and self.n == 2:
            plt.show()
        return self.wrt, status


class SteepestGradientDescent(LineSearchOptimizer):
    """
    Apply the classical Steepest Descent algorithm for the minimization of
    the provided function f.
    # - x is either a [n x 1] real (column) vector denoting the input of
    #   f(), or [] (empty).
    #
    # - x (either [n x 1] real vector or [], default []): starting point.
    #   If x == [], the default starting point provided by f() is used.
    #
    # - eps (real scalar, optional, default value 1e-6): the accuracy in the
    #   stopping criterion: the algorithm is stopped when the norm of the
    #   gradient is less than or equal to eps. If a negative value is provided,
    #   this is used in a *relative* stopping criterion: the algorithm is
    #   stopped when the norm of the gradient is less than or equal to
    #   (- eps) * || norm of the first gradient ||.
    #
    # - max_f_eval (integer scalar, optional, default value 1000): the maximum
    #   number of function evaluations (hence, iterations will be not more than
    #   max_f_eval because at each iteration at least a function evaluation is
    #   performed, possibly more due to the line search).
    #
    # - m1 (real scalar, optional, default value 0.01): first parameter of the
    #   Armijo-Wolfe-type line search (sufficient decrease). Has to be in (0,1)
    #
    # - m2 (real scalar, optional, default value 0.9): typically the second
    #   parameter of the Armijo-Wolfe-type line search (strong curvature
    #   condition). It should to be in (0,1); if not, it is taken to mean that
    #   the simpler Backtracking line search should be used instead
    #
    # - a_start (real scalar, optional, default value 1): starting value of
    #   alpha in the line search (> 0)
    #
    # - tau (real scalar, optional, default value 0.9): scaling parameter for
    #   the line search. In the Armijo-Wolfe line search it is used in the
    #   first phase: if the derivative is not positive, then the step is
    #   divided by tau (which is < 1, hence it is increased). In the
    #   Backtracking line search, each time the step is multiplied by tau
    #   (hence it is decreased).
    #
    # - sfgrd (real scalar, optional, default value 0.01): safeguard parameter
    #   for the line search. To avoid numerical problems that can occur with
    #   the quadratic interpolation if the derivative at one endpoint is too
    #   large w.r.t. The one at the other (which leads to choosing a point
    #   extremely near to the other endpoint), a *safeguarded* version of
    #   interpolation is used whereby the new point is chosen in the interval
    #   [as * (1 + sfgrd), am * (1 - sfgrd)], being [as, am] the
    #   current interval, whatever quadratic interpolation says. If you
    #   experience problems with the line search taking too many iterations to
    #   converge at "nasty" points, try to increase this
    #
    # - m_inf (real scalar, optional, default value -inf): if the algorithm
    #   determines a value for f() <= m_inf this is taken as an indication that
    #   the problem is unbounded below and computation is stopped
    #   (a "finite -inf").
    #
    # - min_a (real scalar, optional, default value 1e-16): if the algorithm
    #   determines a step size value <= min_a, this is taken as an indication
    #   that something has gone wrong (the gradient is not a direction of
    #   descent, so maybe the function is not differentiable) and computation
    #   is stopped. It is legal to take min_a = 0, thereby in fact skipping this
    #   test.
    """

    def __init__(self, f, wrt=None, eps=1e-6, max_f_eval=1000, m1=0.01, m2=0.9, a_start=1, tau=0.9,
                 sfgrd=0.01, m_inf=-np.inf, min_a=1e-16, verbose=False, plot=False):
        """

        :param f:          the objective function.
        :param wrt:        ([n x 1] real column vector): the point where to start the algorithm from.
        :param eps:        (real scalar, optional, default value 1e-6): the accuracy in the stopping
                           criterion: the algorithm is stopped when the norm of the gradient is less
                           than or equal to eps.
        :param max_f_eval: (integer scalar, optional, default value 1000): the maximum number of
                           function evaluations (hence, iterations will be not more than max_f_eval
                           because at each iteration at least a function evaluation is performed,
                           possibly more due to the line search).
        :param m1:         (real scalar, optional, default value 0.01): first parameter of the
                           Armijo-Wolfe-type line search (sufficient decrease). Has to be in (0,1).
        :param m2:         (real scalar, optional, default value 0.9): typically the second parameter
                           of the Armijo-Wolfe-type line search (strong curvature condition). It should
                           to be in (0,1); if not, it is taken to mean that the simpler Backtracking
                           line search should be used instead.
        :param a_start:    (real scalar, optional, default value 1): starting value of alpha in the
                           line search (> 0).
        :param tau:        (real scalar, optional, default value 0.9): scaling parameter for the line
                           search. In the Armijo-Wolfe line search it is used in the first phase: if the
                           derivative is not positive, then the step is divided by tau (which is < 1,
                           hence it is increased). In the Backtracking line search, each time the step is
                           multiplied by tau (hence it is decreased).
        :param sfgrd:      (real scalar, optional, default value 0.01): safeguard parameter for the line search.
                           To avoid numerical problems that can occur with the quadratic interpolation if the
                           derivative at one endpoint is too large w.r.t. The one at the other (which leads to
                           choosing a point extremely near to the other endpoint), a *safeguarded* version of
                           interpolation is used whereby the new point is chosen in the interval
                           [as * (1 + sfgrd), am * (1 - sfgrd)], being [as, am] the current interval, whatever
                           quadratic interpolation says. If you experience problems with the line search taking
                           too many iterations to converge at "nasty" points, try to increase this.
        :param m_inf:      (real scalar, optional, default value -inf): if the algorithm determines a value for
                           f() <= m_inf this is taken as an indication that the problem is unbounded below and
                           computation is stopped (a "finite -inf").
        :param min_a:      (real scalar, optional, default value 1e-16): if the algorithm determines a step size
                           value <= min_a, this is taken as an indication that something has gone wrong (the gradient
                           is not a direction of descent, so maybe the function is not differentiable) and computation
                           is stopped. It is legal to take min_a = 0, thereby in fact skipping this test.
        :param verbose:    (boolean, optional, default value False): print details about each iteration
                           if True, nothing otherwise.
        :param plot:       (boolean, optional, default value False): plot the function's surface and its contours
                           if True and the function's dimension is 2, nothing otherwise.
        :return x:         ([n x 1] real column vector): the best solution found so far.
                                - v (real, scalar): if x == [] this is the best known lower bound on the unconstrained
                                global optimum of f(); it can be -inf if either f() is not bounded below, or no such
                                information is available. If x ~= [] then v = f(x);
                                - g (real, [n x 1] real vector): this also depends on x. If x == [] this is the
                                standard starting point from which the algorithm should start, otherwise it is the
                                gradient of f() at x (or a subgradient if f() is not differentiable at x, which it
                                should not be if you are applying the gradient method to it).
        :return status:    (string): a string describing the status of the algorithm at termination:
                              - 'optimal': the algorithm terminated having proven that x is a(n approximately) optimal
                           solution, i.e., the norm of the gradient at x is less than the required threshold;
                              - 'unbounded': the algorithm has determined an extremely large negative value for f()
                           that is taken as an indication that the problem is unbounded below (a "finite -inf",
                           see m_inf above);
                              - 'stopped': the algorithm terminated having exhausted the maximum number of iterations:
                           x is the bast solution found so far, but not necessarily the optimal one;
                              - 'error': the algorithm found a numerical error that prev_vents it from continuing
                           optimization (see min_a above).
        """
        super().__init__(f, wrt, eps, max_f_eval, m1, m2, a_start, tau, sfgrd, m_inf, min_a, verbose, plot)

    def minimize(self):
        f_star = self.f.function([])

        last_wrt = np.zeros((self.n,))  # last point visited in the line search
        last_g = np.zeros((self.n,))  # gradient of last_wrt
        f_eval = 1  # f() evaluations count ("common" with LSs)

        if f_star > -np.inf:
            if self.verbose:
                print('f_eval\trel gap\t\t|| g(x) ||\t\trate\t', end='')
            prev_v = np.inf
        else:
            if self.verbose:
                print('f_eval\tf(x)\t\t\t|| g(x) ||\t', end='')
        if self.verbose:
            print('ls f_eval\ta*')

        v, g = self.f.function(self.wrt), self.f.jacobian(self.wrt)
        ng = np.linalg.norm(g)
        if self.eps < 0:
            ng0 = -ng  # norm of first subgradient
        else:
            ng0 = 1  # un-scaled stopping criterion

        if self.plot and self.n == 2:
            surface_plot, contour_plot, contour_plot, contour_axes = self.f.plot()

        while True:
            # output statistics
            if f_star > -np.inf:
                if self.verbose:
                    print('{:4d}\t{:1.4e}\t{:1.4e}'.format(f_eval, (v - f_star) / max(abs(f_star), 1), ng), end='')
                if prev_v < np.inf:
                    if self.verbose:
                        print('\t{:1.4e}'.format((v - f_star) / (prev_v - f_star)), end='')
                else:
                    if self.verbose:
                        print('\t\t\t', end='')
                prev_v = v
            else:
                if self.verbose:
                    print('{:4d}\t{:1.8e}\t\t{:1.4e}'.format(f_eval, v, ng), end='')

            # stopping criteria
            if ng <= self.eps * ng0:
                status = 'optimal'
                break

            if f_eval > self.max_f_eval:
                status = 'stopped'
                break

            d = -g

            phi_p0 = -ng * ng

            # compute step size
            a, v, last_wrt, last_g, f_eval = self.line_search.search(d, self.wrt, last_wrt, last_g, f_eval,
                                                                     self.a_start, v, phi_p0)

            # output statistics
            if self.verbose:
                print('\t\t{:1.4e}'.format(a))

            if a <= self.min_a:
                status = 'error'
                break

            if v <= self.m_inf:
                status = 'unbounded'
                break

            # plot the trajectory
            if self.plot and self.n == 2:
                p_xy = np.vstack((self.wrt, last_wrt))
                contour_axes.plot(p_xy[:, 0], p_xy[:, 1], color='k')

            # update new point
            self.wrt = last_wrt

            # update gradient
            g = last_g
            ng = np.linalg.norm(g)

            self.iter += 1

        if self.verbose:
            print()
        if self.plot and self.n == 2:
            plt.show()
        return self.wrt, status


class GradientDescent(Optimizer):

    def __init__(self, f, wrt=None, eps=1e-6, max_iter=1000, step_rate=0.01, momentum=0.,
                 momentum_type='none', verbose=False, plot=False):
        super().__init__(f, wrt, eps, max_iter, verbose, plot)
        if not np.isscalar(step_rate):
            raise ValueError('step_rate is not a real scalar')
        if step_rate < 0:
            raise ValueError('step_rate must be > 0')
        self.step_rate = step_rate
        if not np.isscalar(momentum):
            raise ValueError('momentum is not a real scalar')
        if momentum < 0:
            raise ValueError('momentum must be > 0')
        self.momentum = momentum
        if momentum_type not in ('nesterov', 'standard', 'none'):
            raise ValueError('unknown momentum type')
        self.momentum_type = momentum_type

        self.step = 0
        self.state_fields = 'step_rate momentum momentum_type step iter'.split()

    def minimize(self):
        f_star = self.f.function([])

        f_eval = 1  # f() evaluations count ("common" with LSs)

        if f_star > -np.inf:
            if self.verbose:
                print('f_eval\trel gap\t\t|| g(x) ||\t\trate\t', end='')
            prev_v = np.inf
        else:
            if self.verbose:
                print('f_eval\tf(x)\t\t\t|| g(x) ||\t', end='')
        if self.verbose:
            print('ls f_eval\ta*')

        v, g = self.f.function(self.wrt), self.f.jacobian(self.wrt)
        ng = np.linalg.norm(g)
        if self.eps < 0:
            ng0 = -ng  # norm of first subgradient
        else:
            ng0 = 1  # un-scaled stopping criterion

        if self.plot and self.n == 2:
            surface_plot, contour_plot, contour_plot, contour_axes = self.f.plot()

        while True:
            # output statistics
            if f_star > -np.inf:
                if self.verbose:
                    print('{:4d}\t{:1.4e}\t{:1.4e}'.format(f_eval, (v - f_star) / max(abs(f_star), 1), ng), end='')
                if prev_v < np.inf:
                    if self.verbose:
                        print('\t{:1.4e}'.format((v - f_star) / (prev_v - f_star)), end='')
                else:
                    if self.verbose:
                        print('\t\t\t', end='')
                prev_v = v
            else:
                if self.verbose:
                    print('{:4d}\t{:1.8e}\t\t{:1.4e}'.format(f_eval, v, ng), end='')

            step_m1 = self.step

            if self.momentum_type == 'standard':
                gradient = self.f.jacobian(self.wrt)
                step = step_m1 * self.momentum + self.step_rate * gradient
                self.wrt -= step
            elif self.momentum_type == 'nesterov':
                big_jump = step_m1 * self.momentum
                self.wrt -= big_jump
                gradient = self.f.jacobian(self.wrt)
                correction = self.step_rate * gradient
                self.wrt -= correction
                step = big_jump + correction
            elif self.momentum_type == 'none':
                gradient = self.f.jacobian(self.wrt)
                step = self.step_rate * gradient
                self.wrt -= step

            # stopping criteria
            if ng <= self.eps * ng0:
                status = 'optimal'
                break

            if self.iter > self.max_iter:
                status = 'stopped'
                break

            # plot the trajectory
            if self.plot and self.n == 2:
                p_xy = np.vstack((self.wrt, step_m1))
                contour_axes.plot(p_xy[:, 0], p_xy[:, 1], color='k')

            self.step = step

            self.iter += 1

        if self.verbose:
            print()
        if self.plot and self.n == 2:
            plt.show()
        return self.wrt, status


if __name__ == "__main__":
    import optimization.test_functions as tf

    print(SteepestGradientDescent(tf.Rosenbrock(), [-1, 1], verbose=True, plot=True).minimize())
    print()
    print(GradientDescent(tf.quad1, [-1, 1], [-1, 1], step_rate=0.01, momentum_type='standard',
                          verbose=True, plot=True).minimize())
