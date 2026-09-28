import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """

    ### YOUR CODE HERE ###
    a = 1
    b = 1/(2**0.5)
    t = 1/4
    p = 1
    pi_estimate = (a + b) ** 2 / (4 * t)

    while True:
        a_n = (a+b)/2
        b_n = (a*b)**0.5
        p_n = 2*p
        t_n = t - p*(a_n-a)**2
    
        a = a_n
        b = b_n
        p = p_n
        t = t_n

        pi_estimate = ((a_n+b_n)**2)/(4*t_n)

        if abs(math.pi - pi_estimate) < abs(target_error):
            break



    # change this so an actual value is returned
    return pi_estimate




desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)

if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
