import sys
import numpy as np
from PyQt5.QtWidgets import QApplication

from filter_responses import *

# Launch the Qt application.
app = QApplication(sys.argv)


def normal_butterworth(w, n=2):
    """
    :math:`n'{th}` order Butterworth low-pass filter with 1 rad/sec cutoff frequency.

    Parameters
    ----------
    w : float,
        Frequency
    n : int,
        Filter order.

    Returns
    -------
    float,
        Magnitude response at ``w``

    """
    return 1 / np.sqrt(1 + w ** (2 * n))


def normal_chebyshev(w, n=2, ripple=0.5):
    """
    :math:`n^{th}` order Chebyshev low-pass filter with 1 rad/sec cuttoff frequency.

    Parameters
    ----------
    w : float,
        Frequency
    n : int,
        Filter order
    ripple : float
        Filter ripple in dB

    Returns
    -------
    float,
        Magnitude response at ``w``.
    """
    epsilon = np.sqrt(10 ** (ripple / 10) - 1)
    if abs(w) <= 1:
        cheby_poly = np.cos(n * np.arccos(w))
    else:
        cheby_poly = np.cosh(n * np.arccosh(w))
    return 1 / np.sqrt(1 + (epsilon * cheby_poly) ** 2)


# Control sliders of test function.
pair = ((normal_butterworth, {'n': (2, 10)}),
        (normal_chebyshev, {'n': (2, 10), 'ripple': (0.1, 5)}))


# Start the application
w = Widget(pair, domain=np.logspace(-1, 5, 1000), log_scale=True,
           win_title='Filter Responses', plt_title='Butterworth and Chebyshev Filters',
           xlabel='w[log]', ylabel='Magnitude')
w.show()
sys.exit(app.exec_())

