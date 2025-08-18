import logging
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar

from .config import Config
from .utils import load_csv_data


class PlotData(Config):
    """Handle plotting of SentinelHub imagery with annotations."""

    def __init__(self, image_path: str, csv_path: str | None = None) -> None:
        super().__init__()
        self.image_path = image_path
        self.csv_path = csv_path or self.csv_src
        self.image = None

    def run(self) -> None:
        """Run full plotting sequence."""
        self.load_image()
        self.plot()

    def load_image(self) -> None:
        """Load the TIFF image from disk."""
        import rasterio

        logging.info("Loading image from %s", self.image_path)
        with rasterio.open(self.image_path) as src:
            self.image = src.read([1, 2, 3])  # RGB bands
            self.image = self.image.transpose((1, 2, 0))  # reshape to HWC

    def plot(self) -> None:
        """Display the satellite image with annotations."""
        if self.image is None:
            raise RuntimeError("Image not loaded. Call load_image() first.")

        fig, ax = plt.subplots(figsize=self.fig_size, dpi=self.dpi)
        ax.imshow(self.image)
        ax.set_title(self.fig_title)
        ax.set_xlabel(self.x_label)
        ax.grid(self.grid)

        if self.scale:
            scalebar = ScaleBar(
                dx=self.resolution,
                units="m",
                location="lower right",
                scale_loc="bottom",
                color="black",
            )
            ax.add_artist(scalebar)

        if self.csv_path:
            df = load_csv_data(self.csv_path)
            for _, row in df.iterrows():
                ax.scatter(row["lon"], row["lat"], c="red", s=40, marker="x")
                ax.text(
                    row["lon"] + self.normal_lon_correction,
                    row["lat"] + self.normal_lat_correction,
                    row["name"],
                    color=self.normal_color,
                    fontsize=8,
                )

        plt.show()
