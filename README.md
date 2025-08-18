# Satellite Project

## Overview

This project provides a modular Python pipeline to:

1. Download satellite imagery from the **SentinelHub API**.
2. Convert **Google Earth KML files** into CSV format containing names and coordinates.
3. Plot the extracted points onto the satellite imagery with custom annotations.

The code is organized using an object-oriented design, ensuring that each component has a clear responsibility. This makes the system easier to maintain, test, and extend.

---

## Features

* Download high-resolution satellite maps from SentinelHub with minimal cloud coverage.
* Convert KML files into CSV format (compatible with WGS84 coordinates).
* Plot points on top of satellite imagery with customizable labels, corrections, and styling.
* Configurable via a central configuration file (`config.py` or `config.yaml`).

---

## Project Structure

```
satellite_project/
│
├── satellite/                 
│   ├── __init__.py
│   ├── config.py              # Global configuration
│   ├── downloader.py          # SentinelHubDownloader
│   ├── converter.py           # KmlCsvConverter
│   ├── plotter.py             # DataPlotter
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       ├── file_utils.py
│       └── geo_utils.py
│
├── scripts/                   
│   ├── download_and_plot.py   # Full pipeline execution
│   └── convert_kml.py         # Run only KML → CSV conversion
│
├── tests/                     
│   ├── test_downloader.py
│   ├── test_converter.py
│   └── test_plotter.py
│
├── requirements.txt
└── pyproject.toml
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/satellite_project.git
cd satellite_project
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Linux / MacOS
venv\Scripts\activate     # On Windows

pip install -r requirements.txt
```

---

## Configuration

Before running the pipeline, you must configure your SentinelHub credentials and project settings.

You can either:

* Edit `satellite/config.py` directly, or
* Create a `config.yaml` file with the following structure:

```yaml
instance_id: "your_instance_id"
client_id: "your_client_id"
client_secret: "your_client_secret"
bbox: [-16.9, 13.6, -16.3, 14.2]
resolution: 30
start_date: "2019-06-01"
end_date: "2022-07-25"
kml_path: "data/input.kml"
csv_path: null
output_dir: "SentinelDownload"
```

---

## Usage

### Run the full pipeline:

```bash
python scripts/download_and_plot.py
```

This will:

* Download imagery from SentinelHub,
* Convert the KML file to CSV (if needed),
* Plot the points on the satellite map,
* Save the final annotated image into the `SentinelDownload` directory.

### Convert only a KML file:

```bash
python scripts/convert_kml.py --input data/input.kml --output data/output.csv
```

---

## Requirements

* Python 3.9+
* sentinelhub-py
* pandas
* matplotlib
* opencv-python
* pyyaml

All dependencies are listed in `requirements.txt`.

---

## Future Improvements

* Add shapefile support for spatial inputs.
* Validate coordinates against the bounding box.
* Extend plotting options (color maps, layers, interactive visualization).
* Improve error handling and logging.

![V2 2](https://user-images.githubusercontent.com/110732997/220370356-804d294e-cd22-4a8b-aaeb-c1270a721d2c.png)
