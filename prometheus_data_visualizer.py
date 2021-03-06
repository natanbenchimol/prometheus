import pandas as pd
import numpy as np
from tkinter import filedialog
from tkinter import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots
window = Tk()

window.title("Prometheus Data Visualizer")       # Title of the GUI window
window.iconbitmap("Assets/LPL.ico")              # Puts the LPL logo on the GUI window

LARGE_FONT= ("Verdana", 12)

# This creates the GUI
class mclass:
    def __init__(self, window):
        self.window = window            # This creates an empty window

        self.ax1 = pd.DataFrame()       # Creates empty dataframes
        self.ax2 = pd.DataFrame()       # These are needed for now so that an error doesn't occur when
        self.ax3 = pd.DataFrame()       # "Plot all sensor" button is pressed before loading all sensor data

        # All the "Button" creates a button on the GUI
        # "command" is what the button does, can be a built in command or a command we will define
        # The plot button initiate the plotting sequence for the checked sensors
        self.Button = Button(window, text='Plot', command=self.plots).grid(row=3, column=3, sticky=W, padx=5)

        # This button initiate the plotting for all sensors
        self.Button = Button(window, text='Plot all sensors', command=self.allsensor).grid(row=7, column=3,
                                                                                           sticky=W, padx=5, pady=5)
        # Must use this quit button after plotting or else you need to stop the process manually which leads to an error
        self.Button = Button(window, text='Quit', command=window.quit).grid(row=8, column=3, sticky=W,
                                                                                  padx=5, pady=3)

        self.Label = Label(window, text='Select the sensors you want to plot, '
                                        'then hit the Plot button').grid(row=2, column=0, columnspan=3,
                                                                         sticky=W, padx=5, pady=5)
        self.Label = Label(window, text='Need to load all three types of sensor before plotting').grid(row=0,
                                                                column=0, columnspan=3, sticky=W, padx=5, pady=5)

        # Buttons to allow user to select sensor data to load
        self.Button = Button(window, text='Import TC', command=self.importtc).grid(row=1, column=0, sticky=W,
                                                                                   padx=5, pady=3)
        self.Button = Button(window, text='Import PT', command=self.importpt).grid(row=1, column=1, sticky=W,
                                                                                padx=5, pady=3)
        self.Button = Button(window, text='Import FM', command=self.importfm).grid(row=1, column=2, sticky=W,
                                                                                   padx=5, pady=3)

    # This opens file explorer to allow user to select sensors data
    # The check boxes for the sensors will be created after importing data
    # The if statement is needed so an error doesn't occur if cancel is pressed after file explorer is opened
    def importtc(self):
        tcfile = filedialog.askopenfile(filetypes=[("CSV files","*.csv")], title="Select TC Data")
        if tcfile is not None:
            self.TC = pd.read_csv(tcfile)
            # the .drop drops the column with the name "   " since we don't need it to plot
            self.ax1 = self.TC.drop(['Batch Num', 'Avg. Time'], axis=1)
            # All the "Checkbutton" creates a check box on the GUI
            # "variable" returns 1 or 0 to that variable depending on if the checkbox is checked or not
            self.Check = Checkbutton(window, text=self.ax1.columns[1], variable=TCsensor1).grid(row=3, column=0,
                                                                                           sticky=W, padx=5)
            self.Check = Checkbutton(window, text=self.ax1.columns[2], variable=TCsensor2).grid(row=4, column=0,
                                                                                           sticky=W, padx=5)
            self.Check = Checkbutton(window, text=self.ax1.columns[3], variable=TCsensor3).grid(row=5, column=0,
                                                                                           sticky=W, padx=5)
            self.Check = Checkbutton(window, text=self.ax1.columns[4], variable=TCsensor4).grid(row=6, column=0,
                                                                                           sticky=W, padx=5)
            self.Check = Checkbutton(window, text=self.ax1.columns[5], variable=TCsensor5).grid(row=7, column=0,
                                                                                           sticky=W, padx=5)
            self.Check = Checkbutton(window, text=self.ax1.columns[6], variable=TCsensor6).grid(row=8, column=0,
                                                                                           sticky=W, padx=5, pady=5)
            self.Check = Checkbutton(window, text=self.ax1.columns[7], variable=TCsensor7).grid(row=9, column=0,
                                                                                           sticky=W, padx=5, pady=8)
            self.Button = Button(window, text='Plot all TC', command=self.allTC).grid(row=4, column=3,
                                                                                      sticky=W, padx=5, pady=5)

    def importpt(self):
        ptfile = filedialog.askopenfile(filetypes=[("CSV files","*.csv")], title="Select PT Data")
        if ptfile is not None:
            self.PT = pd.read_csv(ptfile)
            self.ax2 = self.PT.drop(['Batch Num', 'Avg. Time'], axis=1)
            self.Check = Checkbutton(window, text=self.ax2.columns[1], variable=PTsensor1).grid(row=3, column=1,
                                                                                           sticky=W, padx=5)
            self.Check = Checkbutton(window, text=self.ax2.columns[2], variable=PTsensor2).grid(row=4, column=1,
                                                                                           sticky=W, padx=5)
            self.Check = Checkbutton(window, text=self.ax2.columns[3], variable=PTsensor3).grid(row=5, column=1,
                                                                                           sticky=W, padx=5)
            self.Check = Checkbutton(window, text=self.ax2.columns[4], variable=PTsensor4).grid(row=6, column=1,
                                                                                           sticky=W, padx=5)
            self.Check = Checkbutton(window, text=self.ax2.columns[5], variable=PTsensor5).grid(row=7, column=1,
                                                                                           sticky=W, padx=5)
            self.Check = Checkbutton(window, text=self.ax2.columns[6], variable=PTsensor6).grid(row=8, column=1,
                                                                                           sticky=W, padx=5, pady=5)
            self.Check = Checkbutton(window, text=self.ax2.columns[7], variable=PTsensor7).grid(row=9, column=1,
                                                                                           sticky=W, padx=5, pady=8)
            self.Button = Button(window, text='Plot all PT', command=self.allPT).grid(row=5, column=3,
                                                                                      sticky=W, padx=5, pady=5)

    def importfm(self):
        fmfile = filedialog.askopenfile(filetypes=[("CSV files","*.csv")], title="Select FM Data")
        if fmfile is not None:
            self.FM = pd.read_csv(fmfile)
            self.ax3 = self.FM.drop(['Batch Num', 'Avg. Time'], axis=1)
            self.Check = Checkbutton(window, text=self.ax3.columns[1], variable=FMsensor1).grid(row=3, column=2,
                                                                                           sticky=W, padx=5)
            self.Check = Checkbutton(window, text=self.ax3.columns[2], variable=FMsensor2).grid(row=4, column=2,
                                                                                           sticky=W, padx=5)
            self.Button = Button(window, text='Plot all FM', command=self.allFM).grid(row=6, column=3,
                                                                                      sticky=W, padx=5, pady=5)

    # This initiate the plotting of the selected sensors
    def plots(self):
        # Creates empty data sets that sensors will be added to as they are checked
        tcsensor2plot = pd.DataFrame()
        ptsensor2plot = pd.DataFrame()
        fmsensor2plot = pd.DataFrame()

        # Append time to first column to use for the x-axis
        data0 = self.ax1.iloc[:, 0]
        data1 = self.ax2.iloc[:, 0]
        data2 = self.ax3.iloc[:, 0]
        tcsensor2plot = tcsensor2plot.append(data0)
        ptsensor2plot = ptsensor2plot.append(data1)
        fmsensor2plot = fmsensor2plot.append(data2)

        # Creates a vector of 1 (checked) and 0 (unchecked) for the TC and PT sensors
        # Will be used to check which sensors are selected
        tcsensors = [TCsensor1.get(), TCsensor2.get(), TCsensor3.get(), TCsensor4.get(), TCsensor5.get(),
                     TCsensor6.get(), TCsensor7.get()]
        ptsensors = [PTsensor1.get(), PTsensor2.get(), PTsensor3.get(), PTsensor4.get(), PTsensor5.get(),
                     PTsensor6.get(), PTsensor7.get()]
        fmsensors = [FMsensor1.get(), FMsensor2.get()]

        # Goes through each sensor that returns a 1 and append the data for that sensor to a new data set with just
        # the sensors we want to plot
        for i in range(0,len(self.ax1.columns)-1):
            if tcsensors[i] == 1:
                tcsensor2plot = tcsensor2plot.append(self.ax1.iloc[:, i+1])
        for i in range(0, len(self.ax2.columns) - 1):
            if ptsensors[i] == 1:
                ptsensor2plot = ptsensor2plot.append(self.ax2.iloc[:, i+1])
        for i in range(0, len(self.ax3.columns) - 1):
            if fmsensors[i] == 1:
                fmsensor2plot = fmsensor2plot.append(self.ax3.iloc[:, i+1])

        # Had to transpose because the append function adds each sensor data as a row vector
        tcsensor2plot = np.transpose(tcsensor2plot)
        ptsensor2plot = np.transpose(ptsensor2plot)
        fmsensor2plot = np.transpose(fmsensor2plot)

        # Counts the number of check boxes that are checked (0 if none are checked)
        tcchecked = np.count_nonzero(tcsensors)
        ptchecked = np.count_nonzero(ptsensors)
        fmchecked = np.count_nonzero(fmsensors)

        def singleplot(self, df, plottitle, ytype):
            for i in range(1, len(df.columns)):
                col = df.columns.to_list()
                fig.add_trace(go.Scatter(
                    x=df.iloc[:, 0],
                    y=df.iloc[:, i],
                    showlegend=True,
                    name=col[i]))
            fig.update_layout(
                title=plottitle,
                xaxis_title="Time (s)",
                yaxis_title=ytype,
                font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"))

        def doubleplot(self, df1, df2, plottitle, ytype1, ytype2):
            col1 = df1.columns.to_list()
            col2 = df2.columns.to_list()
            for i in range(1, len(df1.columns)):
                fig.add_trace(go.Scatter(
                    x=df1.iloc[:, 0],
                    y=df1.iloc[:, i],
                    name=col1[i]),
                    secondary_y=False)
            for i in range(1, len(df2.columns)):
                fig.add_trace(go.Scatter(
                    x=df2.iloc[:, 0],
                    y=df2.iloc[:, i],
                    name=col2[i]),
                    secondary_y=True)
            fig.update_layout(title_text=plottitle)
            fig.update_xaxes(title_text="Time (s)")
            fig.update_yaxes(title_text=ytype1, secondary_y=False)
            fig.update_yaxes(title_text=ytype2, secondary_y=True)

        # If none of the sensors are selected, a blank plot will display that way we don't get an error
        if tcchecked ==0 and ptchecked ==0 and fmchecked == 0:
            fig = go.Figure()

        # If only one type of sensor is checked, then a plot is created with all the selected sensors of that type
        if 1 in tcsensors and ptchecked == 0 and fmchecked == 0:
            fig = go.Figure()
            singleplot(self, tcsensor2plot, 'TC Plot', 'Temperature (F)')
        if 1 in ptsensors and tcchecked == 0 and fmchecked == 0:
            fig = go.Figure()
            singleplot(self, ptsensor2plot, 'PT Plot', 'Pressure (psi)')
        if 1 in fmsensors and tcchecked == 0 and ptchecked == 0:
            fig = go.Figure()
            singleplot(self, fmsensor2plot, 'FM Plot', 'Flow Rate (cubic cm/s)')

        # If two different type of sensors are checked, then a plot is created with two y-axis
        if 1 in tcsensors and 1 in ptsensors and fmchecked == 0:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            doubleplot(self, tcsensor2plot, ptsensor2plot, 'TC & PT Plot', 'Temperature (F)', 'Pressure (psi)')
        if 1 in tcsensors and 1 in fmsensors and ptchecked == 0:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            doubleplot(self, tcsensor2plot, fmsensor2plot, 'TC & FM Plot', 'Temperature (F)', 'Flow Rate (cubic cm/s)')
        if 1 in ptsensors and 1 in fmsensors and tcchecked == 0:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            doubleplot(self, ptsensor2plot, fmsensor2plot, 'PT & FM Plot', 'Pressure (psi)', 'Flow Rate (cubic cm/s)')

        # If all three type of sensors are checked, then a plot is created with three y-axis
        if 1 in tcsensors and 1 in ptsensors and 1 in fmsensors:
            fig = go.Figure()
            coltc = tcsensor2plot.columns.to_list()         # Creates a list with selected sensors' name
            colpt = ptsensor2plot.columns.to_list()
            colfm = fmsensor2plot.columns.to_list()
            for i in range(1, len(tcsensor2plot.columns)):
                fig.add_trace(go.Scatter(
                    x=tcsensor2plot.iloc[:, 0],
                    y=tcsensor2plot.iloc[:, i],
                    name=coltc[i]))
            for i in range(1, len(ptsensor2plot.columns)):
                fig.add_trace(go.Scatter(
                    x=ptsensor2plot.iloc[:, 0],
                    y=ptsensor2plot.iloc[:, i],
                    name=colpt[i],
                    yaxis="y2"
                ))
            for i in range(1, len(fmsensor2plot.columns)):
                fig.add_trace(go.Scatter(
                    x=fmsensor2plot.iloc[:, 0],
                    y=fmsensor2plot.iloc[:, i],
                    name=colfm[i],
                    yaxis="y3"
                ))
            fig.update_layout(
                xaxis=dict(
                    title="Time (s)",
                    domain=[0,0.85]
                    ),
                yaxis=dict(title="Temperature (F)",
                           titlefont=dict(color="#1f77b4"),
                           tickfont=dict(color="#1f77b4")
                           ),
                yaxis2=dict(
                    title="Pressure (psi)",
                    titlefont=dict(color="#ff7f0e"),
                    tickfont=dict(color="#ff7f0e"),
                    anchor="x",
                    overlaying="y",
                    side="right"
                    ),
                yaxis3=dict(
                    title="Flow Rate (cubic cm/s",
                    titlefont=dict(color="#d62728"),
                    tickfont=dict(color="#d62728"),
                    anchor="free",
                    overlaying="y",
                    side="right",
                    position=0.95
                    ),
                )
            fig.update_layout(title_text="Sensor Plots")
        fig.show()

    # Defines the function that initiate plotting all TC, PT, or FM
    def allTC(self):
        fig = go.Figure()
        for i in range(1, len(self.ax1.columns)):
            col = self.ax1.columns.to_list()
            fig.add_trace(go.Scatter(
                x=self.ax1.iloc[:, 0],
                y=self.ax1.iloc[:, i],
                showlegend=True,
                name=col[i]))
        fig.update_layout(
            title="TC Plot",
            xaxis_title="Time (s)",
            yaxis_title="Temperature (F)",
            font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"))
        fig.show()
    def allPT(self):
        fig = go.Figure()
        for i in range(1, len(self.ax2.columns)):
            col = self.ax2.columns.to_list()
            fig.add_trace(go.Scatter(
                x=self.ax2.iloc[:, 0],
                y=self.ax2.iloc[:, i],
                showlegend=True,
                name=col[i]))
        fig.update_layout(
            title="PT Plot",
            xaxis_title="Time (s)",
            yaxis_title="Pressure (psi)",
            font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"))
        fig.show()
    def allFM(self):
        fig = go.Figure()
        for i in range(1, len(self.ax3.columns)):
            col = self.ax3.columns.to_list()
            fig.add_trace(go.Scatter(
                x=self.ax3.iloc[:, 0],
                y=self.ax3.iloc[:, i],
                showlegend=True,
                name=col[i]))
        fig.update_layout(
            title="TC Plot",
            xaxis_title="Time (s)",
            yaxis_title="Flow Rate (cubic cm/s)",
            font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"))
        fig.show()

    # Defines the function that initiates subplots for all sensors
    def allsensor(self):
        fig = make_subplots(rows=2, cols=2,
                            specs=[[{"secondary_y": True}, {"secondary_y": True}],
                                   [{"secondary_y": True}, {"secondary_y": True}]])
        for i in range(1, len(self.ax1.columns)):
            col1 = self.ax1.columns.to_list()
            fig.add_trace(go.Scatter(
                x=self.ax1.iloc[:, 0],
                y=self.ax1.iloc[:, i],
                name=col1[i]),
                row=1, col=1)
        for i in range(1, len(self.ax2.columns)):
            col2 = self.ax2.columns.to_list()
            fig.add_trace(go.Scatter(
                x=self.ax2.iloc[:, 0],
                y=self.ax2.iloc[:, i],
                name=col2[i],
                yaxis="y2"),
                row=2, col=1)
        for i in range(1, len(self.ax3.columns)):
            col3 = self.ax3.columns.to_list()
            fig.add_trace(go.Scatter(
                x=self.ax3.iloc[:, 0],
                y=self.ax3.iloc[:, i],
                name=col3[i],
                yaxis="y3"),
                row=1, col=2)
        fig.update_layout(
            yaxis=dict(title="Temperature (F)",
                       titlefont=dict(color="#1f77b4"),
                       tickfont=dict(color="#1f77b4")
                       ),
            yaxis2=dict(
                title="Pressure (psi)",
                titlefont=dict(color="#ff7f0e"),
                tickfont=dict(color="#ff7f0e"),
                anchor="free",
                overlaying="y",
                side="left",
                position=0.5
            ),
            yaxis3=dict(
                title="Flow Rate (cubic cm/s",
                titlefont=dict(color="#d62728"),
                tickfont=dict(color="#d62728"),
                anchor="free",
                overlaying="y",
                side="left",
                position=0.57
            ),
        )
        fig.update_layout(title_text="Sensor Plots")
        fig.show()

# Returns a 1 if sensor is selected and 0 if it isn't
# Use to select which sensor data to append to data set that is used to plot
# If the sensor returns a 1, the data for that sensor will be added to the data set that is used to plot
TCsensor1 = IntVar()
TCsensor2 = IntVar()
TCsensor3 = IntVar()
TCsensor4 = IntVar()
TCsensor5 = IntVar()
TCsensor6 = IntVar()
TCsensor7 = IntVar()

PTsensor1 = IntVar()
PTsensor2 = IntVar()
PTsensor3 = IntVar()
PTsensor4 = IntVar()
PTsensor5 = IntVar()
PTsensor6 = IntVar()
PTsensor7 = IntVar()

FMsensor1 = IntVar()
FMsensor2 = IntVar()

start=mclass(window)
window.mainloop()