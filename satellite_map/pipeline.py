import logging
from pathlib import Path

from .downloader import SentinelHubDownload
from .plotter import PlotData


class Pipeline:
    """End-to-end pipeline: download imagery and plot results."""

    def __init__(self) -> None:
        self.downloader = SentinelHubDownload()

    def run(self) -> None:
        """Run the pipeline."""
        logging.info("Starting pipeline...")
        self.downloader.run()

        # Assume image saved in working dir
        output_dir = Path(self.downloader.working_directory)
        tiff_files = list(output_dir.glob("**/*.tiff"))

        if not tiff_files:
            logging.error("No TIFF image found!")
            return

        image_path = str(tiff_files[0])
        plotter = PlotData(image_path=image_path)
        plotter.load_image()
        plotter.plot()

        logging.info("Pipeline finished successfully.")
