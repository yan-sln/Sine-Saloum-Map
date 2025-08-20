import logging
import os
from time import sleep

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

from .config import Config
from .utils import plot_image


class SentinelHubDownload(Config):
    """Download satellite data using SentinelHub API."""

    def __init__(self) -> None:
        super().__init__()
        self.evalscript: str = ""
        self.sentinel_bbox: BBox | None = None
        self.sentinel_size: tuple[int, int] | None = None
        self.request_true_color: SentinelHubRequest | None = None

    def config_sh(self) -> SHConfig:
        """Load and validate SentinelHub credentials."""
        config = SHConfig()
        config.instance_id = self.instance_id
        config.sh_client_id = self.client_id
        config.sh_client_secret = self.client_secret

        if not config.sh_client_id or not config.sh_client_secret:
            logging.warning(
                "Missing credentials! Provide SentinelHub client ID and secret."
            )
        return config

    def sentinel_parameters(self) -> None:
        """Set resolution, bounding box, and evalscript."""
        resolution = self.resolution
        self.sentinel_bbox = BBox(bbox=self.bbox, crs=CRS.WGS84)
        self.sentinel_size = bbox_to_dimensions(self.sentinel_bbox, resolution=resolution)
        logging.info(
            "Image shape at %d m resolution: %s pixels", resolution, self.sentinel_size
        )

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

    def prepare_request(self) -> None:
        """Prepare SentinelHub request."""
        self.request_true_color = SentinelHubRequest(
            data_folder=self.working_directory,
            evalscript=self.evalscript,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L1C,
                    time_interval=(self.time_interval, self.interval_time),
                    mosaicking_order=MosaickingOrder.LEAST_CC,
                )
            ],
            responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
            bbox=self.sentinel_bbox,
            size=self.sentinel_size,
            config=self.config_sh(),
        )

    def retrieve_data(self) -> None:
        """Execute request and fetch data."""
        if self.request_true_color is None:
            raise RuntimeError("Request not prepared. Call prepare_request() first.")

        self.request_true_color.get_data(save_data=True)

        print("\nData downloaded and saved at:\n")
        for folder, _, filenames in os.walk(self.request_true_color.data_folder):
            for filename in filenames:
                print(os.path.join(folder, filename))

        data_mask = self.request_true_color.get_data()
        plot_image(data_mask[0], factor=1 / 255)
        sleep(0.5)
        print("\n")

    def run(self) -> None:
        """Run full download sequence."""
        self.sentinel_parameters()
        self.prepare_request()
        self.retrieve_data()
        logging.warning("End of SentinelHub downloading!\n")
