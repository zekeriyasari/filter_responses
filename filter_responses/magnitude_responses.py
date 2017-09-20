"""
:mod:`magnitude_response` module includes a GUI to compare the magnitude response of the lowpass filters.
"""
from filter_responses.gui_widgets import *

# Launch the Qt application.
app = QApplication(sys.argv)


def butter_analytic(w, n=2):
    """
    :math:`n'{th}` order Butterworth low-pass filter with 1 rad/sec cutoff frequency.

    Parameters
    ----------
    w : numpy.ndarray,
        Frequency
    n : int, optional
        Filter order.(Default=2)

    Returns
    -------
    numpy.ndarray
        Magnitude response at ``w``

    """
    return 1 / np.sqrt(1 + w ** (2 * n))


def cheby_analytic(w, n=2, ripple=0.5):
    """
    :math:`n^{th}` order Chebyshev low-pass filter with 1 rad/sec cuttoff frequency.

    Parameters
    ----------
    w : numpy.ndarray,
        Frequency
    n : int, optional
        Filter order. (Default=2)
    ripple : float, optional
        Filter ripple in decibels. (Default=0.5)

    Returns
    -------
    numpy.ndarray,
        Magnitude response at ``w``.
    """
    epsilon = np.sqrt(10 ** (ripple / 10) - 1)
    if abs(w) <= 1:
        cheby_poly = np.cos(n * np.arccos(w))
    else:
        cheby_poly = np.cosh(n * np.arccosh(w))
    return 1 / np.sqrt(1 + (epsilon * cheby_poly) ** 2)


# Control sliders of test function.
pair = ((butter_analytic, {'n': (2, 10)}),
        (cheby_analytic, {'n': (2, 10), 'ripple': (0.1, 5)}))


# Start the application
w = Widget(pair, domain=np.logspace(-1, 5, 1000), log_scale=True,
           win_title='Filter Responses', plt_title='Butterworth and Chebyshev Filters',
           xlabel='w[rad/sec]', ylabel='Magnitude')
w.show()
sys.exit(app.exec_())

