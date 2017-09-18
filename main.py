import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, \
    QVBoxLayout, QWidget
import pyqtgraph as pg
import numpy as np
from inspect import signature


class Slider(QWidget):
    """Slider widget"""

    def __init__(self, minimum, maximum, name='', parent=None):
        super(Slider, self).__init__(parent=parent)

        self.name = name
        self.minimum = minimum
        self.maximum = maximum
        self.value = None

        self.verticalLayout = QVBoxLayout(self)
        self.horizontalLayout = QHBoxLayout()
        self.label = QLabel(self)
        self.slider = QSlider(self)

        self.verticalLayout.addWidget(self.label)

        spacerItem = QSpacerItem(0, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        spacerItem1 = QSpacerItem(0, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.slider.setOrientation(Qt.Vertical)
        self.horizontalLayout.addWidget(self.slider)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.resize(self.sizeHint())
        self.slider.valueChanged.connect(self.set_label_value)
        self.set_label_value(self.slider.value())

    def set_label_value(self, value):
        self.value = self.minimum + (float(value) / (self.slider.maximum() - self.slider.minimum())) * (
            self.maximum - self.minimum)
        self.label.setText("{0:.4g}".format(self.value))


class Widget(QWidget):
    """Plotting widget"""
    def __init__(self, func, control_sliders, domain=np.linspace(0, 10, 1000),
                 win_title='', plt_title='', color='r', parent=None):

        super(Widget, self).__init__(parent=parent)

        self.func = func
        self.control_sliders = control_sliders
        self.domain = domain
        self.win_title = win_title
        self.plt_title = plt_title
        self.color = color

        self.horizontalLayout = QHBoxLayout(self)

        for control_slider in self.control_sliders:
            self.horizontalLayout.addWidget(control_slider)

        self.win = pg.GraphicsWindow(title=self.win_title)
        self.horizontalLayout.addWidget(self.win)
        self.p6 = self.win.addPlot(title=self.plt_title)
        self.p6.setLabel('left', 'y')
        self.p6.setLabel('bottom', 'x')
        self.curve = self.p6.plot(pen=self.color)

        self.update()
        for control_slider in self.control_sliders:
            control_slider.slider.valueChanged.connect(lambda: self.update())

    def update(self):
        sig = signature(self.func)
        params = dict()
        for control_slider in self.control_sliders:
            if control_slider.name in sig.parameters.keys():
                params[control_slider.name] = control_slider.value
        data = self.func(self.domain, **params)
        self.curve.setData(x=self.domain, y=data)


if __name__ == '__main__':
    # Launch Qt GUI application
    app = QApplication(sys.argv)

    # Test function
    def f(x, k=1., alpha=0.5, f0=1., phi=0., x0=0.):
        return k * np.exp(-alpha * x) * np.cos(2 * np.pi * f0 * x + phi) + x0

    # Control sliders of test function.
    amplitude_slider = Slider(1, 10, name='k')
    damping_slider = Slider(0, 1, name='alpha')
    frequency_slider = Slider(1, 10, name='f0')
    phase_slider = Slider(0., np.pi, name='phi')
    offset_slider = Slider(0, 10, name='x0')
    control_sliders = (amplitude_slider, damping_slider, frequency_slider, phase_slider, offset_slider)

    # Start the application
    w = Widget(f, control_sliders)
    w.show()
    sys.exit(app.exec_())
