try:
        import wx
        import wx.grid as gridlib
        from wx.lib.plot import PlotCanvas, PlotGraphics, PolyMarker
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
    pi_val_matrix = []

    Result = None

    Filepath = ''

    plot_x = []
    x_name = ''

    plot_y = []
    y_name = ''

    dataset = []

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 700))
        self.parent = parent
        Pi_interface.updating_columns = False
        self.case = True

        self.initialize()

    def initialize(self):
        Sizer = wx.BoxSizer(wx.VERTICAL)
        Mainsizer = wx.BoxSizer(wx.HORIZONTAL)

        buttonsizer = wx.BoxSizer(wx.VERTICAL)
        righthandsizer = wx.BoxSizer(wx.VERTICAL)

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

        self.Bind(wx.EVT_MENU, self.import_data, fileimport)
        self.Bind(wx.EVT_MENU, self.save, filesave)
        self.Bind(wx.EVT_MENU, self.reset, filereset)
        self.Bind(wx.EVT_MENU, self.quit, filequit)

        self.Button_permute = wx.Button(self, -1, "Permute Pi Groups")
        self.Button_plot = wx.Button(self, -1, "Plot relations")

        ColLabels = ["Name", "L", "T", "M", u"\u03F4", "N", "I", "J"]

        Ncols = len(ColLabels)
        Nrows_initial = 1

        Pi_interface.values = gridlib.Grid(self)

        Pi_interface.values.CreateGrid(Nrows_initial, Ncols)

        self.Feedback = wx.Panel(self, -1, style=wx.BORDER)
        self.Feedbacktext = wx.StaticText(self.Feedback, label='Welcome!')

        self.SetBackgroundColour((230, 230, 230))
