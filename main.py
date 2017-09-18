import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, \
    QVBoxLayout, QWidget
import pyqtgraph as pg
import numpy as np
from inspect import signature
from matplotlib.colors import CSS4_COLORS


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
        self.label.setText("{0}={1:.4g}".format(self.name, self.value))


class Widget(QWidget):
    """Plotting widget"""

    def __init__(self, pairs, domain=np.linspace(0, 5, 1000),
                 win_title='', plt_title='', parent=None):

        super(Widget, self).__init__(parent=parent)

        self.pairs = pairs  # Function and control parameters
        self.domain = domain
        self.win_title = win_title
        self.plt_title = plt_title
        self.colors = tuple(CSS4_COLORS.values())

        self.horizontalLayout = QHBoxLayout(self)

        self.win = pg.GraphicsWindow(title=self.win_title)
        self.palette = self.win.addPlot(title=self.plt_title)
        self.palette.setLabel('left', 'y')
        self.palette.setLabel('bottom', 'x')
        self.horizontalLayout.addWidget(self.win)

        # Construct the sliders
        self.funcs = []
        for func, params in self.pairs:
            if func and params:
                self.palette.addLegend(offset=np.random.randint(100))
                func.curve = self.palette.plot(pen=self.colors[np.random.randint(138)],
                                               name=func.__name__)  # Plot the curve
                func.sliders = []
                for parameter, interval in params.items():
                    min_val, max_val = interval
                    slider = Slider(min_val, max_val, name=parameter)
                    self.horizontalLayout.addWidget(slider)
                    func.sliders.append(slider)
                self.funcs.append(func)

        self.update()

        for func in self.funcs:
            control_sliders = func.sliders
            for control_slider in control_sliders:
                control_slider.slider.valueChanged.connect(lambda: self.update())

    def update(self):
        for func in self.funcs:
            curve = func.curve
            control_sliders = func.sliders
            sig = signature(func)
            params = dict()
            for control_slider in control_sliders:
                if control_slider.name in sig.parameters.keys():
                    params[control_slider.name] = control_slider.value
            data = func(self.domain, **params)
            curve.setData(x=self.domain, y=data)


if __name__ == '__main__':
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
            (f2, {'k2': (1, 10), 'alpha2': (0, 1), 'f02': (1, 10), 'phi2': (0, np.pi/6), 'x02': (0, 10)}))

    # Start the application
    w = Widget(pair)
    w.show()
    sys.exit(app.exec_())
