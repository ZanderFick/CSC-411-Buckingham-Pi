try:
        import wx
        import wx.grid as gridlib
        import wx.lib.plot as plot
except ImportError:
    raise ImportError("wxpython module required!")
try:
        import svd_PI_finder as PI
except ImportError:
    raise ImportError("PI_Finder module required!")

from pandas import *

import numpy as np

import csv


class Pi_interface(wx.Frame):
    Data = []
    var_val_matrix = []

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 700))
        self.parent = parent
        Pi_interface.updating_columns = False

        self.initialize()

    def initialize(self):

        panel = wx.Panel(self, 1, (10, 20), style=wx.SUNKEN_BORDER)

        menu = wx.MenuBar()
        filemenu = wx.Menu()
        fileimport = filemenu.Append(wx.ID_OPEN, '&Import', 'Import Variable Data')
        filesave = filemenu.Append(wx.ID_SAVE, '&Save', 'Save Variable and Pi Group Data')
        filemenu.AppendSeparator()
        filereset = filemenu.Append(wx.ID_RESET, '&Reset', 'Clear all data and reset fields')
        filemenu.AppendSeparator()
        filequit = filemenu.Append(wx.ID_EXIT, 'Quit', 'Close Pi Finder')

        menu.Append(filemenu,  '&File')
        self.SetMenuBar(menu)

        self.Bind(wx.EVT_MENU, self.reset, filereset)
        self.Bind(wx.EVT_MENU, self.quit, filequit)
        self.Bind(wx.EVT_MENU, self.import_data, fileimport)

        self.Button_permute = wx.Button(panel, -1, "Permute Pi Groups", (605, 30))
        self.Button_plot = wx.Button(panel, -1, "Plot relations", (605, 300))

        ColLabels = ["Name", "L", "T", "M", u"\u03F4", "N", "I", "J"]

        Ncols = len(ColLabels)
        Nrows_initial = 1

        Pi_interface.values = gridlib.Grid(panel)
        Pi_interface.values.CreateGrid(Nrows_initial, Ncols)
        Pi_interface.values.SetSize((600, 300))

        Pi_interface.values.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange,)
        self.Button_permute.Bind(wx.EVT_BUTTON, self.permute)
        self.Button_plot.Bind(wx.EVT_BUTTON, self.plot)

        for column, name in enumerate(ColLabels):
            Pi_interface.values.SetColLabelValue(column, name)

        Pi_interface.values.AutoSizeColumns()

        for r in range(Nrows_initial):
            for c in range(8, Ncols):
                Pi_interface.values.SetReadOnly(r, c)

    def OnCellChange(self, event):
        if Pi_interface.updating_columns:
            return

        Nrows = Pi_interface.values.GetNumberRows()
        Ncols = Pi_interface.values.GetNumberCols()

        rcount = 0

        for r in range(0, Nrows):
            val = Pi_interface.values.GetCellValue(r, 0)
            if val != '':
                rcount += 1

        self.input_mat = np.zeros([rcount, 7]).T

        for update_col in range(1, 7):
            for update_row in range(0, rcount):
                val = Pi_interface.values.GetCellValue(update_row, update_col)
                if val != '':
                    self.input_mat[update_col-1, update_row] = val
        if Nrows > 1:
            self.input_fixed = self.input_mat[self.input_mat.any(1)].T
            self.Result = PI.buck(self.input_fixed)

        if Nrows > 2:
            val = Pi_interface.values.GetCellValue(Nrows-2, 0)
            if val == '':
                Pi_interface.updating_columns = True
                Pi_interface.values.DeleteRows(Nrows-2)
                Pi_interface.updating_columns = False

        val = Pi_interface.values.GetCellValue(Nrows-1, 0)

        if val != '':
            Pi_interface.updating_columns = True
            Pi_interface.values.InsertRows(Nrows, 1)
            Pi_interface.updating_columns = False

            for entry_row_check in range(0, Nrows):
                for add in range(1, 8):
                    val = Pi_interface.values.GetCellValue(entry_row_check, add)
                    if val == '' or val == '0':
                        Pi_interface.values.SetCellValue(entry_row_check, add, '0')

        if self.Result is not None:
            [res_rows, res_cols] = self.Result.shape
            self.Permute_Result = np.matrix(np.zeros([res_rows, 1]))
        else:
            res_cols = 0
            res_rows = 0

        coldelt = res_cols-(Ncols-8)

        if coldelt > 0:
            Pi_interface.updating_columns = True
            Pi_interface.values.InsertCols(Ncols, coldelt)
            Pi_interface.updating_columns = False

        elif coldelt < 0:
            Pi_interface.updating_columns = True
            Pi_interface.values.DeleteCols(Ncols+coldelt, abs(coldelt))
            Pi_interface.updating_columns = False

        for resR in range(0, res_rows):
            for colR in range(0, res_cols):
                val = "%g" % round(self.Result[resR, colR], 2)
                Pi_interface.values.SetCellValue(resR, colR+8, val)

        for colup in range(0, res_cols):
            colupdate = colup + 8
            name = u'\u03A0%g' % (colup + 1)
            Pi_interface.values.SetColLabelValue(colupdate, name)
            for rowupdate in range(0, Nrows):
                col = (255, 130, 0)
                Pi_interface.values.SetCellBackgroundColour(rowupdate, colupdate, col)
        Pi_interface.updating_columns = True
        Pi_interface.values.AutoSizeColumns()
        Pi_interface.updating_columns = False

    def permute(self, event):
        res_shape = self.Result.shape
        if res_shape[1] > 1:
            new_group = np.zeros([res_shape[0], 1])
            for iter_r in range(0, res_shape[1]):
                rand = np.random.randint(-1, 2)
                new = np.matrix(self.Result[:, iter_r]).T
                new_group += rand*new
                self.Permute_Result = np.hstack((self.Permute_Result, new_group))
            self.Permute_Result = DataFrame(self.Permute_Result.T).drop_duplicates().values.T
            self.Permute_Result = self.Permute_Result.T[self.Permute_Result.T.any(1)].T

            perm_shape = self.Permute_Result.shape

            Nrows = Pi_interface.values.GetNumberRows()
            Ncols = Pi_interface.values.GetNumberCols()

            delt = perm_shape[1] - (Ncols - res_shape[1] - 8)

            if delt > 0:
                Pi_interface.updating_columns = True
                Pi_interface.values.InsertCols(Ncols, delt)
                Pi_interface.updating_columns = False

                for colup in range(0, perm_shape[1]):
                    colupdate = colup + 8 + res_shape[1]
                    name = u'\u03A0%g' % (colup + 1 + res_shape[1])
                    Pi_interface.values.SetColLabelValue(colupdate, name)
                    for rowupdate in range(0, Nrows):
                        col = (70, 140, 255)
                        Pi_interface.values.SetCellBackgroundColour(rowupdate, colupdate, col)

                for res_permR in range(0, perm_shape[0]):
                    for col_permR in range(0, perm_shape[1]):
                        val = "%g" % round(self.Permute_Result[res_permR, col_permR], 2)
                        Pi_interface.values.SetCellValue(res_permR, col_permR+8+res_shape[1], val)

        Pi_interface.updating_columns = True
        Pi_interface.values.AutoSizeColumns()
        Pi_interface.updating_columns = False

    def import_data(self, event):
        Browser().Show()

    def plot(self, event):
        print ""

    def reset(self, event):
        Nrows = Pi_interface.values.GetNumberRows()
        Ncols = Pi_interface.values.GetNumberCols()
        self.input_mat = []
        self.input_fixed = []
        self.Result = []
        self.Permute_Result = []
        if Nrows > 1:
            Pi_interface.updating_columns = True
            Pi_interface.values.DeleteRows(0, Nrows-1)
            Pi_interface.updating_columns = False
        if Ncols > 8:
            Pi_interface.updating_columns = True
            Pi_interface.values.DeleteCols(8, Ncols-8)
            Pi_interface.updating_columns = False

    def quit(self, event):
        self.Close()


