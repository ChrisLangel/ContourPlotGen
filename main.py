#!/usr/bin/env python

import os
import pprint
import random
import sys
import wx
import subprocess
from subprocess import Popen, PIPE

# The recommended way to use wx with mpl is with the WXAgg
# backend. 
#
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
import numpy as np
import pylab
from pylab import arange, meshgrid, contourf, quiver, plot, colorbar


"""This is were we set up a box where you enter the
   q-file and grid name  
"""

class Convq(wx.Panel):

    def __init__(self, parent, ID, label, label2, initval):
        wx.Panel.__init__(self, parent, ID)
        
        self.value = initval
        self.value2 = 1
        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        self.manual_text = wx.TextCtrl(self, -1, 
            size=(80,-1),
            value=initval,
            style=wx.TE_PROCESS_ENTER)

        self.manual_text2 = wx.TextCtrl(self, -1, 
            size=(50,-1),
            value=str(1),
            style=wx.TE_PROCESS_ENTER)
        
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.manual_text)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.manual_text2)
        self.s_label = wx.StaticText(self, -1 , label=label2) 
        
        manual_box = wx.BoxSizer(wx.HORIZONTAL)
        manual_box.Add(self.manual_text, flag=wx.ALIGN_CENTER_VERTICAL)
        manual_box.Add(self.s_label, flag=wx.ALIGN_CENTER_VERTICAL)
        manual_box.Add(self.manual_text2, flag=wx.ALIGN_CENTER_VERTICAL)
        
        sizer.Add(manual_box, 0, wx.ALL, 10)
        
        self.SetSizer(sizer)
        sizer.Fit(self)
   
    def on_text_enter(self, event):
        self.value = self.manual_text.GetValue()
        self.value2 = self.manual_text2.GetValue()
    def is_auto(self):
        return self.radio_auto.GetValue()
        
    def manual_value(self):
        return self.value

    def second_value(self):
        return self.manual_text2.GetValue()

    """ -------------------------------------------------------------------------- """
    """ This is the box that will allow us to change the J, K, L indexes to plot 
    """

class IndexBox(wx.Panel):

    def __init__(self, parent, ID, label, initval1, initval2):
        wx.Panel.__init__(self, parent, ID)
        self.value1 = initval1
        self.value2 = initval2
        
        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        self.max_label = wx.StaticText(self, -1 , label= " Max: ")  
        self.min_label = wx.StaticText(self, -1 , label= "Min: ") 

        self.manual_text1 = wx.SpinCtrl(self, -1, 
            size=(65,-1),
            value=str(initval1),
            style=wx.TE_PROCESS_ENTER,
            name = "Min",
            max=9999,min=1)
        self.manual_text2 = wx.SpinCtrl(self, -1, 
            size=(65,-1),
            value=str(initval2),
            style=wx.TE_PROCESS_ENTER,
            name = 'Max',
            max=9999)           
  

        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter1, self.manual_text1)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter2, self.manual_text2)
        
        manual_box = wx.BoxSizer(wx.HORIZONTAL)
        manual_box.Add(self.min_label, flag=wx.ALIGN_CENTER_VERTICAL)
        manual_box.Add(self.manual_text1, flag=wx.ALIGN_CENTER_VERTICAL)
        manual_box.Add(self.max_label, flag=wx.ALIGN_CENTER_VERTICAL)
        manual_box.Add(self.manual_text2, flag=wx.ALIGN_CENTER_VERTICAL)      
        sizer.Add(manual_box, 0, wx.ALL, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)


    def on_text_enter1(self, event):
        self.value1 = self.manual_text1.GetValue()

    def on_text_enter2(self, event):
        self.value2 = self.manual_text2.GetValue()
    
    def is_auto(self):
        return self.radio_auto.GetValue()
        
    def manual_value1(self):
        return self.value1

    def manual_value2(self):
        return self.value2
  
    def blank_out(self, active):  
        accept = True
        connum = self.manual_text1.GetValue()
        if (active == 1):
            self.manual_text2.SetValue(connum)
            accept = False       

        self.manual_text2.Enable(accept)
    
       
 
    """ --------------------------------------------------------------------------"""
    """ Here is where we choose what plane to loop through """

class WhichPlane(wx.Panel):
    

    def __init__(self, parent, ID, label, initval1, initval2):
        wx.Panel.__init__(self, parent, ID)
        
        self.value1 = initval1
        self.value2 = initval2
        
        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
             
        self.j_sel = wx.RadioButton(self, -1, 
            label="Const-J ", style=wx.RB_GROUP)
        self.k_sel = wx.RadioButton(self, -1, 
            label="Const-K ")
        self.l_sel = wx.RadioButton(self, -1, 
            label="Const-L ")

        self.j_sel.Bind(wx.EVT_RADIOBUTTON, self.SetVal)
        self.k_sel.Bind(wx.EVT_RADIOBUTTON, self.SetVal)
        self.l_sel.Bind(wx.EVT_RADIOBUTTON, self.SetVal)

        manual_box = wx.BoxSizer(wx.VERTICAL)
        manual_box.Add(self.j_sel, flag=wx.ALIGN_CENTER_VERTICAL)
        manual_box.AddSpacer(53)
        manual_box.Add(self.k_sel, flag=wx.ALIGN_CENTER_VERTICAL)
        manual_box.AddSpacer(53)
        manual_box.Add(self.l_sel, flag=wx.ALIGN_CENTER_VERTICAL)
     
        sizer.Add(manual_box, 0, wx.ALL, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)

    def SetVal(self, e):
        hmmm = 1 


    """ -------------------------------------------------------------------------- """
    """ -------------------------------------------------------------------------- """
    """ Create a drop down menu to select the q variable you want to plot """
