import logging
import pandas as pd
import matplotlib.pyplot as plt
from lxml import etree


def plot_image(image, factor: float = 1.0, clip_range: tuple[float, float] | None = None):
    """Plot a numpy image array."""
    if clip_range:
        image = image.clip(*clip_range)
    plt.imshow(image * factor)
    plt.axis("off")
    plt.show()


def kml_to_csv(kml_path: str, csv_out: str) -> None:
    """Convert KML placemarks to CSV."""
    logging.info("Converting KML %s to CSV %s", kml_path, csv_out)

    with open(kml_path, "rb") as f:
        tree = etree.parse(f)

    names, lats, lons = [], [], []
    for placemark in tree.findall(".//{http://www.opengis.net/kml/2.2}Placemark"):
        name = placemark.find("{http://www.opengis.net/kml/2.2}name").text
        coords = placemark.find(".//{http://www.opengis.net/kml/2.2}coordinates").text
        lon, lat, *_ = map(float, coords.split(","))
        names.append(name)
        lats.append(lat)
        lons.append(lon)

    df = pd.DataFrame({"name": names, "lat": lats, "lon": lons})
    df.to_csv(csv_out, index=False)


def load_csv_data(path: str) -> pd.DataFrame:
    """Load CSV file into a normalized DataFrame.

    Normalizes column names to expected format:
      - 'Name'      -> 'name'
      - 'Longitude' -> 'lon'
      - 'Latitude'  -> 'lat'
      - 'Altitude'  -> 'alt' (if present)

    Args:
        path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame with standardized column names.
    """
    df = pd.read_csv(path)

    # Map legacy column names to standardized ones
    col_map = {
        "Name": "name",
        "Longitude": "lon",
        "Latitude": "lat",
        "Altitude": "alt",
    }
    df = df.rename(columns=col_map)

    # Sanity check
    required = {"name", "lon", "lat"}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV file {path} must contain at least {required}")

    return df
