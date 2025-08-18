#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to download satellite data from SentinelHub.
"""

import logging
from satellite_map.downloader import SentinelHubDownload


def main() -> None:
    """Run the SentinelHub download sequence."""
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    downloader = SentinelHubDownload()
    downloader.run()


if __name__ == "__main__":
    main()
