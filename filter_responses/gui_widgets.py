"""
:mod:`gui_widgets` module defines some of the widgets to be used in the GUI
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, \
    QVBoxLayout, QWidget
import pyqtgraph as pg
import numpy as np
from inspect import signature
from functools import partial
from matplotlib.colors import CSS4_COLORS


class Slider(QWidget):
    """
    Slider widget for parameter control of the plots.

    Attributes
    ----------
    minimum : int, optional
        Minimum value of the slider. (Default=0)
    maximum : int, optional
        Maximum value of the slider. (Default=1)
    data_type : type, optional
        Data of the slider data. If ``data_type`` is `int`, only integer slider values are  displayed. (Default=float)
    name : str, optional
        Name of the slider. (Default='')
    color : str,
        Color of the slider label.(Default='black')
    """

    def __init__(self, minimum=0, maximum=1, data_type=float, name='', color='black'):
        super().__init__()

        self.name = name
        self.minimum = minimum
        self.maximum = maximum
        self.data_type = data_type
        self.value = None
        self.color = color

        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout()
        self.label = QLabel(self)
        self.slider = QSlider(self)

        self.verticalLayout.addWidget(self.label)

        spacerItem = QSpacerItem(0, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        spacerItem1 = QSpacerItem(0, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.slider.setOrientation(Qt.Vertical)
        self.horizontalLayout.addWidget(self.slider)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.resize(self.sizeHint())
        self.slider.valueChanged.connect(self.set_label_value)
        self.set_label_value(self.slider.value())

    def set_label_value(self, value):
        """
        Update slider value.
        
        Parameters
        ----------
        value : float
            Value of the slider.
        """
        self.value = self.minimum + (float(value) / (self.slider.maximum() - self.slider.minimum())) * (
            self.maximum - self.minimum)
        if self.data_type is int:
            self.value = int(self.value)
        self.label.setText("{0}={1:.4g}".format(self.name, self.value))
        self.label.setStyleSheet('color: ' + self.color)


class SliderBlock(QWidget):
    """
    Group of sliders.
    
    This class basically constructs a single widget bundling a couple of sliders together.
    
    Attributes
    ----------
    sliders : Tuple[Slider]
        A tuple of sliders
    """

    def __init__(self, sliders):
        super().__init__()
        self.sliders = sliders
        self.horizontalLayout = QHBoxLayout(self)
        for slider in self.sliders:
            self.horizontalLayout.addWidget(slider)


class Widget(QWidget):
    """
    Plotting widget to plot parametric plots.

    Attributes
    ----------
    pairs : Tuple[Tuple[callable, dict]]
        Tuple of functions and corresponding parameters. Consider that we are to plot the functions

        .. math ::
            \begin{equation}
            \begin{split}
                & f_1(t, \alpha_1, \alpha_2, \ldots, \alpha_K) \\
                & f_2(t, \beta_1, \beta_2, \ldots, \beta_L)
            \end{split}
            \end{equation}

        for some control parameters `` \alpha_1 \in [m_{\alpha_1}, M_{\alpha_1}, \ldots, m_{\alpha_K}, M_{\alpha_K}]``
        and ``m_{\beta_1}, M_{\beta_1}, \ldots, m_{\beta_1}, M_{\beta_1}``, where ``m_{\alpha_i}`` and ``M_{\alpha_i}``
        is the minimum and maximum value of the parameter ``\alpha_i``. Then ``pairs`` is provided as

        pairs = (f_1, {'\alpha_1': (m_{\alpha_1}, M_{\alpha_1}), \ldots, '\alpha_1': (m_{\alpha_K}, M_{\alpha_K})}
                f_2, {'\beta_1': (m_{\beta_1}, M_{\beta_1}), \ldots, '\beta_1': (m_{\beta_K}, M_{\beta_K})})
    domain : numpy.ndarray, optional
        Domain of the functions of the to be plotted.(Default=np.linspace(0, 5, 1000))
    log_scale : bool, optional
        If True, the plot x-scale is logarithmic. (Default=False)
    win_title: str, optional
        Title of the GUI window. (Default='')
    plt_title: str, optional,
        Title of the plots. (Default='')
    xlabel : str, optional
        x-label of the plot. (Default='')
    ylabel : str, optional
        y-label of the plot. (Default='')
        
    """

    def __init__(self, pairs, domain=np.linspace(0, 5, 1000), log_scale=False,
                 win_title='', plt_title='', xlabel='', ylabel=''):

        super().__init__()

        self.pairs = pairs
        self.domain = domain
        self.log_scale = log_scale
        self.win_title = win_title
        self.plt_title = plt_title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.colors = tuple(CSS4_COLORS.values())

        self.horizontalLayout = QHBoxLayout(self)

        self.win = pg.GraphicsWindow(title=self.win_title)
        self.palette = self.win.addPlot(title=self.plt_title)
        self.palette.setLabel('left', self.ylabel)
        self.palette.setLabel('bottom', self.xlabel)
        self.horizontalLayout.addWidget(self.win)

        # Construct the sliders
        self.funcs = []
        for func, params in self.pairs:
            if func and params:
                self.palette.addLegend(offset=np.random.randint(100))
                if self.log_scale:
                    self.palette.setLogMode(x=True, y=False)
                pen_color = self.colors[np.random.randint(138)]
                func.curve = self.palette.plot(pen=pen_color,
                                               name=func.__name__)  # Get func curve
                func.sliders = []
                for parameter, interval in params.items():
                    min_val, max_val = interval
                    slider = Slider(min_val, max_val, name=parameter, color=pen_color)
                    self.horizontalLayout.addWidget(slider)
                    func.sliders.append(slider)
                self.funcs.append(func)

        self.update()

        for func in self.funcs:
            control_sliders = func.sliders
            for control_slider in control_sliders:
                control_slider.slider.valueChanged.connect(lambda: self.update())

    def update(self):
        """
        Update the curve of the graphics windows.
        
        This method is the callback function of the sliders. If the value of the slider is changed, 
        this method is called immediately. 
        """
        for func in self.funcs:
            # Get func curve and its control sliders
            curve = func.curve
            control_sliders = func.sliders

            # Read func control sliders and wrap func accordingly.
            sig = signature(func)
            params = dict()
            for control_slider in control_sliders:
                if control_slider.name in sig.parameters.keys():
                    params[control_slider.name] = control_slider.value
            func_ = partial(func, **params)

            # Compute new data of the func curve and update the curve.
            data = np.array([func_(x) for x in self.domain])
            curve.setData(x=self.domain, y=data)


def main():
    # Launch Qt GUI application
    app = QApplication(sys.argv)

    # Test function
    def f1(x, k1=1., alpha1=0.5, f01=1., phi1=0., x01=0.):
        return k1 * np.exp(-alpha1 * x) * np.cos(2 * np.pi * f01 * x + phi1) + x01

    # Test function
    def f2(x, k2=1., alpha2=0.5, f02=1., phi2=0., x02=0.):
        return k2 * np.exp(-alpha2 * x) * np.sin(2 * np.pi * f02 * x + phi2) + x02

    # Control sliders of test function.
    pair = ((f1, {'k1': (1, 10), 'alpha1': (0, 1), 'f01': (1, 10), 'phi1': (0, np.pi), 'x01': (0, 10)}),
            (f2, {'k2': (1, 10), 'alpha2': (0, 1), 'f02': (1, 10), 'phi2': (0, np.pi / 6), 'x02': (0, 10)}))

    # Start the application
    w = Widget(pair)
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
