# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 09:55:08 2022

@author: yan-s
"""

from main import VariableGlobal
import logging
import os
from csv import writer
from typing import List


class KmlCSV(VariableGlobal):
    """
    A class to convert a Google Earth KML file into a CSV file.

    0) __init__(): Initializes the class, checks for the input .kml file,
       and creates a DataFrame that is saved as a .csv file.
    1) filePrinter(): Processes the input .kml file and returns a list of lists
       that can be directly written into a .csv file.
    """

    def __init__(self) -> None:
        """
        Initializes the KmlCSV class, processes the KML file, and creates the CSV file.
        If the .kml file path is not provided, the user will be prompted to input it.
        """
        # Initialize the parent class (VariableGlobal) for shared resources and methods
        super().__init__()

        logging.warning("Starting the conversion from KML to CSV...")

        # Prompt for the .kml file path if not provided as input to the class
        if not self.kmlSrc:
            self.kmlSrc = input("Please provide the path to the Google Earth .kml file: ").strip().replace("'", "").replace('"', "")

        # Generate a list of rows (data) from the .kml file
        rows = self.filePrinter(self.kmlSrc)

        # Define the output path for the .csv file using the working directory and the title
        self.csvPath = os.path.join(self.workingDirectory, f"{self.title}.csv")

        # Write the rows into the .csv file
        try:
            with open(self.csvPath, "w", newline="", encoding="utf-8") as file:
                csv_writer = writer(file)
                csv_writer.writerows(rows)
            logging.warning(f"CSV file created successfully at: {self.csvPath}")
        except Exception as e:
            logging.error(f"Failed to write CSV file due to: {e}")

    def filePrinter(self, path: str) -> List[List[str]]:
        """
        Processes the KML file and extracts relevant data (names, coordinates).

        Args:
            path (str): The path to the KML file to be processed.

        Returns:
            list: A list of lists where each list contains the Name, Longitude, Latitude, and Altitude.
        """
        # Initialize the output list with column names for the CSV file
        output = [["Name", "Longitude", "Latitude", "Altitude"]]

        try:
            # Check if the provided file exists
            if not os.path.exists(path):
                logging.error(f"The file '{path}' does not exist!")
                raise FileNotFoundError(f"The file '{path}' does not exist.")

            # Open and read the .kml file line by line
            with open(path, "r", encoding="utf-8") as file:
                logging.debug("Started reading the KML file...")

                line_data = []  # Temporary list to store data for each point

                # Process each line in the KML file
                for line in file:
                    # Extract the title of the KML file (assuming it is within <name> tags)
                    if line.startswith("	<name>"):
                        self.title = line[7:-8].strip()
                        logging.debug(f"File Title: {self.title}")

                    # Extract the description (optional, used for logging)
                    if line.startswith("	<description>"):
                        description = line[14:-15].strip()
                        logging.debug(f"Description: {description}")

                    # Extract the name of the place (within <name> tags)
                    if line.startswith("		<name>"):
                        name = line[8:-8].strip()
                        line_data.append(name)

                    # Extract coordinates (Longitude, Latitude, and Altitude) from <coordinates> tag
                    if line.startswith("			<coordinates>"):
                        coordinates = line[16:-15].strip()
                        lon, lat, alt = coordinates.split(",")
                        line_data.extend([lon, lat, alt])

                    # If a full set of data (name + coordinates) is collected, add it to the output list
                    if len(line_data) >= 4:
                        output.append(line_data[-4:])  # Add last 4 elements (Name, Lon, Lat, Alt)
                        line_data = []  # Reset line_data for the next entry

                logging.debug("Finished reading the KML file...")

            return output  # Return the processed data
        except Exception as e:
            logging.error(f"Error processing the KML file: {e}")
            return []  # Return an empty list in case of error


if __name__ == "__main__":
    # Output the class documentation for understanding the purpose of this script
    print(KmlCSV.__doc__)
