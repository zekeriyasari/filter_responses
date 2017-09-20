# https://pythonspot.com/en/pyqt5-grid-layout/
from filter_responses.gui_widgets import *
from filter_responses.filter_prototypes import *
from PyQt5.QtWidgets import QGroupBox, QGridLayout


class GUI(QWidget):
    def __init__(self, pairs, domain=np.linspace(0, 5, 1000), log_scale=False,
                 win_labels=(), ):
        super().__init__()
        self.pairs = pairs
        self.domain = domain
        self.log_scale = log_scale
        self.win_labels = win_labels
        self.colors = tuple(CSS4_COLORS.values())

        # Match GUI windows with functions and sliders
        self.gui_wins = []
        self.gui_sliders = []
        for win_label in self.win_labels.keys():
            win = self.get_graphics_window(label=win_label, log_scale=self.log_scale)
            win.funcs = []
            for func, params in self.pairs:
                func(0)  # Dummy call to label the func.
                if func.label == win_label:
                    pen_color = self.colors[np.random.randint(138)]
                    func.curve = win.palette.plot(pen=pen_color,
                                                  name=func.__name__)  # Plot the curve
                    win.funcs.append(func)
                    if params:
                        func.sliders = []  # Function sliders to control parameters of func
                        for parameter, interval in params.items():
                            min_val, max_val = interval
                            slider = Slider(min_val, max_val, name=parameter, color=pen_color, data_type=type(min_val))
                            # self.horizontalLayout.addWidget(slider)
                            func.sliders.append(slider)
                            self.gui_sliders.append(slider)
            self.gui_wins.append(win)

        # Construct the layout of GUI.
        self.gui_wins = tuple(self.gui_wins)
        self.gui_sliders = SliderBlock(self.gui_sliders)
        num_cols = 2  # Two-column GUI
        num_rows = int((len(self.gui_wins) + 1) / 2)
        self.construct_layout(layout_shape=(num_rows, num_cols))

        # Plot the curves
        self.update()

        # Start the interaction
        for win in self.gui_wins:
            for func in win.funcs:
                control_sliders = func.sliders
                for control_slider in control_sliders:
                    control_slider.slider.valueChanged.connect(lambda: self.update())

    def construct_layout(self, layout_shape=(1, 1)):
        self.horizontalGroupBox = QGroupBox("Grid")
        windows = (self.gui_sliders, *self.gui_wins)
        layout = QGridLayout()
        num_rows, num_cols = layout_shape
        counter = 0
        for row in range(num_rows):
            for col in range(num_cols):
                layout.addWidget(windows[counter], row, col)
                counter += 1
        self.horizontalGroupBox.setLayout(layout)
        window_layout = QVBoxLayout()
        window_layout.addWidget(self.horizontalGroupBox)
        self.setLayout(window_layout)

    def get_graphics_window(self, window_title='', plot_title='', xlabel='', ylabel='', label='', log_scale=False):
        """Get a graphic window."""
        win = pg.GraphicsWindow(title=window_title)
        win.palette = win.addPlot(title=self.win_labels[label][0])
        win.palette.setLabel('bottom', self.win_labels[label][1])
        win.palette.setLabel('left', self.win_labels[label][2])
        win.palette.addLegend(offset=np.random.randint(100))
        win.palette.showGrid(x=True, y=True)
        if log_scale:
            win.palette.setLogMode(x=True, y=False)
        win.label = label
        return win

    def update(self):
        for win in self.gui_wins:
            for func in win.funcs:
                curve = func.curve
                control_sliders = func.sliders
                sig = signature(func)
                params = dict()
                for control_slider in control_sliders:
                    if control_slider.name in sig.parameters.keys():
                        params[control_slider.name] = control_slider.value
                func_ = partial(func, **params)
                # data = np.array([func_(x) for x in self.domain]).flatten()  # Iterative calculation may be slow!
                data = func_(self.domain)
                curve.setData(x=data[0], y=data[1])


