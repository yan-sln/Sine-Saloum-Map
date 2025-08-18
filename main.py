# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 09:44:49 2022

Main "global variables" class for downloading SentinelHub data
and managing plotting parameters for KML/CSV overlay.

@author: yan-s
"""

import os
import logging
from typing import List, Tuple


class VariableGlobal:
    """Download satellite map from SentinelHub & plot data from GoogleEarth .kml file.

    What it does:
        - Download SentinelHub satellite map imagery.
        - Convert .kml file from GoogleEarth into a .csv file with names and coordinates.
        - Plot names with coordinates on the SentinelHub map download.

    Requirements:
        - SentinelHub credentials (https://www.sentinel-hub.com/).
        - .kml file exported from GoogleEarth or .csv with Name/Longitude/Latitude columns.
        - WGS84 coordinate system for inputs.

    Output:
        - Directory "SentinelDownload" containing:
            - Final .png file.
            - Optional .csv file.
            - Subdirectories with .json, .tiff & .png files from SentinelHub.

    Possible improvements:
        - Add shapefile support.
        - Add function to check if coordinates are outside BBox.
        - Improve documentation and customization options.
    """

    def __init__(self) -> None:
        """Initialize pseudo-global variables and manage working directory."""

        # Logging setup
        logging.basicConfig(
            level=logging.DEBUG,
            format="[%(levelname)s] %(asctime)s - %(message)s",
        )
        logging.getLogger("PIL").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("sentinelhub").setLevel(logging.WARNING)
        logging.getLogger("http.client").setLevel(logging.WARNING)
        logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
        logging.getLogger("requests.packages.urllib3").setLevel(logging.WARNING)

        # SentinelHub credentials
        self.instanceID: str = ""
        self.clientID: str = ""
        self.clientSecret: str = ""

        # Bounding box (WGS84)
        self.BBox: List[float] = [-16.9, 13.6, -16.3, 14.2]

        # SentinelHub download parameters
        self.resolution: int = 30  # meters/pixel
        self.timeInterval: str = "2019-06-01"
        self.intervalTime: str = "2022-07-25"

        # KML/CSV sources
        self.csvSrc: str = r""
        self.kmlSrc: str = r"../Sine Saloum 2.0.kml"

        # Plotting parameters
        self.figSize: Tuple[float, float] = (32.0, 24.0)
        self.dpi: float = 100.0
        self.figTitle: str = "Le Sine Saloum"
        self.xLabel: str = "05/08/2022"
        self.grid: bool = True
        self.locator: bool = True
        self.xMajor: float = 0.05
        self.yMajor: float = 0.05
        self.xMinor: int = 4
        self.yMinor: int = 4

        # Scale bar
        self.scale: bool = True
        self.xy: Tuple[float, float] = (-16.40, 13.6625)
        self.xyText: Tuple[float, float] = (-16.3495, 13.6625)
        self.arrowStyle: str = "<|-|>"
        self.nomenclature: str = "5 500m"
        self.xyNomenclature: Tuple[float, float] = (-16.3835, 13.664)

        # Label positioning lists
        self.listyUp: List[str] = [
            "Bambougar Massemba",
            "Bangalere",
            "Biogane",
            "Mar Lodj",
            "Palmarin Ngethé",
            "Soum",
        ]
        self.listyDown: List[str] = [
            "Bambougar Malech",
            "Bassar",
            "Fayako",
            "Diathanor",
            "Gagué Mode",
            "Joal-Fadiout",
            "Ndangane Sambou",
            "Velingara",
        ]

        # Label corrections and colors
        self.upperLonCorrection: float = -0.0005
        self.upperLatCorrection: float = 0.001
        self.upperColor: str = "red"

        self.upwardLonCorrection: float = -0.01
        self.upwardLatCorrection: float = 0.001
        self.upwardColor: str = "black"

        self.downwardLonCorrection: float = -0.013
        self.downwardLatCorrection: float = -0.004
        self.downwardColor: str = "black"

        self.normalLonCorrection: float = 0.0
        self.normalLatCorrection: float = 0.001
        self.normalColor: str = "black"

        self.arrowColor: str = "blue"

        # Working directory setup
        self.workingDirectory: str = self._init_working_directory()

    def _init_working_directory(self) -> str:
        """Ensure that 'SentinelDownload' directory exists and switch to it."""
        current_directory = os.path.basename(os.getcwd())
        if current_directory != "SentinelDownload":
            logging.warning("Start of SentinelHub downloading !")
            try:
                os.mkdir("SentinelDownload")
                logging.debug('Directory "SentinelDownload" successfully created!')
            except FileExistsError:
                logging.debug('Directory "SentinelDownload" already exists!')
            finally:
                os.chdir("SentinelDownload/")
        return os.getcwd()


if __name__ == "__main__":
    try:
        from SentinelHubDownload import SentinelHubDownload
        from PlotDATA import PlotDATA

        exe_seq = SentinelHubDownload()
        exe_seq.exeSeq()

        exe_seq = PlotDATA()
        exe_seq.exeSeq()
    except Exception as e:
        print(e)
