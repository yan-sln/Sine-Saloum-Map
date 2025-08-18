#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to plot data on top of a SentinelHub map.
"""

import logging
from satellite_map.plotter import PlotData


def main() -> None:
    """Run the plotting sequence."""
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    plotter = PlotData()
    plotter.run()


if __name__ == "__main__":
    main()