def main():
    # Launch Qt GUI application
    app = QApplication(sys.argv)

    # Test function
    def f1(x, k1=1., alpha1=0.5, f01=1., phi1=0., x01=0.):
        f1.label = 'mag'
        return k1 * np.exp(-alpha1 * x) * np.cos(2 * np.pi * f01 * x + phi1) + x01

    # Test function
    def f2(x, k2=1., alpha2=0.5, f02=1., phi2=0., x02=0.):
        f2.label = 'mag'
        return k2 * np.exp(-alpha2 * x) * np.sin(2 * np.pi * f02 * x + phi2) + x02

        # Test function

    def f3(x, k3=1., alpha3=0.5, f03=1., phi3=0., x03=0.):
        f3.label = 'mag'
        return k3 * np.exp(-alpha3 * x) * np.cos(2 * np.pi * f03 * x + phi3) + x03

        # Test function

    def f4(x, k4=1., alpha4=0.5, f04=1., phi4=0., x04=0.):
        f4.label = 'mag'
        return k4 * np.exp(-alpha4 * x) * np.sin(2 * np.pi * f04 * x + phi4) + x04

    def f5(x, k5=1., alpha5=0.5, f05=1., phi5=0., x05=0.):
        f5.label = 'mag'
        return k5 * np.exp(-alpha5 * x) * np.cos(2 * np.pi * f05 * x + phi5) + x05

        # Test function

    def f6(x, k6=1., alpha6=0.5, f06=1., phi6=0., x06=0.):
        f6.label = 'mag'
        return k6 * np.exp(-alpha6 * x) * np.sin(2 * np.pi * f06 * x + phi6) + x06

    # Control sliders of test function.
    pair = (
        (f1, {'alpha1': (0, 1), 'f01': (1, 10)}),
        (f2, {'alpha1': (0, 1), 'f02': (1, 10)}),
        (f3, {'alpha2': (0, 1), 'f03': (1, 10)}),
        (f4, {'alpha2': (0, 1), 'f04': (1, 10)}),
        (f5, {'alpha3': (0, 1), 'f05': (1, 10)}),
        (f6, {'alpha3': (0, 1), 'f06': (1, 10)})
    )

    # Start the application
    w = GUI(pair, win_labels=('mag', 'phase', 'nyq'))
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # Launch the Qt application.
    app = QApplication(sys.argv)


    def butter_hw_mag(w, n=4):
        n = int(n)
        if not hasattr(butter_hw_mag, 'label'):
            butter_hw_mag.label = 'mag'
        a, b = signal.butter(n, 1., btype='low', analog=True)
        filter_func = hw2hwmag(hs2hw(coefficients2hs(a, b[::-1], n=n)))
        return w, filter_func(w)


    def butter_hw_phase(w, n=4):
        n = int(n)
        if not hasattr(butter_hw_phase, 'label'):
            butter_hw_phase.label = 'phase'
        a, b = signal.butter(n, 1., btype='low', analog=True)
        filter_func = hw2hwphase(hs2hw(coefficients2hs(a, b[::-1], n=n)))
        return w, filter_func(w)


    def cheby_hw_mag(w, n=4, eps=1.):
        n = int(n)
        if not hasattr(cheby_hw_mag, 'label'):
            cheby_hw_mag.label = 'mag'
        a, b = signal.cheby1(n, eps, 1., btype='low', analog=True)
        filter_func = hw2hwmag(hs2hw(coefficients2hs(a, b[::-1], n=n)))
        return w, filter_func(w)


    def cheby_hw_phase(w, n=4, eps=1.):
        n = int(n)
        if not hasattr(cheby_hw_phase, 'label'):
            cheby_hw_phase.label = 'phase'
        a, b = signal.cheby1(n, eps, 1., btype='low', analog=True)
        filter_func = hw2hwphase(hs2hw(coefficients2hs(a, b[::-1], n=n)))
        return w, filter_func(w)


    def butter_hw_nyquist(w, n=4):
        n = int(n)
        if not hasattr(butter_hw_nyquist, 'label'):
            butter_hw_nyquist.label = 'nyquist'
        _, theta = butter_hw_phase(w, n=n)
        _, r = butter_hw_mag(w, n=n)
        return r * np.cos(theta), r * np.sin(theta)


    def cheby_hw_nyquist(w, n=4, eps=1.):
        n = int(n)
        if not hasattr(cheby_hw_nyquist, 'label'):
            cheby_hw_nyquist.label = 'nyquist'
        _, theta = cheby_hw_phase(w, n=n, eps=eps)
        _, r = cheby_hw_mag(w, n=n)
        return r * np.cos(np.deg2rad(theta)), r * np.sin(np.deg2rad(theta))


    pair = ((butter_hw_mag, {'n': (1, 10)}),
            (butter_hw_phase, {'n': (1, 10)}),
            (cheby_hw_mag, {'n': (1, 10), 'eps': (0.1, 5.)}),
            (cheby_hw_phase, {'n': (1, 10), 'eps': (0.1, 5.)}),
            (butter_hw_nyquist, {'n': (1, 10)}),
            (cheby_hw_nyquist, {'n': (1, 10), 'eps': (0.1, 5.)}))

    # Start the application
    w = GUI(pair, domain=np.linspace(0, 5, 5000),
            win_labels={'mag': ('Magnitude Response', 'w[rad/sec]', 'Magnitude'),
                        'phase': ('Phase Response', 'w[rad/sec]', 'Phase[degree]'),
                        'nyquist': ('Nyquist Plot', 'Amplitude', 'Amplitude')})
    w.show()
    sys.exit(app.exec_())
