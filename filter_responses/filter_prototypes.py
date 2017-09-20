"""
:mod:`filter_prototypes` includes the filter prototypes
"""

import numpy as np
from scipy import signal


# TODO: Conversions from lowpass to highpass, bandpass and bandreject filters are to be added.

def coefficients2hs(a, b, n=1):
    """
    Converts filter coefficients to transfer function in s-domain
    
    Parameters
    ----------
    a : numpy.ndarray
        Nominator coefficients of the filter.
    b : numpy.ndarray
        Denominator coefficients of the filter.
    n : int, optional
        Filter order. (Default=1)

    Returns
    -------
    callable
        s-domain transfer function :func:`hs` of the filter.

    """

    def hs(s):
        return a / np.sum([b[k] * s ** k for k in range(int(n), -1, -1)], axis=0)

    return hs


def hs2hw(hs):
    """
    Converts filter transfer function in s domain into frequency domain.
    
    Parameters
    ----------
    hs : callable,
        s-domain transfer function of the filter

    Returns
    -------
    callable
        Frequency domain transfer function :func:`h` of the filter.
    """

    def hw(w):
        return hs(1j * w)

    return hw


def hw2hwmag(hw):
    """
    Converts frequency function to amplitude response function.
    
    Parameters
    ----------
    hw :  callable,
        Frequency domain transfer function of the filter.

    Returns
    -------
    callable
        Magnitude response function of the filter.

    """

    def hwmag(w):
        return np.abs(hw(w))

    return hwmag


def hw2hwphase(hw):
    """
    Converts frequency function to phase response function.
    
    Parameters
    ----------
    hw : callable,
        Frequency domain transfer function of the filter.

    Returns
    -------
    callable
        Phase response function of the filter.

    """

    def hwphase(w):
        return np.angle(hw(w)) * 180 / np.pi

    return hwphase


def main():
    """
    Test function to test the functions of the module.
    """
    import matplotlib.pyplot as plt

    def butter_hw_mag(w, n=4):
        if not hasattr(butter_hw_mag, 'filter_func'):
            a, b = signal.butter(n, 1., btype='low', analog=True)
            butter_hw_mag.filter_func = hw2hwmag(hs2hw(coefficients2hs(a, b[::-1], n=n)))
        return w, butter_hw_mag.filter_func(w)

    def butter_hw_phase(w, n=4):
        if not hasattr(butter_hw_phase, 'filter_func'):
            a, b = signal.butter(n, 1., btype='low', analog=True)
            butter_hw_phase.filter_func = hw2hwphase(hs2hw(coefficients2hs(a, b[::-1], n=n)))
        return w, butter_hw_mag.filter_func(w)

    def cheby_hw_mag(w, n=4, eps=1):
        if not hasattr(cheby_hw_mag, 'filter_func'):
            a, b = signal.cheby1(n, eps, 1., btype='low', analog=True)
            cheby_hw_mag.filter_func = hw2hwmag(hs2hw(coefficients2hs(a, b[::-1], n=n)))
        return w, cheby_hw_mag.filter_func(w)

    def cheby_hw_phase(w, n=4, eps=1):
        if not hasattr(cheby_hw_phase, 'filter_func'):
            a, b = signal.cheby1(n, eps, 1., btype='low', analog=True)
            cheby_hw_phase.filter_func = hw2hwphase(hs2hw(coefficients2hs(a, b[::-1], n=n)))
        return w, cheby_hw_phase.filter_func(w)

    # Compute responses
    domain = np.linspace(0, 5, 1001)
    butter_mag_res = butter_hw_mag(domain)
    butter_phase_res = butter_hw_phase(domain)
    cheby_mag_res = cheby_hw_mag(domain)
    cheby_phase_res = cheby_hw_phase(domain)

    # Plot responses
    fig, ax = plt.subplots(nrows=2, ncols=2)
    ax[0, 0].plot(butter_mag_res[0], butter_mag_res[1])
    ax[1, 0].plot(butter_phase_res[0], butter_phase_res[1])
    ax[0, 1].plot(cheby_mag_res[0], cheby_mag_res[1])
    ax[1, 1].plot(cheby_phase_res[0], cheby_phase_res[1])

    plt.show()


if __name__ == '__main__':
    main()
