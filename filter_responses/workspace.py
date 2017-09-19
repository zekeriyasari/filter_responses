# https://pythonspot.com/en/pyqt5-grid-layout/
from filter_responses.pyqtgraph_gui import *
from PyQt5.QtWidgets import QGroupBox, QGridLayout


class SliderBlock(QWidget):
    """
    Group of Sliders
    """

    def __init__(self, sliders):
        super().__init__()
        self.sliders = sliders
        self.horizontalLayout = QHBoxLayout(self)
        for slider in self.sliders:
            self.horizontalLayout.addWidget(slider)


class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.win_sliders = self.construct_sliders()
        self.win_mag = self.construct_graphics_window(plot_title='Magnitude Response', xlabel='w[rad/sec]',
                                                      ylabel='Magnitude')
        self.win_phase = self.construct_graphics_window(plot_title='Magnitude Response', xlabel='w[rad/sec]',
                                                      ylabel='Magnitude')
        self.win_nyq = self.construct_graphics_window(plot_title='Magnitude Response', xlabel='w[rad/sec]',
                                                      ylabel='Magnitude')
        self.wins = dict(sliders=self.win_sliders, graphs=(self.win_mag, self.win_phase, self.win_nyq))

        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()

        self.horizontalGroupBox.setLayout(layout)
        window_layout = QVBoxLayout()
        window_layout.addWidget(self.horizontalGroupBox)
        self.setLayout(window_layout)

    def construct_layout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        num_wins = len(self.wins)
        for win in self.wins:

    def construct_sliders(self, num=1):
        """Get control sliders"""
        return SliderBlock([Slider() for i in range(num)])

    def construct_graphics_window(self, window_title='', plot_title='', xlabel='', ylabel=''):
        """Get a graphic window."""
        win = pg.GraphicsWindow(title=window_title)
        win.palette = win.addPlot(title=plot_title)
        win.palette.setLabel('left', ylabel)
        win.palette.setLabel('bottom', xlabel)
        return win


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # gui = SliderBlock([Slider() for i in range(10)])
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
