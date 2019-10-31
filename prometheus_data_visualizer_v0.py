import pandas as pd
import matplotlib.pyplot as plt

TC = pd.read_csv('promCleanTC.csv')
PT = pd.read_csv('promCleanPT.csv')
FM = pd.read_csv('promCleanFM.csv')

def shouldPlotType(question):
    answer = input(question + "(y/n): ").lower().strip()
    print("")
    while not(answer == "y" or answer == "yes" or
    answer == "n" or answer == "no"):
        print("Input yes or no")
        answer = input(question + "(y/n):").lower().strip()
        print("")
    if answer[0] == "y":
        return True
    else:
        return False


def main():
    if shouldPlotType("Plot TC's?"):
        ax1 = TC.drop(['Batch Num', 'Avg. Time'], axis=1)           #Creates TC dataset while ignoring Batch Num & Avg. Time
        ax1p = 1            #Need this variable to indicate that we want to plot this
    else:
        ax1 = None
        ax1p = None         #Need this variable to indicate that we want to ignore this

    if shouldPlotType("Plot PT's?"):
        ax2 = PT.drop(['Batch Num', 'Avg. Time'], axis=1)           #Creates PT dataset while ignoring Batch Num & Avg. Time
        ax2p = 1            #Need this variable to indicate that we want to plot this
    else:
        ax2 = None
        ax2p = None         #Need this variable to indicate that we want to ignore this

    if shouldPlotType("Plot Flow Meters?"):
        ax3 = FM.drop(['Batch Num', 'Avg. Time'], axis=1)           #Creates FM dataset while ignoring Batch Num & Avg. Time
        ax3p = 1            #Need this variable to indicate that we want to plot this
    else:
        ax3 = None
        ax3p = None         #Need this variable to indicate that we want to ignore this

    def singlePlot(df, type, ytype):
        df.plot(x='Mission Time', title=type)
        plt.xlabel('Time (s)')
        plt.ylabel(ytype)
        plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

    def doublePlot(df1, df2, type1, type2, ytype1, ytype2):
        fig, axes = plt.subplots(nrows=2, ncols=1)
        df1.plot(x='Mission Time', title=type1, ax=axes[0]).legend(bbox_to_anchor=(1, 1), loc='upper left')
        df2.plot(x='Mission Time', title=type2, ax=axes[1]).legend(bbox_to_anchor=(1, 1), loc='upper left')
        axes[0].set_xlabel('Time (s)')
        axes[0].set_ylabel(ytype1)
        axes[1].set_xlabel('Time (s)')
        axes[1].set_ylabel(ytype2)
        plt.tight_layout()

    def triplePlot(df1, df2, df3, type1, type2, type3):
        fig, axes = plt.subplots(figsize=(13, 7), nrows=2, ncols=2)
        df1.plot(x='Mission Time', title=type1, ax=axes[0, 0]).legend(bbox_to_anchor=(1, 1), loc='upper left')
        df2.plot(x='Mission Time', title=type2, ax=axes[1, 0]).legend(bbox_to_anchor=(1, 1), loc='upper left')
        df3.plot(x='Mission Time', title=type3, ax=axes[0, 1]).legend(bbox_to_anchor=(1, 1), loc='upper left')
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('Temperature (F)')
        axes[1, 0].set_xlabel('Time (s)')
        axes[1, 0].set_ylabel('Pressure (psi)')
        axes[0, 1].set_xlabel('Time (s)')
        axes[0, 1].set_ylabel('Flow (ft/s)')
        plt.tight_layout()


    # Single Plots%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if ax1p == 1 and ax2p == ax3p is None:
        singlePlot(ax1, 'TC Plot', 'Temperature (F)')

    if ax2p == 1 and ax1p == ax3p is None:
        singlePlot(ax2, 'PT Plot', 'Pressure (psi)')

    if ax3p == 1 and ax1p == ax2p is None:
        singlePlot(ax3, 'Flow Meter Plot', 'Flow (ft/s)')

    # Double Plots%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if ax1p == ax2p == 1 and ax3p is None:
        doublePlot(ax1, ax2, "TC Plot", "PT Plot", 'Temperature (F)', 'Pressure (psi)')

    if ax1p == ax3p == 1 and ax2p is None:
        doublePlot(ax1, ax3, 'TC Plot', 'Flow Meter Plot', 'Temperature (F)', 'Flow (ft/s)')

    if ax2p == ax3p == 1 and ax1p is None:
        doublePlot(ax2, ax3, "PT Plot", "Flow Meter Plot", 'Pressure (psi)', 'Flow (ft/s)')

    # Triple Plots%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if ax1p == ax2p == ax3p == 1:
        triplePlot(ax1, ax2, ax3, 'TC Plot', 'PT Plot', 'Flow Meter Plot')

    plt.show()

main()