class Browser(Pi_interface, wx.Frame):
    def __init__(self):

        wx.Frame.__init__(self, wx.GetApp().TopWindow, title='Browse for data', size=(400, 300))
        bpanel = wx.Panel(self, -1)
        tbox = wx.BoxSizer(wx.HORIZONTAL)
        bbox = wx.BoxSizer(wx.HORIZONTAL)
        box = wx.BoxSizer(wx.VERTICAL)

        self.browser = wx.GenericDirCtrl(bpanel, 0, size=(250, 200))
        tbox.Add(self.browser, 1, wx.ALL, 10)

        bbox.Add(wx.Button(bpanel, 1, 'Import'), 0)
        bbox.Add(wx.Button(bpanel, 2, 'Close'), 0)
        box.Add(tbox)
        box.Add(bbox, 1, wx.LEFT, 10)

        bpanel.SetSizer(box)

        self.Bind(wx.EVT_BUTTON, self.Import, id=1)
        self.Bind(wx.EVT_BUTTON, self.close, id=2)

        self.path = ''

    def Import(self, event):
        self.path = self.browser.GetFilePath()
        filedata = []
        if self.path != '':
            with open(self.path, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                for row in reader:
                    if filedata == []:
                        filedata = row
                    else:
                        filedata = np.vstack((filedata, row))

                Pi_interface.Data = filedata
                Browser.read_in(self)
            self.Close()

    def close(self, event):
        self.Close()

    def read_in(self):

        Pi_interface.reset(self, self.reset)
        datashape = Pi_interface.Data.shape

        var_name_matrix = Pi_interface.Data[0, :]
        Pi_interface.var_val_matrix = np.array(Pi_interface.Data[1:8, 1:], dtype='f')

        Pi_interface.updating_columns = True
        Pi_interface.values.InsertRows(0, datashape[1]-1)
        Pi_interface.updating_columns = False

        for row in range(1, datashape[1]):
            Pi_interface.values.SetCellValue(row-1, 0, var_name_matrix[row])
            for col in range(1, datashape[0]):
                Pi_interface.values.SetCellValue(row-1, col, '0')

        Pi_interface.OnCellChange(self, self.OnCellChange)


class Plotwindow(Pi_interface, wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title='Browse for data', size=(400, 300))
        plot_panel = wx.panel(self, -1)
        self.canvas = plot.PlotCanvas(plot_panel)
        self.canvas.Draw(self.createPlotGraphics())

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        plot_panel.SetSizer(sizer)


if __name__ == "__main__":
    app = wx.App()
    frame = Pi_interface(None, -1, 'PI Finder GUI').Show()
    app.MainLoop()