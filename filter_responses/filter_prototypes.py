"""
:mod:`filter_prototypes` includes the filter prototypes
"""

import numpy as np
from scipy import signal


def coefficients2hs(a, b, n=1):
    """Converts filter coefficients to transfer function in s-domain"""

    def hs(s):
        return a / np.sum([b[k] * s ** k for k in range(int(n), -1, -1)], axis=0)

    return hs


def hs2hw(hs):
    """Converts filter transfer function in s domain into frequency domain"""

    def hw(w):
        return hs(1j * w)

    return hw


def hw2hwmag(hw):
    """Converts frequency function to amplitude response function"""

    def hwmag(w):
        return np.abs(hw(w))

    return hwmag


def hw2hwphase(hw):
    """Converts frequency function to phase response function"""

    def hwphase(w):
        return np.angle(hw(w)) * 180 / np.pi

    return hwphase


def test_func():
    """Test function"""
    import matplotlib.pyplot as plt

    def butter_hw_mag(w, n=4):
        if not hasattr(butter_hw_mag, 'filter_func'):
            a, b = signal.butter(n, 1., btype='low', analog=True)
            butter_hw_mag.filter_func = hw2hwmag(hs2hw(coefficients2hs(a, b[::-1], n=n)))
        return butter_hw_mag.filter_func(w)

    def butter_hw_phase(w, n=4):
        if not hasattr(butter_hw_phase, 'filter_func'):
            a, b = signal.butter(n, 1., btype='low', analog=True)
            butter_hw_phase.filter_func = hw2hwphase(hs2hw(coefficients2hs(a, b[::-1], n=n)))
        return butter_hw_mag.filter_func(w)

    def cheby_hw_mag(w, n=4, eps=1):
        if not hasattr(cheby_hw_mag, 'filter_func'):
            a, b = signal.cheby1(n, eps, 1., btype='low', analog=True)
            cheby_hw_mag.filter_func = hw2hwmag(hs2hw(coefficients2hs(a, b[::-1], n=n)))
        return cheby_hw_mag.filter_func(w)

    def cheby_hw_phase(w, n=4, eps=1):
        if not hasattr(cheby_hw_phase, 'filter_func'):
            a, b = signal.cheby1(n, eps, 1., btype='low', analog=True)
            cheby_hw_phase.filter_func = hw2hwphase(hs2hw(coefficients2hs(a, b[::-1], n=n)))
        return cheby_hw_phase.filter_func(w)

    # Compute responses
    domain = np.linspace(0, 5, 1001)
    butter_mag_res = np.array([butter_hw_mag(w) for w in domain])
    butter_phase_res = np.array([butter_hw_phase(w) for w in domain])
    cheby_mag_res = np.array([cheby_hw_mag(w) for w in domain])
    cheby_phase_res = np.array([cheby_hw_phase(w) for w in domain])

    # Plot responses
    fig, ax = plt.subplots(nrows=2, ncols=2)
    ax[0, 0].plot(domain, butter_mag_res)
    ax[1, 0].plot(domain, butter_phase_res)
    ax[0, 1].plot(domain, cheby_mag_res)
    ax[1, 1].plot(domain, cheby_phase_res)

    plt.show()


if __name__ == '__main__':
    test_func()
