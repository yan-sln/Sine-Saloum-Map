#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to execute the full pipeline:
1. Download satellite data from SentinelHub.
2. Plot points from CSV/KML on the downloaded map.
"""

import logging
from satellite_map.downloader import SentinelHubDownload
from satellite_map.plotter import PlotData


def main() -> None:
    """Run the full sequence of download + plot."""
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    logging.info("Starting SentinelHub download...")
    downloader = SentinelHubDownload()
    downloader.run()

    logging.info("Starting plotting sequence...")
    plotter = PlotData()
    plotter.run()

    logging.info("Pipeline execution completed successfully.")


if __name__ == "__main__":
    main()
