class PlotData:
    def __init__(self, met_a, a_e, x_r, x_ind):
        self.met_a = met_a
        self.a_e = a_e
        self.x_r = x_r
        self.x_ind = x_ind

    def set_met_a(self, data):
        self.met_a.set_data(data)

    def set_y_met_a(self, data):
        self.met_a.set_ydata(data)

    def set_y_a_e(self, data):
        self.a_e.set_ydata(data)

    def set_a_e(self, data):
        self.a_e.set_data(data)