import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


class draw_holes:
    
    def __init__(self, from_ct, to_ct, hole_type):
        '''
        Draws plots for headings / CTs of floor drilling respective to the RL of the floor 
        And the extrapolated GML seam.
        '''
        self.input_from_ct = from_ct
        self.input_to_ct = to_ct
        self.input_hole_type = hole_type
        self.canvas_fig, self.canvas_axes = plt.subplots()

    def set_canvas_fig(self, fig):
        self.canvas_fig = fig
    
    def set_canvas_axes(self, ax):
        self.canvas_axes = ax

    def get_canvas_fig(self):
        return self.canvas_fig
    
    def get_canvas_axes(self):
        return self.canvas_axes

    def show_graphs(self):
        plt.subplots_adjust(hspace=.35)
        plt.get_current_fig_manager().window.state('zoomed')
        plt.show()

    def baseline_b(self, x):
        """ 
        Creates an interpolated line of the MG106 B heading 
        roadway between the given Cut Throughs.
        :param x: chainages as given by the drill data for the given roadway
        :return: Array of RL values associated to a respective chainage
        """
        if self.input_from_ct == 21 and self.input_to_ct == 22:
            return -0.00009*x**2 - 0.09252*x - 139.95001
        elif self.input_from_ct == 22 and self.input_to_ct == 23:
            return -0.0001*x**2 - 0.05765*x - 152.8635
        elif self.input_from_ct == 23 and self.input_to_ct == 24:
            return -0.000005*x**3 + 0.0012*x**2 - 0.1056*x - 161.48
        else:
            return ValueError

    def baseline_c(self, x):
        """ 
        Creates an interpolated line of the MG106 C heading 
        roadway between the given Cut Throughs.
        :param x: chainages as given by the drill data for the given roadway
        :return: Array of RL values associated to a respective chainage
        """

        if self.input_from_ct == 21 and self.input_to_ct == 22:
            return 0.00005*x**2 - 0.10774*x - 139.24042
        elif self.input_from_ct == 22 and self.input_to_ct == 23:
            return 0.00012*x**2 - 0.07897*x - 152.2284
        elif self.input_from_ct == 23 and self.input_to_ct == 24:
            return -1
        else:
            return ValueError

    def baseline_c_b(self, x):
        """ 
        Creates an interpolated line of the MG106 C-B Cuthroughs as provided
        :param x: chainages as given by the drill data for the given CT
        :return: Array of RL values associated to a respective chainage
        """

        if self.input_from_ct == 22 and self.input_to_ct == 22:
            return -0.000007*x**3 + 0.0010256*x**2 - 0.0486984*x - 151.7854722

        elif self.input_from_ct == 23 and self.input_to_ct == 23:
            return  -0.00021*x**2 - 0.00402 *x - 160.56427
        else:
            return ValueError

    def plots(self):
        """ 
        Plots the roadway and drill hole data for the given roadway based select input
        parameters. Plots the holes, RL of the floor, reported gas emission depth
        and an interpolated RL of the GML seam
        """
        # Retrieve the historical drill log data via file location
        data = pd.read_excel("Drill Sheet data log v3.0.xlsx", sheet_name="Historical Table")

        if (self.input_from_ct != self.input_to_ct):
        
            # C heading Data filter
            heading_c = data["Heading"] == "C"
            from_ct = data["From (C/t)"] == self.input_from_ct
            to_ct = data["To (C/t)"] == self.input_to_ct
            hole_type = data["Hole type"] == self.input_hole_type
            
            C_hdg = data[heading_c & from_ct & to_ct & hole_type]           

            # Chainage data for holes drilled in B hdg
            x_chainage_c = C_hdg["Chainage"].values

            # RL of GM/Development floor depth 
            y_floor_c = C_hdg["Floor Depth (RL)"].values

            # Drill depth of hole
            y_hole_depth_c = C_hdg["Hole Depth (RL)"].values

            # RL of apparent GML depth
            gml_depth_c = C_hdg["GML Depth (RL)"].values

            # RL of gas release Depth
            gas_release_depth_c = C_hdg["Gas Release RL"].values

            # B heading Data filter
            heading_b = data["Heading"] == "B"
            from_ct = data["From (C/t)"] == self.input_from_ct
            to_ct = data["To (C/t)"] == self.input_to_ct
            hole_type = data["Hole type"] == self.input_hole_type

            B_hdg = data[heading_b & from_ct & to_ct & hole_type]

            # Chainage data for holes drilled in B hdg
            x_chainage_b = B_hdg["Chainage"].values

            # RL of GM/Development floor depth 
            y_floor_b = B_hdg["Floor Depth (RL)"].values

            # Drill depth of hole
            y_hole_depth_b = B_hdg["Hole Depth (RL)"].values

            # RL of apparent GML depth
            gml_depth_b = B_hdg["GML Depth (RL)"].values

            # RL of gas release Depth
            gas_release_depth_b = B_hdg["Gas Release RL"].values

            # Plot creation; Figure and axes of the plot
            fig, ax = plt.subplots(2)
            
            # interpolation of the GML depth based on drill logs
            f_b = interp1d(x_chainage_b, gml_depth_b, kind="slinear")
            x_b_new = np.linspace(min(x_chainage_b), max(x_chainage_b), num=10)
            y_b_new = f_b(x_b_new)

            ax[1].plot(x_b_new, y_b_new, '--', color="r", label="Approximate GML")

            # interpolation of the GML depth based on drill logs
            f_c = interp1d(x_chainage_c, gml_depth_c, kind="slinear")
            x_c_new = np.linspace(min(x_chainage_c), max(x_chainage_c), num=10)
            y_c_new = f_c(x_c_new)

            ax[0].plot(x_c_new, y_c_new, '--', color="r", label="Approximate GML")

            #plot of the chainage vs the final drill depth (RL). Shows the accuracy of drilling
            ax[1].scatter(x_chainage_b, y_hole_depth_b, label="Drill Depth (RL)", color='grey', marker=11)
        
            # plot of the chainage vs the Floor depth (RL). this line simulates the GML depth based on RL
            ax[1].plot(x_chainage_b, self.baseline_b(x_chainage_b), 'g', label="Floor RL")
         
            # plot area of apparent gas release from drilling logs
            ax[1].scatter(x_chainage_b, gas_release_depth_b, label="Gas Release Depth (m)", marker="x")

            #plot of the chainage vs the final drill depth (RL). Shows the accuracy of drilling
            ax[0].scatter(x_chainage_c, y_hole_depth_c, label="Drill Depth (RL)", color='grey', marker=11)
      
            # plot of the chainage vs the Floor depth (RL). this line simulates the GML depth based on RL
            ax[0].plot(x_chainage_c, self.baseline_c(x_chainage_c), 'g', label="Floor RL")

            # plot area of apparent gas release from drilling logs
            ax[0].scatter(x_chainage_c, gas_release_depth_c, label="Gas Release Depth (m)", color="black", marker="x")

            # Plot drilled holes against average GML seam
            ax[1].vlines(x=x_chainage_b, ymin=y_hole_depth_b, ymax=self.baseline_b(x_chainage_b), color='grey', label="Drilled holes")
            ax[0].vlines(x=x_chainage_c, ymin=y_hole_depth_c, ymax=self.baseline_c(x_chainage_c), color='grey', label="Drilled holes")

            # Move x-axis to top of plot, add legend
            ax[0].xaxis.tick_top()
            ax[0].xaxis.set_ticks(np.arange(min(x_chainage_c), max(x_chainage_c), 10))
            ax[0].legend(loc="upper right")

            # Move x-axis to top of plot
            ax[1].xaxis.tick_top()
            ax[1].xaxis.set_ticks(np.arange(min(x_chainage_b), max(x_chainage_b), 10))
            ax[1].legend(loc="upper right")

            # Labels for each plot
            ax[0].set_xlabel("Chainage")
            ax[0].set_ylabel("Hole Depth")
            ax[0].set_title(f"{self.input_hole_type} Holes in {self.input_from_ct}-{self.input_to_ct} CT C Heading")

            ax[1].set_xlabel("Chainage")
            ax[1].set_ylabel("Hole Depth")
            ax[1].set_title(f"{self.input_hole_type} Holes in {self.input_from_ct}-{self.input_to_ct} CT B Heading")

            # Set Figure and axes
            self.set_canvas_fig(fig)
            self.set_canvas_axes(ax)


        elif self.input_from_ct == self.input_to_ct:
            
            # Filter data to ensure C-B CT values are selected
            heading_c_b = data["Heading"] == "C-B"
            to_ct = data["From (C/t)"] == self.input_from_ct
            hole_type = data["Hole type"] == self.input_hole_type

            # Filters data based on heading and hole type
            C_B_hdg = data[heading_c_b & to_ct & hole_type]

            # Chainage data for holes drilled in B hdg
            x_chainage = C_B_hdg["Chainage"].values

            # RL of GM/Development floor depth 
            y_floor = C_B_hdg["Floor Depth (RL)"].values

            # Drill depth of hole
            y_hole_depth = C_B_hdg["Hole Depth (RL)"].values

            # RL of apparent GML depth
            gml_depth = C_B_hdg["GML Depth (RL)"].values

            # RL of gas release Depth
            gas_release_depth = C_B_hdg["Gas Release RL"].values

            #figure and axies of plot
            fig, ax = plt.subplots()
            
            # interpolated gml depth 
            f = interp1d(x_chainage, gml_depth, kind="slinear")
            x_new = np.linspace(min(x_chainage), max(x_chainage), num=10)
            y_new = f(x_new)

            # plot of the approximate GML based on interpolated data
            ax.plot(x_new, y_new, '--', color="r", label="Approximate GML")

            #plot of the chainage vs the final drill depth (RL). Shows the accuracy of drilling
            ax.scatter(x_chainage, y_hole_depth, label="Drill Depth (RL)", color='grey', marker=11)

            # plot of the chainage vs the Floor depth (RL). this line simulates the GML depth based on RL
            ax.plot(x_chainage, self.baseline_c_b(x_chainage), 'g', label="Floor RL")

            # plot area of apparent gas release from drilling logs
            ax.scatter(x_chainage, gas_release_depth, label="Gas Release Depth (m)", marker="x")

            # Plot drilled holes against average GML seam
            ax.vlines(x=x_chainage, ymin=y_hole_depth, ymax=self.baseline_c_b(x_chainage), color='grey', label="Drilled holes")

            # Move x-axis to top of plot
            ax.xaxis.tick_top()
            ax.xaxis.set_ticks(np.arange(min(x_chainage), max(x_chainage), 10))
            ax.legend(loc="upper right")

            ax.set_xlabel("Chainage")
            ax.set_ylabel("Hole Depth")
            ax.set_title(f"{self.input_hole_type} Holes in {self.input_from_ct} CT")

            # Set Figure and axes
            self.set_canvas_fig(fig)
            self.set_canvas_axes(ax)

