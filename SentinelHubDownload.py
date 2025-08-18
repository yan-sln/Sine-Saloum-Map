# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 09:46:12 2022

@author: yan-s
"""

import os
import logging
from time import sleep
from typing import Optional

from utils import plot_image
from sentinelhub import (
    CRS,
    BBox,
    SHConfig,
    DataCollection,
    MimeType,
    MosaickingOrder,
    SentinelHubRequest,
    bbox_to_dimensions,
)

from main import VariableGlobal


class SentinelHubDownload(VariableGlobal):
    """Download satellite DATA using the SentinelHub API.

    Methods:
    0) __init__() : Initializes the parent class VariableGlobal().
    1) config() : Loads SentinelHub credentials and checks them.
    2) sentinelParameters() : Sets resolution, BBox, and prepares evalscript.
    3) preRequest() : Prepares the request with config and all parameters.
    4) retrieveData() : Executes the request and uses already downloaded data if available.
    5) exeSeq() : Executes the full sequence of actions for downloading data.

    Note: Refer to the official documentation for more details:
    https://docs.sentinel-hub.com/api/latest/
    """

    def __init__(self) -> None:
        """Initializes the parent class VariableGlobal()."""
        super().__init__()

    def config(self) -> SHConfig:
        """Loads SentinelHub credentials and checks them.

        Returns:
            SHConfig: Config object containing SentinelHub credentials.
        """
        config = SHConfig()
        config.instance_id = self.instanceID
        config.sh_client_id = self.clientID
        config.sh_client_secret = self.clientSecret

        # Check if credentials are provided
        if not config.sh_client_id or not config.sh_client_secret:
            logging.warning("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

        return config

    def sentinelParameters(self) -> None:
        """Sets resolution, BBox, and prepares the evalscript for the satellite data."""
        resolution = self.resolution  # Satellite pixel resolution
        self.sentinelBBox = BBox(bbox=self.BBox, crs=CRS.WGS84)
        self.sentinelSize = bbox_to_dimensions(self.sentinelBBox, resolution=resolution)

        logging.info(f"Image shape at {resolution} m resolution: {self.sentinelSize} pixels")

        # Evalscript setup for Sentinel-2 imagery (true color and cloud mask)
        self.evalscript = """
        //VERSION=3
        function setup() {
          return {
            input: ["B02", "B03", "B04", "CLM"],
            output: { bands: 3 }
          }
        }

        function evaluatePixel(sample) {
          if (sample.CLM == 1) {
            return [0.75 + sample.B04, sample.B03, sample.B02]
          }
          return [3.5*sample.B04, 3.5*sample.B03, 3.5*sample.B02];
        }
        """

    def preRequest(self) -> None:
        """Prepares the request with configuration and parameters.

        This method sets up the SentinelHubRequest based on the configuration and input parameters.
        """
        self.request_true_color = SentinelHubRequest(
            data_folder=self.workingDirectory,
            evalscript=self.evalscript,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L1C,
                    time_interval=(self.timeInterval, self.intervalTime),
                    mosaicking_order=MosaickingOrder.LEAST_CC,
                )
            ],
            responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
            bbox=self.sentinelBBox,
            size=self.sentinelSize,
            config=self.config(),
        )

    def retrieveData(self) -> None:
        """Executes the request to retrieve satellite data.

        If the data is already downloaded, it uses the local data.
        """
        # Get data from SentinelHub API
        self.request_true_color.get_data(save_data=True)

        # Print the location of the saved data
        print("\nThe output directory has been created and a true color TIFF file was saved into the following structure:\n")
        for folder, _, filenames in os.walk(self.request_true_color.data_folder):
            for filename in filenames:
                print(os.path.join(folder, filename))

        # Retrieve the data mask and plot the image
        data_mask = self.request_true_color.get_data()
        plot_image(data_mask[0], factor=1 / 255)
        sleep(0.5)  # Just a slight delay to improve visualization
        print('\n')

    def exeSeq(self) -> None:
        """Executes the full sequence for downloading and displaying satellite data."""
        self.config()
        self.sentinelParameters()
        self.preRequest()
        self.retrieveData()
        logging.warning('End of SentinelHub downloading !\n')


if __name__ == '__main__':
    print(SentinelHubDownload.__doc__)
