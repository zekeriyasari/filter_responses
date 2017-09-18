import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, \
    QVBoxLayout, QWidget

import pyqtgraph as pg
import numpy as np
from inspect import signature
from functools import partial


class Slider(QWidget):
    """Slider object."""

    def __init__(self, minimum, maximum, name=''):
        super(Slider, self).__init__()

        self.minimum = minimum
        self.maximum = maximum
        self.name = name
        self.value = None

        self.verticalLayout = QVBoxLayout(self)  # Vertical layout
        self.horizontalLayout = QHBoxLayout()  # Horizontal layout
        self.slider = QSlider(self)  # Slider
        self.label = QLabel(self)  # Label

        self.verticalLayout.addWidget(self.label)

        spacerItem = QSpacerItem(0, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.slider.setOrientation(Qt.Vertical)
        self.horizontalLayout.addWidget(self.slider)

        spacerItem1 = QSpacerItem(0, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.resize(self.sizeHint())

        self.slider.valueChanged.connect(self.set_label_value)
        self.setLabelValue(self.slider.value())

    def set_label_value(self, value):
        """Set label of the Slider."""
        self.value = self.minimum + (float(value) / (self.slider.maximum() - self.slider.minimum())) * (
            self.maximum - self.minimum)
        self.label.setText("{0:.4g}".format(self.value))


class Widget(QWidget):
    """
    Plotting GUI of a function with control variables.
    """

    def __init__(self, f, slider_controls, domain=np.linspace(0, 1, 1000), win_title='', plot_title='', color='r'):
        super(Widget, self).__init__()

        self.f = f  # Function to be called
        self.slider_controls = slider_controls
        self.domain = domain
        self.win_title = win_title
        self.plot_title = plot_title
        self.color = color

        self.horizontalLayout = QHBoxLayout(self)

        for slider_control in self.slider_controls:
            self.horizontalLayout.addWidget(slider_control)

        self.win = pg.GraphicsWindow(title=self.win_title)
        self.horizontalLayout.addWidget(self.win)
        self.p6 = self.win.addPlot(title=self.plot_title)
        self.curve = self.p6.plot(pen=self.color)

        # Update the curve of the plot.
        self.update()

        for slider_control in self.slider_controls:
            slider_control.slider.valueChanged.connect(lambda: self.update())

    def update(self):
        """Read slider values and update the curve of the function"""
        sig = signature(self.f)
        func_params = sig.parameters.keys()[1:]  # It is assumed that the first parameter is not keyword.
        kwargs = dict()
        for slider_control in self.slider_controls:
            if slider_control.name in func_params:
                kwargs[slider_control.label] = slider_control.value
        data = self.f(self.domain, **kwargs)
        self.curve.setData(data)

        # TODO: Read the sliders and wrap self.f accordingly.
        # func = partial(self.f, *args, **kwargs)
        # k = self.w1.x
        # alpha = self.w2.x
        # f = self.w3.x
        # phi = self.w4.x
        # x0 = self.w5.x

        # data = self.f(self.domain, k=k, alpha=alpha, f=f, phi=phi, x0=x0)
        # self.curve.setData(data)


def test_gui():
    """Test function for the GUI"""

    # Test function
    def f(t, k=1., alpha=0.5, f0=1., phi=0., x0=0.):
        return k * np.exp(-alpha * t) * np.cos(2 * np.pi * f0 * t + phi) + x0

    # Sliders
    amplitude_slider = Slider(1, 10)
    damping_slider = Slider(0, 1)
    frequency_slider = Slider(1, 10)
    phase_slider = Slider(0, np.pi)
    offset_slider = Slider(0, 10)
    sliders = [amplitude_slider, damping_slider, frequency_slider, phase_slider, offset_slider]

    # Start the GUI
    app = QApplication(sys.argv)
    w = Widget(f, sliders)
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test_gui()
