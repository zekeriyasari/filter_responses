import numpy as np
from numpy.polynomial import polynomial

# TODO: Include Foster I-II and Cauer I-II realizations.


def continued_fractions(num, den):
    """
    Compute continued fractions for polynomials `num` and `den`.


    Parameters
    ----------
    num : numpy.ndarray,
        Numerator polynomial
    den : numpy.ndarray
        Denominator polynomial

    Returns
    -------
    numpy.ndarray : Coefficients of continued fractions of polynomials.

    Raises
    ------
    ValueError : is raised if degree of `den` is greate than that of `num`. 
    """
    num_deg = np.nonzero(num)[0][-1]
    den_deg = np.nonzero(den)[0][-1]
    if den_deg > num_deg:
        ValueError("Numerator degree must be grater than denominator degree")

    # Compute the coefficients
    alphas = np.zeros(num_deg)
    for i in range(num_deg):
        quo, rem = polynomial.polydiv(num, den)
        alphas[i] = quo[1]
        num, den = den, rem

    return alphas


def is_hurwitz(pol, get_cof=False):
    """
    Check if polynomial is `pol` Hurwitz polynomial.

    To check if `pol` is Hurwitz, :func:`continued_fractions` is called. `pol` is Hurwitz, 
    if all the coefficients are positive.

    Parameters
    ----------
    pol : numpy.ndarray
        Polynomial to be checked.
    get_cof : bool, optional
        If True, return continued fractions coefficients.(Defaults to false).

    Returns
    -------
    bool : If `pol` is Hurwitz or not. If `get_cof` is true, 
        continued fraction coefficients are also returned.
    """
    # Construct even and odd polynomials.
    p = pol.size - 1
    even_idx = range(0, p + 1, 2)
    odd_idx = range(1, p + 1, 2)
    even_pol = np.zeros(p + 1)
    odd_pol = np.zeros(p + 1)
    even_pol[even_idx] = pol[even_idx]
    odd_pol[odd_idx] = pol[odd_idx]
    n = np.nonzero(odd_pol)[0][-1]
    m = np.nonzero(even_pol)[0][-1]

    # Determine numerator and denominator
    if m > n:
        num, den = even_pol, odd_pol
    else:
        num, den = odd_pol, even_pol
    alphas = continued_fractions(num, den)

    if get_cof:
        return np.all(alphas > 0), alphas
    return np.all(alphas > 0)


if __name__ == "__main__":
    pol1 = np.array([6, 11, 6, 1])
    _, cof1 = is_hurwitz(pol1, get_cof=True)
    print("Coefficients: ", cof1)

    pol2 = np.array([1, 1, 1, 2])
    _, cof2 = is_hurwitz(pol2, get_cof=True)
    print("Coefficients: ", cof2)

    pol3 = np.array([1, 2, 2, 1])  # 3rd order Butterworth filter
    _, cof3 = is_hurwitz(pol3, get_cof=True)
    print("Coefficients: ", cof3)

    pol4 = np.array([0, 2, 0, 2])  # 3rd order Butterworth filter
    cof4 = continued_fractions(np.array([6, 0, 8, 0, 2]), np.array([0, 2, 0, 1, 0]))
    print("Coefficients: ", cof4)
