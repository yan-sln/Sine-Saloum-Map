# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 09:58:36 2022

@author: yan-s
"""

from KmlCSV import KmlCSV
from main import VariableGlobal

import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
from cv2 import imread, imwrite, IMWRITE_PNG_COMPRESSION
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from typing import List, Tuple


class PlotDATA(KmlCSV):
    """Plots DATA on map using Name, Latitude & Longitude (WGS84) of a DataFrame.

    Methods:
    0) __init__() : If no .csv file is provided, creates one using .kml file from Google Earth.
    1) tiffPNG() : Converts .tiff file from sentinelHubDownload to .png file for use as a basemap.
    2) load() : Loads map & .csv file.
    3) axes() : Creates axes & subplot with Bounding Box, locator & nomenclature.
    4) listy() : Creates a second DataFrame and moves specific rows from the first DataFrame to it.
    5) plot() : Plots little arrows with coordinates & annotates 'Name' beside.
    6) show() : Displays the created map in the console.
    7) save() : Saves the newly created map locally.
    8) exeSeq() : Executes the full plotting sequence.

    Note: Most of these methods are just containers.
    """

    def __init__(self) -> None:
        """Initializes the parent class and prepares the plotting data."""
        super().__init__()

        # Check if a .csv file is provided
        if not self.csvSrc:
            # Create a .csv file from a Google Earth .kml file
            KmlCSV.__init__(self)
        else:
            # Use the provided .csv file
            self.csvPath = self.csvSrc

        logging.warning('Start of DATA plotting!')

    def tiffPNG(self) -> None:
        """Converts .tiff file to .png file using OpenCV."""
        # Get the latest directory and therefore, the latest .tiff file
        latest = sorted([d for d in os.listdir('.') if os.path.isdir(d)],
                        key=lambda x: os.path.getctime(x), reverse=True)[:1]

        # Set the path to the latest downloaded sentinelHub directory
        filePath = f'{self.workingDirectory}/{latest[0]}/'

        # Search for the .tiff file in the latest directory
        for infile in os.listdir(filePath):
            if infile.endswith('.tiff'):  # Ensure the file is a .tiff
                logging.info(f'File found: "{infile}"')
                outfile = infile.split('.')[0] + '.png'
                self.outfilePath = f'{filePath}{outfile}'

                # Check if the .png file already exists
                if not os.path.exists(self.outfilePath):
                    # Convert .tiff to .png
                    read = imread(filePath + infile)
                    imwrite(self.outfilePath, read, [int(IMWRITE_PNG_COMPRESSION), 0])
                    logging.debug(f'Converted successfully to {outfile}!')
                else:
                    logging.debug(f'File "{outfile}" already exists.')

    def load(self) -> None:
        """Loads the data from the .csv file and the map from the .png file."""
        try:
            self.df = pd.read_csv(self.csvPath)
            logging.info(f'Loaded data from "{self.csvPath}".')
        except Exception as e:
            logging.error(f'Error loading CSV file: {e}')
            quit()

        try:
            self.loadMap = plt.imread(self.outfilePath)
            logging.info(f'Loaded map from "{self.outfilePath}".')
        except Exception as e:
            logging.error(f'Error loading map: {e}')
            exit()

    def axes(self) -> None:
        """Creates and sets parameters of the axes for the map plot.

        Parameters:
            figSize (Tuple): Size of the figure (default is (32.0, 24.0)).
            dpi (float): Dots per inch for the figure (default is 100.0).
            figTitle (str): Title of the figure (default is 'Figure Title').
            xLabel (str): Label for the x-axis (default is 'Label at the Bottom').
            grid (bool): Whether to show a grid (default is True).
            locator (bool): Whether to add a locator (default is True).
            scale (bool): Whether to add a scale bar (default is True).
        """
        fig, self.ax = plt.subplots(figsize=self.figSize, dpi=self.dpi)

        # Define the bounding box
        self.BBox = [self.BBox[0], self.BBox[2], self.BBox[1], self.BBox[3]]
        logging.info(f'Bounding Box is: {self.BBox}.')

        # Set axis limits
        self.ax.set_xlim(self.BBox[0], self.BBox[1])
        self.ax.set_ylim(self.BBox[2], self.BBox[3])

        # Set title and labels
        self.ax.set_title(self.figTitle)
        self.ax.set_xlabel(self.xLabel)

        # Display grid if specified
        if self.grid:
            self.ax.grid()

        # Set up locator if specified
        if self.locator:
            self.ax.xaxis.set_major_locator(MultipleLocator(self.xMajor))
            self.ax.yaxis.set_major_locator(MultipleLocator(self.yMajor))
            self.ax.xaxis.set_minor_locator(AutoMinorLocator(self.xMinor))
            self.ax.yaxis.set_minor_locator(AutoMinorLocator(self.yMinor))

        # Add scale if specified
        if self.scale:
            plt.annotate('', xy=self.xy, xytext=self.xyText,
                         arrowprops=dict(arrowstyle=self.arrowStyle, shrinkA=0, shrinkB=0))
            self.ax.annotate(self.nomenclature, self.xyNomenclature)

        logging.info(f'Title is "{self.figTitle}".')

    def listy(self) -> None:
        """Moves rows from the main DataFrame to a secondary DataFrame based on the listyDown parameter.

        Parameters:
            listyDown (List[str]): Names of cities to be moved downward in the map.
        """
        # Create a second DataFrame for listyDown
        self.df2 = pd.DataFrame({'Name': [], 'Longitude': [], 'Latitude': [], 'Altitude': []})

        # Move 'Downward Name' from df to df2
        for name in self.listyDown:
            index = self.df[self.df['Name'] == name].index.values[0]
            self.df2 = pd.concat([self.df.loc[[index]], self.df2], ignore_index=True)
            self.df.drop(index=index, inplace=True)

        # Reset index of df
        self.df.reset_index(inplace=True)

    def plot(self) -> None:
        """Plots coordinates and places names with arrows on the map."""
        for idx, dat in self.df.iterrows():
            if dat.Name.isupper():
                self.ax.annotate(dat.Name, ((dat.Longitude + self.upperLonCorrection),
                                           (dat.Latitude + self.upperLatCorrection)), color=self.upperColor)
            else:
                if dat.Name in self.listyUp:
                    self.ax.annotate(dat.Name, ((dat.Longitude + self.upwardLonCorrection),
                                               (dat.Latitude + self.upwardLatCorrection)), color=self.upwardColor)
                else:
                    self.ax.annotate(dat.Name, ((dat.Longitude + self.normalLonCorrection),
                                               (dat.Latitude + self.normalLatCorrection)), color=self.normalColor)

            self.ax.scatter(dat.Longitude, dat.Latitude, zorder=1, alpha=0.8, color=self.arrowColor, s=10, marker='^')

        for idx, dat in self.df2.iterrows():
            self.ax.annotate(dat.Name, ((dat.Longitude + self.downwardLonCorrection),
                                        (dat.Latitude + self.downwardLatCorrection)), color=self.downwardColor)
            self.ax.scatter(dat.Longitude, dat.Latitude, zorder=1, alpha=0.8, color=self.arrowColor, s=10, marker='v')

    def show(self) -> None:
        """Displays the plot in the console."""
        self.ax.imshow(self.loadMap, zorder=0, extent=self.BBox, aspect='equal')

    def save(self) -> None:
        """Saves the figure locally."""
        plt.savefig(f'{self.figTitle}.png', bbox_inches='tight')
        logging.info(f'File saved as: "{self.workingDirectory}/{self.figTitle}.png"')

    def exeSeq(self) -> None:
        """Executes the full plotting sequence."""
        self.tiffPNG()
        self.load()
        self.axes()
        self.listy()
        self.plot()
        self.show()
        self.save()
        logging.warning('End of DATA plotting!')


if __name__ == '__main__':
    print(PlotDATA.__doc__)