# Define a class for the SMOS data visualizer
class SMOS_data_visualiser:

    def __init__(self, root):
        '''
        Creates the display window using user inputs for starting cut-through (CT), ending CT, and hole type.
        Initializes variables and UI elements.
        '''
        
        # Initialize some instance variables
        self.start, self.end, self.hole = 0, 0, 0
        self.root = root
        self.var1, self.var2, self.var3 = tk.StringVar(root), tk.StringVar(root), tk.StringVar(root)

        self.frame1 = ttk.Frame(root)
        self.frame2 = ttk.Frame(root)

        self.canvas = None
        self.figure = None

        # Create the UI widgets
        self.create_widgets(self.root)

    
    def select_start(self, var):
        '''
        Callback function for selecting the starting cut-through
        '''
        self.var1 = var
        self.start = var

    
    def select_end(self, var):
        '''
        Callback function for selecting the ending cut-through
        '''
        self.end = var
        self.var2 = var

    
    def select_hole_type(self, var):
        '''
        Callback function for selecting the hole type
        '''
        self.hole = var
        self.var3 = var

    def plot_graphs(self):
        '''
        Plot graphs using data from the Roadway_GML_map_viewer class
        '''
        # Start by destroying the existing widgets in Frame1
        self.clear_graphs()
        self.frame1 = ttk.Frame(root)

        # Use inputs to extract data from the Roadway_GML_map_viewer and create a canvas
        new_plots = draw_holes(int(self.var1.get()), int(self.var2.get()), self.var3.get())
        new_plots.plots()
        figure = new_plots.get_canvas_fig()

        canvas = FigureCanvasTkAgg(figure, master=self.frame1)
        self.frame1.pack(fill=tk.BOTH, expand=True)

        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        root.state('zoomed')
        canvas.draw()

    def clear_graphs(self):
        '''
        Clear existing graphs by destroying the frame
        '''
        self.frame1.destroy()

    def show_control_btns(self):
        '''
        Display control buttons for different plot options
        '''

        # Plot Option controllers
        option_1 = tk.Button(master=button_frame, text="GML", bg="red", command=lambda x: x == 0)
        option_2 = tk.Button(master=button_frame, text="Drill Depth", bg="red", command=lambda x: x == 0)
        option_3 = tk.Button(master=button_frame, text="Gas Release Depth", bg="red", command=lambda x: x == 0)
        option_4 = tk.Button(master=button_frame, text="Drilled holes", bg="red", command=lambda x: x == 0)
        
        #Frame for option buttons
        button_frame = ttk.Frame(master=root)
        
        button_frame.pack(fill=tk.BOTH, side="left")
        option_1.pack(fill=tk.NONE)
        option_2.pack(fill=tk.NONE)
        option_3.pack(fill=tk.NONE)
        option_4.pack(fill=tk.NONE)

    def create_widgets(self, root):
        '''
        Create the main UI widgets and layout
        '''
        root.title("SMOS Floor data visualizer")
        header = tk.Label(text="Pick an Application")
        frame2 = ttk.Frame(master=root)

        var1 = tk.StringVar(root)
        var2 = tk.StringVar(root)
        var3 = tk.StringVar(root)

        # Values for user options
        start_ct = [21, 22, 23]
        end_ct = [22, 23, 24]
        hole_type = ["Relief", "Centreline Easer"]

        var1.set("Start CT")
        var2.set("End CT")
        var3.set("Hole Type")

        # Selection Dropdown
        dropdown1 = tk.OptionMenu(frame2, var1, *start_ct, command=lambda var: self.select_start(var1))
        dropdown2 = tk.OptionMenu(frame2, var2, *end_ct, command=lambda var: self.select_end(var2))
        dropdown3 = tk.OptionMenu(frame2, var3, *hole_type, command=lambda var: self.select_hole_type(var3))

        # Action Buttons
        plot_btn = tk.Button(master=frame2, text="Plot", bg="red", command=self.plot_graphs)
        clear_btn = tk.Button(master=frame2, text="Clear", bg="white", command=self.clear_graphs)
        close_btn = tk.Button(master=frame2, text="Close", command=exit)

        frame2.pack(fill=tk.NONE, expand=False)
        dropdown1.pack(fill=tk.NONE, side="left")
        dropdown2.pack(fill=tk.NONE, side="left")
        dropdown3.pack(fill=tk.NONE, side="left")
        plot_btn.pack(fill=tk.NONE, side="left")
        clear_btn.pack(fill=tk.NONE, side="left")
        close_btn.pack(fill=tk.NONE, side="right")

if __name__ == "__main__":
    root = tk.Tk()
    app = SMOS_data_visualiser(root)
    root.mainloop()