class QvarBox(wx.Panel):

    def __init__(self, parent, ID, label1, initval):
        wx.Panel.__init__(self, parent, ID)
       
        qvars = [ 'Density' , 'Streamwise (u) Velocity' , 'Spanwise (v) Velocity' , 'Normal (w) Velocity',
                   'k (SST) ' , 'w (SST) ' , 'Intermitency (SST_LM)' , 'RE_thetat (SST_LM)',
                   'A_r (SST_LM_RA)', 'Pressure', 'Velocity Magnitude', 'Velocity Vectors','Ldba*Vel','Lbda*Int','Fth' ]
        self.qvarnum = [ '1' , '2', '3' , '4', '7', '8' ,'9', '10','11', '15','16','17','18','19','20' ] 
        self.cb = wx.ComboBox(self, choices=qvars , style=wx.CB_READONLY) 

        self.num = int(self.qvarnum[1])  
        self.cb.Bind(wx.EVT_COMBOBOX, self.OnSelect)

    def OnSelect(self, e):
        i = e.GetString()
        self.num = int(self.qvarnum[self.cb.GetCurrentSelection()])         
    
    def GetValue(self):
        return self.cb.GetValue()

    def SetString(self,string):
        self.cb.SetStringSelection(string)
    
    """ --------------------------------------------------------------------------"""
    """ -------------------------------------------------------------------------- """
    """ Create a drop down menu to select the resolution of the contour plot """
class ResBox(wx.Panel):

    def __init__(self, parent, ID, label1, initval):
        wx.Panel.__init__(self, parent, ID)
       
        res = [ 'Very Low', 'Low', 'Medium', 'High', 'Very High' ]
        self.resnum = [ '30', '60' , '100' , '140' , '250' ] 
        self.cb = wx.ComboBox(self, choices=res , style=wx.CB_READONLY) 

        self.num = int(self.resnum[1])  
        self.cb.Bind(wx.EVT_COMBOBOX, self.OnSelect)

    def OnSelect(self, e):
        i = e.GetString()
        self.num = int(self.resnum[self.cb.GetCurrentSelection()]) 

    def GetValue(self):
        return self.cb.GetValue()

    def SetString(self,string):
        self.cb.SetStringSelection(string)        
        
class GetBoundaryLayer(wx.Panel):
    def __init__(self, parent, ID, label1, initval):
        wx.Panel.__init__(self, parent, ID)
            



class BoundControlBox(wx.Panel):
    """ A static box with a couple of radio buttons and a text
        box. Allows to switch between an automatic mode and a 
        manual mode with an associated value.
    """
    def __init__(self, parent, ID, label, initval):
        wx.Panel.__init__(self, parent, ID)
        
        self.value = initval
        
        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        self.radio_auto = wx.RadioButton(self, -1, 
            label="Auto", style=wx.RB_GROUP)
        self.radio_manual = wx.RadioButton(self, -1,
            label="Manual")
        self.manual_text = wx.TextCtrl(self, -1, 
            size=(35,-1),
            value=str(initval),
            style=wx.TE_PROCESS_ENTER)
        
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_manual_text, self.manual_text)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.manual_text)
        
        manual_box = wx.BoxSizer(wx.HORIZONTAL)
        manual_box.Add(self.radio_manual, flag=wx.ALIGN_CENTER_VERTICAL)
        manual_box.Add(self.manual_text, flag=wx.ALIGN_CENTER_VERTICAL)
        
        sizer.Add(self.radio_auto, 0, wx.ALL, 10)
        sizer.Add(manual_box, 0, wx.ALL, 10)
        
        self.SetSizer(sizer)
        sizer.Fit(self)
    
    def on_update_manual_text(self, event):
        self.manual_text.Enable(self.radio_manual.GetValue())
 
    def on_text_enter(self, event):
        self.value = self.manual_text.GetValue()
    
        
    def is_auto(self):
        return self.radio_auto.GetValue()
        
    def manual_value(self):
        return self.value


class GraphFrame(wx.Frame):
    """ The main frame of the application
    """
    title = 'Contour Plot Generator'
    
    def __init__(self):
        wx.Frame.__init__(self, None, -1, self.title)
       
        self.update = False
        self.bldraw = False
        self.blcall = False
        self.multgrd = False
        self.cb = ""
        self.create_menu()
        self.create_status_bar()
        self.create_main_panel()
        
#        self.redraw_timer = wx.Timer(self)
#        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)        
#        self.redraw_timer.Start(100)

    def create_menu(self):
        self.menubar = wx.MenuBar()
        
        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
                
        self.menubar.Append(menu_file, "&File")
        self.SetMenuBar(self.menubar)

    def create_main_panel(self):
        self.panel = wx.Panel(self)
        self.init_contour()
        self.boundary_layer()
        self.canvas2 = FigCanvas(self.panel, -1, self.fig1)
        self.canvas3 = FigCanvas(self.panel, -1, self.fig2)
        self.xmin_control = BoundControlBox(self.panel, -1, "X min", 0)
        self.xmax_control = BoundControlBox(self.panel, -1, "X max", 1)
        self.ymin_control = BoundControlBox(self.panel, -1, "Y min", 0)
        self.ymax_control = BoundControlBox(self.panel, -1, "Y max", 1)
        self.qfile_control = Convq(self.panel, -1, "Enter Q file", " Grid #: ", "q.save")
        self.grid_file_control = Convq(self.panel, -1, "Enter Grid file", " Chord: ", "grid.in")
        self.j_index_control = IndexBox(self.panel, -1, "Enter J Indices", 1, 100)
        self.k_index_control = IndexBox(self.panel, -1, "Enter K Indices", 1, 50)
        self.l_index_control = IndexBox(self.panel, -1, "Enter L Indices", 1, 1)
        self.qcont_label = wx.StaticText(self.panel, -1 , label="Select Q variable")
        self.selectq_control = QvarBox(self.panel, -1, -1, 1)
        self.res_label = wx.StaticText(self.panel, -1 , label="Select Contour Resolution")
        self.res_control = ResBox(self.panel, -1, "Select Contour Resolution", 1)
        self.ref_mach = wx.StaticText(self.panel, -1 , label= "Mach:                   ") 
        self.times = wx.StaticText(self.panel, -1 , label= "x") 
        self.Alpha = wx.StaticText(self.panel, -1 , label= "Angle of Attach:           ") 
        self.Rey = wx.StaticText(self.panel, -1 , label= "Reynolds #:                       ") 
        self.Njind = wx.StaticText(self.panel, -1 , label= "J-Dim:      ") 
        self.Nkind = wx.StaticText(self.panel, -1 , label= "K-Dim:      ") 
        self.Nlind = wx.StaticText(self.panel, -1 , label= "L-Dim:      ") 

        self.qfile_control.manual_text2.Enable(0)
        

        self.j_index_control.Bind(wx.EVT_SPINCTRL, self.get_c_plane, 
                                  self.j_index_control.manual_text1)
        self.k_index_control.Bind(wx.EVT_SPINCTRL, self.get_c_plane, 
                                  self.k_index_control.manual_text1)
        self.l_index_control.Bind(wx.EVT_SPINCTRL, self.get_c_plane, 
                                  self.l_index_control.manual_text1)


        self.update_button = wx.Button(self.panel, -1, "Update")
        self.Bind(wx.EVT_BUTTON, self.on_update_button, self.update_button)