# Sizing

        Mainsizer.Add(Pi_interface.values, 1, wx.EXPAND)

        buttonsizer.Add(self.Button_permute, 1, wx.EXPAND)
        buttonsizer.Add(self.Button_plot, 1, wx.EXPAND)

        righthandsizer.Add(buttonsizer, 0.5, wx.EXPAND)

        Mainsizer.Add(righthandsizer, 0.5, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)

        Sizer.Add(Mainsizer, 1, wx.EXPAND)
        Sizer.Add(self.Feedback, 0.5, wx.EXPAND | wx.ALL)

        Pi_interface.values.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange,)
        Pi_interface.values.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.checkplot)

        self.Button_permute.Bind(wx.EVT_BUTTON, self.permute)
        self.Button_plot.Bind(wx.EVT_BUTTON, self.plot)

        self.SetSizer(Sizer)
        self.Center()

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
                    try:
                        self.input_mat[update_col-1, update_row] = val
                    except:
                        Pi_interface.changecell(self, update_row, update_col)

        if Nrows > 1:
            self.input_fixed = self.input_mat[self.input_mat.any(1)].T
            self.Result = PI.buck(self.input_fixed)

        if Nrows > 2:
            val = Pi_interface.values.GetCellValue(Nrows-2, 0)
            if val == '':
                Pi_interface.updating_columns = True
                Pi_interface.values.DeleteRows(Nrows-2)
                Pi_interface.updating_columns = False
                Pi_interface.read_only(self)

        val = Pi_interface.values.GetCellValue(Nrows-1, 0)

        if val != '':
            Pi_interface.updating_columns = True
            Pi_interface.values.InsertRows(Nrows, 1)
            Pi_interface.updating_columns = False
            Pi_interface.read_only(self)

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
            Pi_interface.read_only(self)

        elif coldelt < 0:
            Pi_interface.updating_columns = True
            Pi_interface.values.DeleteCols(Ncols+coldelt, abs(coldelt))
            Pi_interface.updating_columns = False
            Pi_interface.read_only(self)

        if self.Result is not None:
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
        Pi_interface.read_only(self)

    def permute(self, event):

        res_shape = self.Result.shape
        perm_shape = self.Permute_Result.shape

        Nrows = Pi_interface.values.GetNumberRows()
        Ncols = Pi_interface.values.GetNumberCols()

        if res_shape[1] > 1:
            new_group = np.zeros([res_shape[0], 1])
            New_Group_found = False
            Wait = 1000
            while not New_Group_found and Wait > 0:
                for iter_r in range(0, res_shape[1]):
                    random = np.random.randint(0, 1)
                    if random == 0:
                        rand = np.random.randint(-1, 1)
                    else:
                        rand = 1/max(new_group.any(1))
                    new = np.matrix(self.Result[:, iter_r]).T
                    new_group += rand*new

                    neg_test = 0

                    for count in range(0, res_shape[0]):
                        if new_group[count] != 0:
                            neg_test += new_group[count]/np.abs(new_group[count])
                        if new_group[count] == -0:
                            new_group[count] = 0

                    if neg_test < 0:
                        new_group[new_group.any(1)] = new_group[new_group.any(1)]/-1
                    try:
                        div_mask = new_group[abs(new_group) > 0.1]
                        div =  min(abs(div_mask))
                        if div != 0:
                            new_group[new_group.any(1)] = new_group[new_group.any(1)]/div
                    except:
                        new_group[new_group.any(1)] = new_group[new_group.any(1)]
                    results = Ncols - 8

                    uniqueness = np.zeros([results, 1])

                    for check_entry in range(0, results):
                        if check_entry < res_shape[1]:
                            compare = self.Result[:, check_entry]
                        elif check_entry >= res_shape[1]:
                            compare = self.Permute_Result[:, check_entry - res_shape[1]]
                        for check_vals in range(0, res_shape[0]):

                            abs_val = np.abs(new_group[check_vals, 0])
                            abs_check = np.abs(compare[check_vals])

                            if abs_val != abs_check:
                                uniqueness[check_entry] = 1

                    if (np.sum(uniqueness) - results) == 0:
                        New_Group_found = True
                        self.Permute_Result = np.hstack((self.Permute_Result, new_group))
                        self.Permute_Result = DataFrame(self.Permute_Result.T).drop_duplicates().values.T
                        self.Permute_Result = self.Permute_Result.T[self.Permute_Result.T.any(1)].T
                    Wait += -1

            perm_shape = self.Permute_Result.shape

            delt = perm_shape[1] - (Ncols - res_shape[1] - 8)

            if delt > 0:
                Pi_interface.updating_columns = True
                Pi_interface.values.InsertCols(Ncols, delt)
                Pi_interface.updating_columns = False
                Pi_interface.read_only(self)

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
        Pi_interface.read_only(self)

    def checkplot(self, event):

        row, col = event.GetRow(), event.GetCol()

        if (col > 7) or (row >= 0):
            if col > 7:
                self.name = Pi_interface.values.GetColLabelValue(col)
                self.choice = [-1, col]
            else:
                self.name = Pi_interface.values.GetCellValue(row, 0)
                self.choice = [row, -1]

            if not hasattr(self, "popupID1"):
                self.popupID1 = wx.NewId()
                self.popupID2 = wx.NewId()

            menu = wx.Menu()

            option = wx.MenuItem(menu, self.popupID1, "Choose " + self.name + " as X axis")
            menu.AppendItem(option)
            menu.Append(self.popupID2, "Choose " + self.name + " as Y axis")

            self.Bind(wx.EVT_MENU, self.x_select, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.y_select, id=self.popupID2)

            self.PopupMenu(menu)
            menu.Destroy()

    def changecell(self, row, col):
        Pi_interface.values.SetCellValue(row, col, '0')

    def x_select(self, event):

        if Pi_interface.plot_x != []:

            if Pi_interface.plot_x[0] == -1:
                Pi_interface.values.SetColLabelValue(Pi_interface.plot_x[1], u'\u03A0%g' % (Pi_interface.plot_x[1]-7))
                for row in range(0,  self.dim[1]):
                    if Pi_interface.plot_x[1] <= 7:
                        oldcolour = (255, 255, 255)
                    elif Pi_interface.plot_x[1] > 7 and Pi_interface.plot_x[1] <= (7 + self.Result.shape[1]):
                        oldcolour = (255, 130, 0)
                    else:
                        oldcolour = (70, 140, 255)
                    Pi_interface.values.SetCellBackgroundColour(row, Pi_interface.plot_x[1], oldcolour)
            else:
                Pi_interface.values.SetRowLabelValue(Pi_interface.plot_x[0], str(Pi_interface.plot_x[0]+1))
                for col in range(0,  self.dim[0]):
                    if col <= 7:
                        oldcolour = (255, 255, 255)
                        Pi_interface.values.SetCellBackgroundColour(Pi_interface.plot_x[0], col, oldcolour)
                    elif col > 7 and col <= (7 + self.Result.shape[1]):
                        oldcolour = (255, 130, 0)
                        Pi_interface.values.SetCellBackgroundColour(Pi_interface.plot_x[0], col, oldcolour)
                    else:
                        oldcolour = (70, 140, 255)
                        Pi_interface.values.SetCellBackgroundColour(Pi_interface.plot_x[0], col, oldcolour)

        Pi_interface.x_name = self.name

        self.dim = Pi_interface.values.GetNumberCols(), Pi_interface.values.GetNumberRows()

        Pi_interface.plot_x = self.choice

        colournew = (225, 255, 200)

        if self.choice[0] == -1:
            Pi_interface.values.SetColLabelValue(self.choice[1], 'X')
            for row in range(0,  self.dim[1]):
                Pi_interface.values.SetCellBackgroundColour(row, self.choice[1], colournew)
        else:
            Pi_interface.values.SetRowLabelValue(self.choice[0], 'X')
            for col in range(0,  self.dim[0]):
                Pi_interface.values.SetCellBackgroundColour(self.choice[0], col, colournew)

        Pi_interface.updating_columns = True
        Pi_interface.values.AutoSizeColumns()
        Pi_interface.updating_columns = False
        Pi_interface.read_only(self)

    def y_select(self, event):

        if Pi_interface.plot_y != []:

            if Pi_interface.plot_y[0] == -1:
                Pi_interface.values.SetColLabelValue(Pi_interface.plot_y[1],  u'\u03A0%g' % (Pi_interface.plot_y[1]-7))
                for row in range(0,  self.dim[1]):
                    if Pi_interface.plot_y[1] <= 7:
                        oldcolour = (255, 255, 255)
                    elif Pi_interface.plot_y[1] > 7 and Pi_interface.plot_y[1] <= (7 + self.Result.shape[1]):
                        oldcolour = (255, 130, 0)
                    else:
                        oldcolour = (70, 140, 255)
                    Pi_interface.values.SetCellBackgroundColour(row, Pi_interface.plot_y[1], oldcolour)
            else:
                Pi_interface.values.SetRowLabelValue(Pi_interface.plot_y[0], str(Pi_interface.plot_y[0]+1))
                for col in range(0,  self.dim[0]):
                    if col <= 7:
                        oldcolour = (255, 255, 255)
                        Pi_interface.values.SetCellBackgroundColour(Pi_interface.plot_y[0], col, oldcolour)
                    elif col > 7 and col <= (7 + self.Result.shape[1]):
                        oldcolour = (255, 130, 0)
                        Pi_interface.values.SetCellBackgroundColour(Pi_interface.plot_y[0], col, oldcolour)
                    else:
                        oldcolour = (70, 140, 255)
                        Pi_interface.values.SetCellBackgroundColour(Pi_interface.plot_y[0], col, oldcolour)

        Pi_interface.y_name = self.name

        self.dim = Pi_interface.values.GetNumberCols(), Pi_interface.values.GetNumberRows()

        Pi_interface.plot_y = self.choice

        colournew = (255, 200, 225)

        if self.choice[0] == -1:
            Pi_interface.values.SetColLabelValue(self.choice[1], 'Y')
            for row in range(0,  self.dim[1]):
                Pi_interface.values.SetCellBackgroundColour(row, self.choice[1], colournew)
        else:
            Pi_interface.values.SetRowLabelValue(self.choice[0], 'Y')
            for col in range(0,  self.dim[0]):
                Pi_interface.values.SetCellBackgroundColour(self.choice[0], col, colournew)

        Pi_interface.updating_columns = True
        Pi_interface.values.AutoSizeColumns()
        Pi_interface.updating_columns = False
        Pi_interface.read_only(self)

    def import_data(self, event):

        dialog = wx.FileDialog(self, message='Select file to import', defaultFile='', style=wx.OPEN | wx.CHANGE_DIR)
        if dialog.ShowModal() == wx.ID_OK:
            Pi_interface.Filepath = dialog.GetPath()
        dialog.Destroy()

        self.path = Pi_interface.Filepath
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
                Pi_interface.read_in(self)

    def plot(self, event):

        if Pi_interface.Data != [] and Pi_interface.plot_x != [] and Pi_interface.plot_y != [] :

            x_set = Pi_interface.plot_x
            y_set = Pi_interface.plot_y

            Pi_interface.calculate_pi_vals(self)

            if x_set and y_set:
                if x_set[0] == -1:
                    pi_pos = x_set[1] - 8
                    x_data = np.matrix(Pi_interface.pi_val_matrix[:, pi_pos])
                else:
                    x_data = np.matrix(Pi_interface.var_val_matrix[:, x_set[0]])

                if y_set[0] == -1:
                    pi_pos = y_set[1] - 8
                    y_data = np.matrix(Pi_interface.pi_val_matrix[:, pi_pos])
                else:
                    y_data = np.matrix(Pi_interface.var_val_matrix[:, y_set[0]])

                Plotwindow.h_label = 'Data Plot Window'

                points = np.concatenate((x_data, y_data), axis=0).T

                Pi_interface.dataset = PolyMarker(points, colour='black',  marker='triangle', size=1)

                Plotwindow().Show()
        else:
             wx.MessageBox('Please select a X and Y axis variable by right clicking the Row or Column label of the desired variable', 'Choose axes', wx.OK)

    def calculate_pi_vals(self):
        if self.Result != None:
            dim = self.var_val_matrix.shape
            res_cols = Pi_interface.values.GetNumberCols()-8
            add = np.zeros([dim[0], res_cols])

            for pi_iter in range(0, res_cols):
                if pi_iter < self.Result.shape[1]:
                    pi = self.Result[:, pi_iter]
                else:
                    pi = self.Permute_Result[:,  pi_iter - self.Result.shape[1]]
                for exp_iter in range(0, dim[0]):
                    exp = self.var_val_matrix[exp_iter]

                    new_val = 1
                    for val_iter in range(0, dim[1]):
                        if exp[val_iter] != 0 or pi[val_iter] != -1:
                            new_val = np.round(new_val*((np.abs(exp[val_iter]))**pi[val_iter]), 6)
                    add[exp_iter, pi_iter] = new_val

            Pi_interface.pi_val_matrix = add

    def reset(self, event):

        Nrows = Pi_interface.values.GetNumberRows()
        Ncols = Pi_interface.values.GetNumberCols()

        self.input_mat = []
        self.input_fixed = []
        self.Permute_Result = []

        if self.case:
            Pi_interface.Data = []

            Pi_interface.var_val_matrix = []
            Pi_interface.pi_val_matrix = []

            Pi_interface.Filepath = ''
            Pi_interface.dataset = [] 
            self.Result = None

        Pi_interface.plot_x = []
        Pi_interface.x_name = ''
        Pi_interface.plot_y = []
        Pi_interface.y_name = ''

        if Nrows > 1:
            Pi_interface.updating_columns = True
            Pi_interface.values.DeleteRows(0, Nrows-1)
            Pi_interface.updating_columns = False
        if Ncols > 8:
            Pi_interface.updating_columns = True
            Pi_interface.values.DeleteCols(8, Ncols-8)
            Pi_interface.updating_columns = False

        for r in range(0, Nrows):
            Pi_interface.values.SetRowLabelValue(r, str(r + 1))
            for c in range(0, Ncols):
                Pi_interface.values.SetCellBackgroundColour(r, c, (255, 255, 255))

        Pi_interface.OnCellChange(self, self.OnCellChange)

    def read_only(self):
        Nrows = Pi_interface.values.GetNumberRows()
        Ncols = Pi_interface.values.GetNumberCols()

        for r in range(0, Nrows):
            for c in range(8, Ncols):
                Pi_interface.values.SetReadOnly(r, c)

    def quit(self, event):
        self.Close()


    def read_in(self):
        try:
            self.case = False
            Pi_interface.reset(self, self.reset)
            self.case = True
            datashape = Pi_interface.Data.shape

            var_name_matrix = Pi_interface.Data[0, :]

            Pi_interface.var_val_matrix = np.array(Pi_interface.Data[1::, :], dtype='f')

            Pi_interface.updating_columns = True
            Pi_interface.values.InsertRows(0, datashape[1])
            Pi_interface.updating_columns = False
            Pi_interface.read_only(self)

            for row in range(0, datashape[1]):
                Pi_interface.values.SetCellValue(row, 0, var_name_matrix[row])
                for col in range(1, 8):
                    Pi_interface.values.SetCellValue(row, col, '0')
            self.Feedbacktext.SetLabel(Pi_interface.Filepath + ' Loaded')
            wx.MessageBox(Pi_interface.Filepath + '\nLoaded', 'File Open', wx.OK)

            Pi_interface.OnCellChange(self, self.OnCellChange)
        except:
            wx.MessageBox('The file at\n' + Pi_interface.Filepath + '\nDoes not contain any data or is not of the correct .CSV datatype', 'File Open', wx.OK)

    def save(self, event):
        def savefile(path, data):
            with open(path, 'wb') as test_file:

                writer = csv.writer(test_file, delimiter=',')

                for row in zip(*data.T):
                    writer.writerow(row)
                wx.MessageBox('Saved', 'Data Save', wx.OK | wx.ICON_INFORMATION)

        Pi_interface.calculate_pi_vals(self)

        if Pi_interface.pi_val_matrix != []:
            heading_group = []

            dialog = wx.FileDialog(self, message='Select file to import', defaultFile=Pi_interface.Filepath, style=wx.SAVE)
            if dialog.ShowModal() == wx.ID_OK:
                if dialog.GetPath().endswith('.csv'):
                    saveFilepath = dialog.GetPath()
                else:
                    saveFilepath = dialog.GetPath() + '.csv'
            dialog.Destroy()

            for i in range(8, Pi_interface.values.GetNumberCols()):
                heading_group.append('Pi Group ' + str(i-7))

            combined_new_set = np.vstack((heading_group, Pi_interface.pi_val_matrix))

            WriteData = np.hstack((Pi_interface.Data, combined_new_set))

            savefile(saveFilepath, WriteData)
            dialog.Destroy()
        else:
            wx.MessageBox('Nothing to save!', 'Error', wx.OK)

    def close(self, event):
        self.Close()


class Plotwindow(Pi_interface,  wx.Frame):
    h_label = ''

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, Plotwindow.h_label)

        panel = wx.Panel(self, wx.ID_ANY)

        name = 'Plot of ' + Pi_interface.y_name + ' versus ' + Pi_interface.x_name

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.canvas = PlotCanvas(panel)
        self.canvas.Draw(PlotGraphics([Pi_interface.dataset], name, Pi_interface.x_name, Pi_interface.y_name))

        sizer.Add(self.canvas, 1, wx.EXPAND)

        panel.SetSizer(sizer)


if __name__ == "__main__":
    app = wx.App()
    frame = Pi_interface(None, -1, 'PI Finder GUI').Show()
    app.MainLoop()