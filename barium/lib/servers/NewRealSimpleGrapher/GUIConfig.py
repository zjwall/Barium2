'''
Configuration settings for Grapher gui
'''
import pyqtgraph as pg
pg.setConfigOption('background', 'k')
pg.setConfigOption('foreground', 'y')

class traceListConfig():
    def __init__(self, background_color = 'white'):
        self.background_color = background_color

class graphConfig():
    def __init__(self, name, ylim=[0,1], isScrolling=False, max_datasets = 20,
                 show_points = True, grid_on = True, scatter_plot='all', isImages=False,
                 isHist=False, line_param=None, vline=None, vline_param=None, hline=None, hline_param=None):
        self.name = name
        self.ylim = ylim
        self.isScrolling = isScrolling
        self.max_datasets = max_datasets
        self.graphs = 1 # just a single graph
        self.show_points = show_points
        self.grid_on = grid_on
        self.scatter_plot = scatter_plot
        self.isImages = isImages
        self.isHist = isHist
        self.line_param = line_param
        self.vline = vline
        self.vline_param = vline_param
        self.hline = hline
        self.hline_param = hline_param


class gridGraphConfig():
    def __init__(self, tab, config_list):
        self.tab = tab
        self.config_list = config_list[0::3]
        self.row_list = config_list[1::3]
        self.column_list = config_list[2::3]

        self.graphs = len(self.config_list)


tabs =[
    #gridGraphConfig('TOF_Trace', [graphConfig('TOF_Trace', max_datasets = 50, show_points=False), 0, 0]),
    gridGraphConfig('PMT', [graphConfig('pmt', ylim=[0,30], isScrolling=True, max_datasets = 1, show_points = False), 0, 0]),
    gridGraphConfig('Laser_Monitor', [graphConfig('Laser Monitor',isScrolling=True, max_datasets = 50, show_points=False), 0, 0]),
    gridGraphConfig('MM', [graphConfig('mm_compensation', show_points = True), 0, 0,]),
    gridGraphConfig('spectrum', [graphConfig('spectrum', show_points = True), 0, 0]),
    #gridGraphConfig('Laser Monitor', [graphConfig('Laser Monitor' , show_points = False, isScrolling=True), 0, 0]),
    #gridGraphConfig('Mass Spectrum', [graphConfig('Mass_Spec' , show_points = True), 0, 0]),
    gridGraphConfig('Rabi/Ramsey', [graphConfig('rabi_flopping', show_points = True), 0, 0,]),
    gridGraphConfig('Tickle', [graphConfig('tickle_sweep', show_points = True), 0, 0,]),
    gridGraphConfig('Qubit Freq Sweep', [graphConfig('qubit_freq_sweep' , show_points = True), 0, 0]),
    gridGraphConfig('bright/dark', [graphConfig('bright/dark' ,isScrolling=True, show_points = True), 0, 0]),
    gridGraphConfig('Shelving', [graphConfig('shelving', isScrolling=True, max_datasets = 10, show_points = True), 0, 0,]),
    #gridGraphConfig('High_Fidelity',[
                      #graphConfig('Threshold', isScrolling=True, show_points = True), 0, 0,
                      #graphConfig('ML', isScrolling=True, show_points = True), 1, 0,])]
    ]
'''
    gridGraphConfig('rabi', [graphConfig('rabi'), 0, 0]),
    gridGraphConfig('calibrations', [
                      graphConfig('car1'), 0, 0,
                      graphConfig('car2'), 0, 1,
                      graphConfig('radial1'), 1, 0,
                      graphConfig('radial2'), 1, 1]),
    gridGraphConfig('molmer-sorensen',[
                      graphConfig('ms_time'), 0, 0]),

    gridGraphConfig('vaet',[
                      graphConfig('vaet_time'), 0, 0,
                      graphConfig('vaet_delta'), 0, 1]),

    gridGraphConfig('local_stark',[
                      graphConfig('ms_local_stark'), 0, 0,
                      graphConfig('ms_local_stark_detuning'), 1, 0,
                      graphConfig('vaet_local_stark'), 0, 1,
                      graphConfig('vaet_local_stark_detuning'), 1, 1]),

    gridGraphConfig('parity', [graphConfig('parity'), 0, 0]),
    gridGraphConfig('ramsey', [graphConfig('ramsey'), 0, 0])

#    gridGraphConfig('testgrid',
#        [
#            graphConfig('fig1'), 0, 0,
#            graphConfig('fig2'), 0, 1,
#            graphConfig('fig3'), 2, 2,
#            graphConfig('fig4'), 1, 2
#        ]),
#    gridGraphConfig('testgrid2',
#        [
#            graphConfig('fig1123'), 0, 0,
#        ])
'''