#        self.Bind(wx.EVT_UPDATE_UI, self.on_update_update_button, self.update_button)
        
        self.bl_button = wx.Button(self.panel, -1, "Draw BL Profile")
        self.Bind(wx.EVT_BUTTON, self.on_bl_button, self.bl_button)
        self.stream_ind = wx.StaticText(self.panel, -1 , label= "Streamwise Index") 
        self.norm_ind = wx.StaticText(self.panel, -1 , label= "Max K Index") 
        self.x_over_c = wx.StaticText(self.panel, -1 , label= "x/c")
        self.mom_label = wx.StaticText(self.panel, -1 , label= " ")
        self.shape_label = wx.StaticText(self.panel, -1 , label= " ")
        self.Bl_jplane = wx.SpinCtrl(self.panel, -1, size=(65,-1), value=str(1), 
                                     style=wx.TE_PROCESS_ENTER, 
                                     name = "Min", max=9999, min=1)
        self.Bind(wx.EVT_SPINCTRL, self.on_bl_button, self.Bl_jplane)
        self.Bl_kplane = wx.SpinCtrl(self.panel, -1, size=(65,-1), value=str(80), 
                                     style=wx.TE_PROCESS_ENTER, 
                                     name = "Min", max=9999, min=1)
        self.Bind(wx.EVT_SPINCTRL, self.on_bl_button, self.Bl_kplane)

        self.cb_grid = wx.CheckBox(self.panel, -1, 
            "Stretch K",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_grid, self.cb_grid)
        self.cb_grid.SetValue(False)
        self.mom_norm = wx.CheckBox(self.panel, -1, 
            "Normalize by \nMomentum Thickness",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_mom_norm, self.mom_norm)
        self.mom_norm.SetValue(False)    
        self.k_str = wx.SpinCtrl(self.panel, -1, size=(65,-1), value=str(1), 
                                     style=wx.TE_PROCESS_ENTER, 
                                     name = "Min", max=9999, min=1)
        
        self.cb_xlab = wx.CheckBox(self.panel, -1, 
            "Use Every Point",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_xlab, self.cb_xlab)        
        self.cb_xlab.SetValue(False)

        self.flatten = wx.CheckBox(self.panel, -1, 
            "Flatten Geometry",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_flatten, self.flatten)        
        self.cb_xlab.SetValue(False)
       
       
        self.l_sel = wx.RadioButton(self.panel, -1, 
            label="Const-L ", style=wx.RB_GROUP)
        self.j_sel = wx.RadioButton(self.panel, -1, 
            label="Const-J ")
        self.k_sel = wx.RadioButton(self.panel, -1, 
            label="Const-K ")
        self.j_sel.Bind(wx.EVT_RADIOBUTTON, self.get_c_plane)
        self.k_sel.Bind(wx.EVT_RADIOBUTTON, self.get_c_plane)
        self.l_sel.Bind(wx.EVT_RADIOBUTTON, self.get_c_plane)
        if not self.update:
            self.l_index_control.blank_out(1) 

        


        self.selbox = wx.BoxSizer(wx.VERTICAL)
        self.selbox.AddSpacer(20)
        self.selbox.Add(self.j_sel, border=5, flag=wx.ALL )
        self.selbox.AddSpacer(45) 
        self.selbox.Add(self.k_sel, border=5, flag=wx.ALL )
        self.selbox.AddSpacer(45) 
        self.selbox.Add(self.l_sel, border=5, flag=wx.ALL ) 

        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox1.AddSpacer(35)
        self.hbox1.Add(self.ref_mach, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.Add(self.Alpha, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.Add(self.Rey, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.Add(self.Njind, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.Add(self.Nkind, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.Add(self.Nlind, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(20)
        self.hbox1.Add(self.cb_grid, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.Add(self.times, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.Add(self.k_str, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.flatten, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.cb_xlab, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        
        self.hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox5.Add(self.xmin_control, border=5, flag=wx.ALL)
        self.hbox5.Add(self.xmax_control, border=5, flag=wx.ALL)

        self.hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox6.Add(self.ymin_control, border=5, flag=wx.ALL)
        self.hbox6.Add(self.ymax_control, border=5, flag=wx.ALL) 

        self.hbox7 = wx.BoxSizer(wx.VERTICAL)
        self.hbox7.Add(self.hbox5, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.hbox7.Add(self.hbox6, 0, flag=wx.ALIGN_LEFT | wx.TOP)

        self.hbox2 = wx.BoxSizer(wx.VERTICAL)
        self.hbox2.Add(self.grid_file_control, border=5, flag=wx.ALL) 
        self.hbox2.AddSpacer(5)
        self.hbox2.Add(self.qfile_control, border=5, flag=wx.ALL) 
        self.hbox2.AddSpacer(5)
        self.hbox2.Add(self.qcont_label, border=5, flag=wx.ALL) 
        self.hbox2.Add(self.selectq_control, border=5, flag=wx.ALL) 
        self.hbox2.Add(self.res_label, border=5, flag=wx.ALL) 
        self.hbox2.Add(self.res_control, border=5, flag=wx.ALL) 

        self.hbox3 = wx.BoxSizer(wx.VERTICAL)
        self.hbox3.Add(self.j_index_control, border=5, flag=wx.ALL ) 
        self.hbox3.Add(self.k_index_control, border=5, flag=wx.ALL ) 
        self.hbox3.Add(self.l_index_control, border=5, flag=wx.ALL ) 
        self.hbox3.Add(self.update_button, border=5, flag=wx.ALL  | wx.ALIGN_CENTER_HORIZONTAL) 
        
        self.blsel = wx.BoxSizer(wx.VERTICAL)
        self.blsel.Add(self.bl_button, 0, flag=wx.ALIGN_CENTER | wx.TOP)
        self.blsel.AddSpacer(15)
        self.blsel.Add(self.x_over_c, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.blsel.AddSpacer(15)
        self.blsel.Add(self.stream_ind, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.blsel.Add(self.Bl_jplane, 0, flag=wx.ALIGN_CENTER | wx.TOP)
        self.blsel.AddSpacer(10)
        self.blsel.Add(self.norm_ind, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.blsel.Add(self.Bl_kplane, 0, flag=wx.ALIGN_CENTER | wx.TOP)
        self.blsel.AddSpacer(10)
        self.blsel.Add(self.mom_norm, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.blsel.AddSpacer(20)
        self.blsel.Add(self.mom_label, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.blsel.AddSpacer(25)
        self.blsel.Add(self.shape_label, 0, flag=wx.ALIGN_LEFT | wx.TOP)


        self.hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox4.AddSpacer(25)
        self.hbox4.Add(self.hbox2, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.hbox4.AddSpacer(25)
        self.hbox4.Add(self.hbox3, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.hbox4.Add(self.selbox, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.hbox4.AddSpacer(25)
        self.hbox4.Add(self.hbox7, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.hbox4.AddSpacer(25)
        self.hbox4.Add(self.blsel, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.hbox4.AddSpacer(25)        
        self.hbox4.Add(self.canvas3, 1, flag=wx.ALIGN_LEFT | wx.TOP | wx.GROW)  


        self.vbox = wx.BoxSizer(wx.VERTICAL) 
        self.vbox.Add(self.canvas2, 1, flag=wx.LEFT | wx.TOP | wx.GROW)         
        self.vbox.Add(self.hbox1, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.vbox.Add(self.hbox4, 0, flag=wx.ALIGN_LEFT | wx.TOP)
               
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

        if self.selectq_control.GetValue() == '':
            self.selectq_control.SetString(string='Streamwise (u) Velocity')

        if self.res_control.GetValue() == '':
            self.res_control.SetString(string='Low')
        
        
    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()

    def init_plot(self):
        self.dpi = 100
        self.fig = Figure((3.0, 3.0), dpi=self.dpi)

        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_bgcolor('white')
        self.axes.set_title('Very important random data', size=12)
        
        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        # plot the data as a line series, and save the reference 
        # to the plotted line series
        #
        self.plot_data = self.axes.plot(
            self.data, 
            linewidth=1,
            color=(1, 0, 0),
            )[0]


#   Determine which plane to hold constant 
 
    def get_c_plane(self,event):
        jinp = 0
        kinp = 0
        linp = 0
        if (self.j_sel.GetValue()):
            jinp = 1
        if (self.k_sel.GetValue()):
            kinp = 1
        if (self.l_sel.GetValue()):
            linp = 1
        self.j_index_control.blank_out(jinp)
        self.k_index_control.blank_out(kinp)
        self.l_index_control.blank_out(linp) 
    


    def init_contour(self):
        self.data2 = []
        self.x = arange(0,10,.5)
        self.y = arange(0,10,.5) 
        self.X, self.Y = pylab.meshgrid(self.x,self.y)
        self.Z, self.Zt = pylab.meshgrid(self.x,self.y)
        self.dpi2 = 101
        self.fig1 = Figure((3.0, 3.0), dpi=self.dpi2)
        self.axes2 = self.fig1.add_subplot(111)
        self.axes2.set_axis_bgcolor('white')

        if not self.update:
            initplot = self.plot_data2 = self.axes2.contourf(self.X,self.Y,self.Z)
            self.cb = self.fig1.colorbar(initplot)

           

    def on_update_button(self, event):        
        self.j_index_control.value1 = self.j_index_control.manual_text1.GetValue()
        self.j_index_control.value2 = self.j_index_control.manual_text2.GetValue()
        self.k_index_control.value1 = self.k_index_control.manual_text1.GetValue()
        self.k_index_control.value2 = self.k_index_control.manual_text2.GetValue()
        self.l_index_control.value1 = self.l_index_control.manual_text1.GetValue()
        self.l_index_control.value2 = self.l_index_control.manual_text2.GetValue()
        self.qfile_control.value = self.qfile_control.manual_text.GetValue()
        self.grid_file_control.value = self.grid_file_control.manual_text.GetValue()
        self.grid_file_control.value2 = self.grid_file_control.manual_text2.GetValue()
        self.qfile_control.value2 = self.grid_file_control.manual_text2.GetValue()
        self.change = True

        if (self.update):
            if (self.jmin == self.j_index_control.manual_value1() and 
                self.jmax == self.j_index_control.manual_value2() and
                self.kmin == self.k_index_control.manual_value1() and 
                self.kmax == self.k_index_control.manual_value2() and
                self.lmin == self.l_index_control.manual_value1() and 
                self.lmax == self.l_index_control.manual_value2() and
                self.selvar == self.selectq_control.num and 
                self.qf == self.qfile_control.manual_value() and
                self.strk == self.cb_grid.IsChecked() and
                self.flat == self.flatten.IsChecked() and
                self.kstretch_fac == self.k_str.GetValue() and
                self.res ==self.res_control.GetValue() and
                self.gnum == self.qfile_control.manual_text2.GetValue() and
                self.gd == self.grid_file_control.manual_value()):  
                self.change = False  

        self.update = True
        self.grid  = self.grid_file_control.manual_value() 
        self.qfile = self.qfile_control.manual_value()
        self.jmin  = self.j_index_control.manual_value1()
        self.jmax  = self.j_index_control.manual_value2()
        self.kmin  = self.k_index_control.manual_value1()
        self.kmax  = self.k_index_control.manual_value2()
        self.lmin  = self.l_index_control.manual_value1()
        self.lmax  = self.l_index_control.manual_value2()
        self.qf = self.qfile_control.manual_value()
        self.gd  = self.grid_file_control.manual_value()
        self.strk =  self.cb_grid.IsChecked()
        self.flat =  self.flatten.IsChecked()
        self.selvar = self.selectq_control.num 
        self.kstretch_fac = self.k_str.GetValue()
        self.res = self.res_control.GetValue()
        self.gnum = self.qfile_control.manual_text2.GetValue()
        if (self.bldraw == False and self.blcall == True): 
            self.update = False
        if (self.update == False or self.change == True):
            self.draw_update() 
            

    def draw_update(self):
        qistr    = ''.join([self.qfile, '\n', self.qfile_control.manual_text2.GetValue()])
        p6 = subprocess.Popen(['getqinfo'], stdin=PIPE, stdout=PIPE)
        o6,e6 = p6.communicate(input=qistr)  

        if (self.change==True or self.update==False): 
            self.file3 = pylab.loadtxt('QOUT.txt')
            os.remove('QOUT.txt')
            self.refmach = self.file3[0] 
            self.alpha = self.file3[1]
            self.rey = self.file3[2] 
            self.time = self.file3[3]
            self.gaminf = self.file3[4]
            self.beta = self.file3[5]
            self.tinf = self.file3[6]
            self.njind = int(self.file3[7])
            self.nkind = int(self.file3[8])
            self.nlind = int(self.file3[9])
            self.ngrid = int(self.file3[10])
        if (self.ngrid > 1):
            self.multgrd = True
            self.qfile_control.manual_text2.Enable(1)
        else: 
            self.multgrd = False
            self.qfile_control.manual_text2.Enable(0)

        self.ref_mach.SetLabel( ''.join([' Mach: ', str(self.refmach)]) )
        self.Alpha.SetLabel( ''.join(['  Angle of Attach: ', str(self.alpha)]) )
        self.Rey.SetLabel( ''.join(['  Reynolds #: ', str(self.rey)]) )
        self.Njind.SetLabel( ''.join(['    J-dim:  ', str(self.njind)]) )
        self.Nkind.SetLabel( ''.join(['   K-dim:  ', str(self.nkind)]) )
        self.Nlind.SetLabel( ''.join(['   L-dim:  ', str(self.nlind)]) )       
        
        gnum = self.qfile_control.manual_text2.GetValue()
        if (self.multgrd):             
            new_str1 = ''.join([self.qfile, '\n','qval.txt', '\n', str(gnum), '\n', str(self.jmin) ,' ', 
                                str(self.jmax) ,' ', str(1), '\n' ,  str(self.kmin),' ',
                                str(self.kmax),' ',str(1), '\n' ,str(self.lmin) ,
                                ' ',str(self.lmax) ,' ', str(1), '\n',
                                str(self.selvar), '\n','n'])  
        else:
            new_str1 = ''.join([self.qfile, '\n','qval.txt', '\n', str(self.jmin) ,' ', 
                                str(self.jmax) ,' ', str(1), '\n' ,  str(self.kmin),' ',
                                str(self.kmax),' ',str(1), '\n' ,str(self.lmin) ,
                                ' ',str(self.lmax) ,' ', str(1), '\n',
                                str(self.selvar), '\n','n'])  

        
        new_str2 = ''.join([self.grid, '\n', str(gnum), '\n','cords.txt', '\n', str(self.jmin) ,' ', 
                            str(self.jmax) ,' ', str(1), '\n' ,  str(self.kmin),' ',
                            str(self.kmax),' ', str(1), '\n' ,str(self.lmin) ,
                            ' ',str(self.lmax) ,' ', str(1)]) 

        self.bldraw = False    
        if (self.change==True or self.update==False): 
            p2 = subprocess.Popen(['getgridcords'], stdin=PIPE, stdout=PIPE)
            o2,e2 = p2.communicate(input=new_str2) 
            p1 = subprocess.Popen(['listplotvar'], stdin=PIPE, stdout=PIPE)
            o1,e1 = p1.communicate(input=new_str1)
            p3 = subprocess.Popen(['tail', '-n', '+7'], stdin=PIPE, stdout=PIPE)
            o3,e3 = p3.communicate(input=o1) 
            p4 = subprocess.Popen(['head', '-n', '-1'], stdin=PIPE, stdout=PIPE)
            o4,e4 = p4.communicate(input=o3) 
            self.file = pylab.loadtxt('cords.txt')
            os.remove('cords.txt')

        jt = (int(self.jmax) - int(self.jmin)) + 1
        kt = (int(self.kmax) - int(self.kmin)) + 1
        lt = (int(self.lmax) - int(self.lmin)) + 1

        in1,in2,in3,in4 = 0,1,3,4
        if (self.k_sel.GetValue()):
            kt = lt 
            self.kmin = self.lmin 
            self.kmax = self.lmax
            in1,in2,in3,in4 = 0,2,3,5
        if (self.j_sel.GetValue()):
            jt = lt 
            self.jmin = self.lmin 
            self.jmax = self.lmax
            in1 = 2
            in2 = 1
            in3 = 5
            in4 = 4
        
        x = [.5 for i in range(jt)]
        y = [.5 for i in range(kt)]
        X, Y = pylab.meshgrid(x,y)
        Z, Zt = pylab.meshgrid(x,y)

        tot = jt*kt
        
        for k in range(0,tot):
            ind1 = int(self.file[k][in1] - int(self.jmin))
            ind2 = int(self.file[k][in2] - int(self.kmin))
            X[ind2][ind1] = float(self.file[k][in3])
            Y[ind2][ind1] = float(self.file[k][in4])
        
#        print X[1]
      
        if (self.change==True or self.update==False):
            self.file2 = pylab.loadtxt('qval.txt')
            os.remove('qval.txt')

        if (self.selvar == 17): 
            for k in range(0,tot):
                ind1 = int(self.file2[k][in1] - int(self.jmin))
                ind2 = int(self.file2[k][in2] - int(self.kmin))
                Z[ind2][ind1] = float(self.file2[k][3])
                Zt[ind2][ind1] = float(self.file2[k][4])

        else:
            for k in range(0,tot):
                ind1 = int(self.file2[k][in1] - int(self.jmin))
                ind2 = int(self.file2[k][in2] - int(self.kmin))
                Z[ind2][ind1] = float(self.file2[k][3])



        chord = int(self.grid_file_control.second_value())
        X = X/chord
        Y = Y/chord
#        Z = Z/chord
        if (self.selvar > 1 and self.selvar < 4 or self.selvar == 16):
            Z = Z/(float(self.refmach))
        self.Xref  = X
        self.Yref  = Y 
#        self.Zref  = Z  
        lz = len(Z)
        minz = np.amin(Z)
        maxz = np.amax(Z)
        minx = np.amin(X)
        maxx = np.amax(X)
        miny = np.amin(Y)
        maxy = np.amax(Y)
        xs = x[::4]
        ys = y[::4]
        Xs,Ys = pylab.meshgrid(xs,ys)
        Zs,Zst = pylab.meshgrid(xs,ys)
        ls = len(X)
        ct = 0
        for i in arange(0,(ls),4):
            Xs[ct] = X[i][::4]
            Ys[ct] = Y[i][::4]
            Zs[ct] = Z[i][::4]
            Zst[ct] = Zt[i][::4]
            ct = ct + 1

        res = self.res_control.num 
        sp = (maxz - minz)/res
        if (minz >= 0):
            levels = arange((minz-minz*.1),maxz*1.05, sp )
        else:
            levels = arange((minz+minz*.1),maxz*1.05, sp ) 
        self.axes2.cla()
        if (self.k_sel.GetValue() or self.j_sel.GetValue()):
            self.cb_xlab.SetValue(True)
        if not self.cb_xlab.IsChecked(): 
            if not self.cb_grid.IsChecked():
                if (self.selvar == 17):
                    self.axes2.plot(X[1],Y[1])
                    cplot = self.axes2.contourf(Xs,Ys,Zs,levels)
                    self.axes2.quiver(X[::3,::2],Y[::3,::2],Z[::3,::2],Zt[::3,::2],scale=1.25)
                else:
                    cplot = self.axes2.contourf(Xs,Ys,Zs,levels)
                    self.fig1.delaxes(self.fig1.axes[1])
                    self.fig1.subplots_adjust(right=0.90)
                    if not (self.selvar == 8 or self.selvar == 7 or self.selvar == 10 ): 
                        legendinterval= (maxz - minz)/6
                        lts = round(legendinterval,2)
                        lstart = lts*(np.floor(minz/lts))
                        self.cb = self.fig1.colorbar(cplot,ticks=[lstart,lstart+lts,lstart+2*lts,
                                              lstart+3*lts,lstart+4*lts,lstart+5*lts,lstart+6*lts])
                    if (self.selvar == 8 or self.selvar == 7 or self.selvar == 10 ): 
                        legendinterval= (maxz - minz)/6
                        lts = np.floor(legendinterval)
                        lstart = lts*(np.floor(minz/lts))
                        self.cb = self.fig1.colorbar(cplot)
            self.axes2.set_xlabel("x/c")
            self.axes2.set_ylabel("z/c")
            if (self.k_sel.GetValue()):
                self.axes2.set_ylabel("y/c")
            if (self.j_sel.GetValue()):
                self.axes2.set_xlabel("y/c")
            minz = np.amin(Zs)
            maxz = np.amax(Zs)
            minx = np.amin(Xs)
            maxx = np.amax(Xs)
            miny = np.amin(Ys)
            maxy = np.amax(Ys)
            self.check_auto_axis(minx,maxx,miny,maxy)
        if self.cb_xlab.IsChecked():
            if not self.cb_grid.IsChecked():
                cplot = self.axes2.contourf(X,Y,Z,levels)
                self.fig1.delaxes(self.fig1.axes[1])
                self.fig1.subplots_adjust(right=0.90)
                if not (self.selvar == 8 or self.selvar == 7 or self.selvar == 10 ): 
                    legendinterval= (maxz - minz)/6
                    lts = round(legendinterval,2)
                    lstart = lts*(np.floor(minz/lts))
                    self.cb = self.fig1.colorbar(cplot,ticks=[lstart,lstart+lts,lstart+2*lts,
                                         lstart+3*lts,lstart+4*lts,lstart+5*lts,lstart+6*lts])
                if (self.selvar == 8 or self.selvar == 7 or self.selvar == 10 ): 
                    legendinterval= (maxz - minz)/6
                    lts = np.floor(legendinterval)
                    lstart = lts*(np.floor(minz/lts))
                    self.cb = self.fig1.colorbar(cplot)
             
            self.axes2.set_xlabel("x/c")
            self.axes2.set_ylabel("z/c")
            if (self.k_sel.GetValue()):
                self.axes2.set_ylabel("y/c")
            if (self.j_sel.GetValue()):
                self.axes2.set_xlabel("y/c")
                
            self.check_auto_axis(minx,maxx,miny,maxy)
        if (self.cb_grid.IsChecked() and not self.flatten.IsChecked()):
            Xstr = X
            Ystr = Y
            lj = len(X[0])
            for k in range(0,ls):
                for j in range(0,lj):
                    stretch = int(self.k_str.GetValue())
                    xa = X[0][j]
                    ya = Y[0][j]
                    xb = X[k][j]
                    yb = Y[k][j] 
                    vax = xb - xa
                    vay = yb - ya
                    Xstr[k][j] = xb + stretch*vax
                    Ystr[k][j] = yb + stretch*vay
            if (self.selvar == 17):
                self.axes2.plot(Xstr[1],Ystr[1])
                self.axes2.quiver(Xstr[::3,::2],Ystr[::3,::2],
                                  Z[::3,::2],Zt[::3,::2],scale=1.25)
            else:
                cplot = self.axes2.contourf(Xstr,Ystr,Z,levels)
                self.fig1.delaxes(self.fig1.axes[1])
                self.fig1.subplots_adjust(right=0.90)
                if not (self.selvar == 8 or self.selvar == 7 or self.selvar == 10 ): 
                    legendinterval= (maxz - minz)/6
                    lts = round(legendinterval,2)
                    lstart = lts*(np.floor(minz/lts))
                    self.cb = self.fig1.colorbar(cplot,ticks=[lstart,lstart+lts,lstart+2*lts,
                                         lstart+3*lts,lstart+4*lts,lstart+5*lts,lstart+6*lts])
                if (self.selvar == 8 or self.selvar == 7 or self.selvar == 10 ): 
                    legendinterval= (maxz - minz)/6
                    lts = np.floor(legendinterval)
                    lstart = lts*(np.floor(minz/lts))
                    self.cb = self.fig1.colorbar(cplot)

            self.axes2.set_ylabel(" ")
       
        if (self.flatten.IsChecked()):
            Xstr = X
            Ystr = Y
            lj = len(X[0])
            goneg = False
            for j in range(0,lj):                
                Xstr[0][j] = X[0][j]
                Ystr[0][j] = 0 
                dist1 = ( (X[1][j] - X[0][j])**2 + (Y[1][j] - Y[0][j])**2)**.5 
                for k in range(1,ls):
                    xa = X[0][j]
                    ya = Y[0][j]
                    xb = X[k][j]
                    yb = Y[k][j]
                    xf = X[ls-1][j]
                    yf = Y[ls-1][j]
                    length = ( (xf - xa)**2 + (yf - ya)**2 )**.5 
                    vax = xb - xa
                    vay = yb - ya
                    dist = (vax**2 + vay**2)**.5
                    Xstr[k][j] = X[0][j]
                    Ystr[k][j] = (dist - dist1)
            self.axes2.cla()
            cplot = self.axes2.contourf(Xstr,Ystr,Z,levels)
#            self.cb.set_clim(vmin=minz, vmax = maxz)  
#            self.cb.draw_all()
            minx = np.amin(Xstr)
            maxx = np.amax(Xstr)
            miny = np.amin(Ystr)
            maxy = np.amax(Ystr)
            self.fig1.delaxes(self.fig1.axes[1])
            self.fig1.subplots_adjust(right=0.90)
            if not (self.selvar == 8 or self.selvar == 7 or self.selvar == 10 ): 
                legendinterval= (maxz - minz)/6
                lts = round(legendinterval,2)
                lstart = lts*(np.floor(minz/lts))
                self.cb = self.fig1.colorbar(cplot,ticks=[lstart,lstart+lts,lstart+2*lts,
                                         lstart+3*lts,lstart+4*lts,lstart+5*lts,lstart+6*lts])
            if (self.selvar == 8 or self.selvar == 7 or self.selvar == 10 ): 
                legendinterval= (maxz - minz)/6
                lts = np.floor(legendinterval)
                lstart = lts*(np.floor(minz/lts))
                self.cb = self.fig1.colorbar(cplot)
 
            interval = (maxx - minx)/20
            tickspace = 0
            if (interval < .05 ):
                tickspace = .05
                xstart = tickspace*(np.floor(minx/tickspace))
            if (interval > .05 and interval < .11):
                tickspace = .10
                xstart = tickspace*(np.floor(minx/tickspace))
            if (interval >= .11 and interval < .16):
                tickspace = .15
                xstart = tickspace*(np.floor(minx/tickspace))
            if (interval >= .16 and interval < .26):
                tickspace = .25
                xstart = tickspace*(np.floor(minx/tickspace))
            if (tickspace > 0):
                self.axes2.set_xticks(arange(xstart,(maxx+tickspace),tickspace))
            self.axes2.set_xlabel("x/c")
            self.axes2.set_ylabel("z/c")
            if (self.k_sel.GetValue()):
                self.axes2.set_ylabel("y/c")
            if (self.j_sel.GetValue()):
                self.axes2.set_xlabel("y/c")
            
            self.check_auto_axis(minx,maxx,miny,maxy)
    
        self.data2 = X[0]                                            
        ymax = round(max(self.data2), 0) + 1
        self.canvas2.draw()
        
    def check_auto_axis(self,minx,maxx,miny,maxy):
        self.xmax_control.value = self.xmax_control.manual_text.GetValue()
        self.xmin_control.value = self.xmin_control.manual_text.GetValue()
        self.ymax_control.value = self.ymax_control.manual_text.GetValue()
        self.ymin_control.value = self.ymin_control.manual_text.GetValue()

        if self.xmax_control.is_auto():
            xmax = maxx
        else:
            xmax = float(self.xmax_control.manual_value())
            
        if self.xmin_control.is_auto():            
            xmin = minx
        else:
            xmin = float(self.xmin_control.manual_value())

        if self.ymin_control.is_auto():
            ymin = miny
        else:
            ymin = float(self.ymin_control.manual_value())
        
        if self.ymax_control.is_auto():
            ymax = maxy
        else:
            ymax = float(self.ymax_control.manual_value())

        self.axes2.set_xbound(lower=xmin, upper=xmax)
        self.axes2.set_ybound(lower=ymin, upper=ymax)

    def on_update_update_button(self, event):
        label = "Update" if self.update else "Draw"
        self.update_button.SetLabel(label)
        

    def boundary_layer(self): 
        self.dpi3 = 102
        self.fig2 = Figure((3.0, 3.0), dpi=self.dpi3)
        self.axes3 = self.fig2.add_subplot(111)
        self.axes3.set_axis_bgcolor('white')
        self.x = arange(0,10,.5)
        self.y = arange(0,10,.5) 
        self.X, self.Y = pylab.meshgrid(self.x,self.y)
        self.Z, self.Zt = pylab.meshgrid(self.x,self.y)

        if not self.update:
            self.axes3.contourf(self.X,self.Y,self.Z)
   
    def update_bl_mom(self,X,Y,U,maxk,jcur):
        Uinf = U[maxk]
        kct  = 0
        ucur = 0
        kmax = self.Bl_kplane.GetValue()
        while ( kct < kmax):  
            ucur = U[kct]
            kct  = kct + 1    
        delta = ( (X[kct] - X[0])**2 + (Y[kct] - Y[0])**2)**.5     
        indmax = 0 
        umax   = 0   
        hitmax = True
        for i in range(0,maxk):
            if (U[i] > umax or i < 5):
                if hitmax:
                    umax = U[i]
                    indmax = i
            else:
                hitmax = False
#        print str(indmax)
        if indmax > maxk:
            indmax = maxk - 1 
        if indmax%2 == 0:
            x = arange(0,(indmax/2),.5)
            y = arange(0,(indmax/2),.5)
            xpt = arange(0,(indmax/2),.5)
            ypt = arange(0,(indmax/2),.5)
        else:
            x = arange(0,(indmax/2)+.5,.5)
            y = arange(0,(indmax/2)+.5,.5)
            xpt = arange(0,(indmax/2)+.5,.5)
            ypt = arange(0,(indmax/2)+.5,.5)
        dispth = 0 
        momth  = 0
        for i in range(0,indmax-1):
            uinf = U[indmax]
            y[i] = ( (X[i] - X[0])**2 + (Y[i] - Y[0])**2)**.5                          
            x[i] = U[i] / uinf
            xpt[i] = U[i] / uinf
            if i > 1:  
                dy =  y[i] - y[i-1] 
                dispth = dispth + (1 - xpt[i-1])*dy
                momth  = momth  +  xpt[i-1]*(1 - xpt[i-1])*dy
        H     = dispth/momth
#        print str(dispth)
#        print str(momth)
#        print str(H)       
        shape = round(H,4)
        self.shape_label.SetLabel( ''.join(['H (Shape Factor) =   ', str(shape)]) )
        momthick = round(momth,8)
        self.mom_label.SetLabel( ''.join(['Momentum \nThickness =   ', str(momthick)]) )
        
        if (self.mom_norm.IsChecked()):
            self.axes3.cla()
            self.axes3.plot(x,(y/momth))
            self.axes3.set_xlabel("$ u/U_e $")
            self.axes3.set_ylabel("$ z/ \Theta$")
            self.axes3.set_xbound(lower=-.1, upper=1.2)
            self.axes3.set_ybound(lower=0, upper=15)
            self.canvas3.draw()
            self.fig2.subplots_adjust(wspace=0.1)
            self.fig2.subplots_adjust(left=0.2)
            self.fig2.subplots_adjust(right=0.95)
            self.fig2.subplots_adjust(bottom=0.15)

   
    def update_bl(self,X,Y,U,maxk,jcur):
        Uinf = U[maxk]
        kct  = 0
        ucur = 0
        kmax = self.Bl_kplane.GetValue()
        while ( kct < kmax):  
            ucur = U[kct]
            kct  = kct + 1    
        delta = ( (X[kct] - X[0])**2 + (Y[kct] - Y[0])**2)**.5 
        x = [.5 for i in range(kct)]
        y = [.5 for i in range(kct)]
        xpt = [.5 for i in range(kct)]
        xpt = [.5 for i in range(kct)]
        for i in range(0,kct):
            y[i] = ( (X[i] - X[0])**2 + (Y[i] - Y[0])**2)**.5                          
            x[i] = U[i] / Uinf
        self.axes3.cla()
        self.axes3.plot(x,y)
        self.axes3.set_xlabel("$ u/U_e $")
        self.axes3.set_ylabel("$ z/c $")
        self.axes3.set_xbound(lower=-.1, upper=1.2)
        self.canvas3.draw()
        self.fig2.subplots_adjust(wspace=0.1)
        self.fig2.subplots_adjust(left=0.28)
        self.fig2.subplots_adjust(right=0.95)
        self.fig2.subplots_adjust(bottom=0.15)


    def on_bl_button(self,event):
        self.selectq_control.SetString(string='Streamwise (u) Velocity')
        self.selectq_control.num = 2
        self.blcall = True 
        self.bldraw = True
        self.on_update_button(event)
        self.blcall = False
        self.jcur = self.Bl_jplane.GetValue()
        gnum = self.qfile_control.manual_text2.GetValue()
        if (self.multgrd):      
            new_str1 = ''.join([self.qfile, '\n','qvalbl.txt', '\n', str(gnum), '\n', str(self.jcur) ,' ', 
                                str(self.jcur) ,' ', str(1), '\n' ,  str(1),' ',
                                str(self.nkind),' ',str(1), '\n' ,str(1) ,
                                ' ',str(1) ,' ', str(1), '\n',
                                str(2), '\n','n'])  
        else:
            new_str1 = ''.join([self.qfile, '\n','qvalbl.txt', '\n', str(self.jcur) ,' ', 
                                str(self.jcur) ,' ', str(1), '\n' ,  str(1),' ',
                                str(self.nkind),' ',str(1), '\n' ,str(1) ,
                                ' ',str(1) ,' ', str(1), '\n',
                                str(2), '\n','n'])  
            
        new_str2 = ''.join([self.grid, '\n',  str(gnum), '\n', 'cordsbl.txt', '\n', str(self.jcur) ,' ', 
                            str(self.jcur) ,' ', str(1), '\n' ,  str(1),' ',
                            str(self.nkind),' ', str(1), '\n' ,str(1) ,
                            ' ',str(1) ,' ', str(1)]) 
        p2 = subprocess.Popen(['getgridcords'], stdin=PIPE, stdout=PIPE)
        o2,e2 = p2.communicate(input=new_str2) 
        p1 = subprocess.Popen(['listplotvar'], stdin=PIPE, stdout=PIPE)
        o1,e1 = p1.communicate(input=new_str1)
        p3 = subprocess.Popen(['tail', '-n', '+7'], stdin=PIPE, stdout=PIPE)
        o3,e3 = p3.communicate(input=o1) 
        p4 = subprocess.Popen(['head', '-n', '-1'], stdin=PIPE, stdout=PIPE)
        o4,e4 = p4.communicate(input=o3) 

        self.file1 = pylab.loadtxt('qvalbl.txt')
        self.file2 = pylab.loadtxt('cordsbl.txt')
        
        os.remove('qvalbl.txt')
        os.remove('cordsbl.txt')
        
        tot = len(self.file1)
        u = [.5 for i in range(tot)]
        x = [.5 for i in range(tot)]
        y = [.5 for i in range(tot)]
        for k in range(0,tot):
            u[k] = float(self.file1[k][3])
            x[k] = float(self.file2[k][3])
            y[k] = float(self.file2[k][4])
        xoverc = round(x[0],5)
        self.x_over_c.SetLabel( ''.join(['x/c =   ', str(xoverc)]) )
        if (self.mom_norm.IsChecked()):
            self.update_bl_mom(x,y,u,(self.nkind-1),(self.jcur))
        else:
            self.update_bl_mom(x,y,u,(self.nkind-1),(self.jcur))
            self.update_bl(x,y,u,(self.nkind-1),(self.jcur))
                  
    

    def on_cb_grid(self, event):
        self.on_update_button(event)  

    def on_flatten(self, event):
        self.on_update_button(event)  
        
    def on_cb_xlab(self, event):
        self.on_update_button(event)
        
    def on_mom_norm(self, event):
        self.on_bl_button(event)


    
    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"
        
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas2.print_figure(path, dpi=self.dpi2)
            self.flash_status_message("Saved to %s" % path)
    
    def on_redraw_timer(self, event):
        i = 1
    
    def on_exit(self, event):
        self.Destroy()
    
    def flash_status_message(self, msg, flash_len_ms=1500):
        self.statusbar.SetStatusText(msg)
        self.timeroff = wx.Timer(self)
        self.Bind(
            wx.EVT_TIMER, 
            self.on_flash_status_off, 
            self.timeroff)
        self.timeroff.Start(flash_len_ms, oneShot=True)
    
    def on_flash_status_off(self, event):
        self.statusbar.SetStatusText('')


if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.frame = GraphFrame()
    app.frame.Show()
    app.MainLoop()



