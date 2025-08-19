import logging
import os


class Config:
    """Configuration manager for global project settings."""

    def __init__(self) -> None:
        # SentinelHub credentials
        self.instance_id: str = ""
        self.client_id: str = ""
        self.client_secret: str = ""

        # SentinelHub parameters
        self.bbox = [-16.900000, 13.600000, -16.300000, 14.200000]
        self.resolution: int = 30
        self.time_interval: str = "2019-06-01"
        self.interval_time: str = "2022-07-25"

        # CSV / KML input
        self.csv_src: str = ""
        self.kml_src: str = "/data/Sine_Saloum.kml"

        # Plot parameters
        self.fig_size = (32.0, 24.0)
        self.dpi = 100.0
        self.fig_title = "Le Sine Saloum"
        self.x_label = "05/08/2022"
        self.grid = True
        self.locator = True
        self.x_major = 0.05
        self.y_major = 0.05
        self.x_minor = 4
        self.y_minor = 4

        # Scale bar
        self.scale = True
        self.xy = (-16.40, 13.6625)
        self.xy_text = (-16.3495, 13.6625)
        self.arrow_style = "<|-|>"
        self.nomenclature = "5 500m"
        self.xy_nomenclature = (-16.3835, 13.664)

        # Annotation lists
        self.listy_up = ["Bambougar Massemba", "Bangalere", "Biogane", "Mar Lodj",
                         "Palmarin Ngethé", "Soum"]
        self.listy_down = ["Bambougar Malech", "Bassar", "Fayako", "Diathanor",
                           "Gagué Mode", "Joal-Fadiout", "Ndangane Sambou", "Velingara"]

        # Annotation style
        self.upper_lon_correction = -0.0005
        self.upper_lat_correction = 0.001
        self.upper_color = "red"

        self.upward_lon_correction = -0.01
        self.upward_lat_correction = 0.001
        self.upward_color = "black"

        self.downward_lon_correction = -0.013
        self.downward_lat_correction = -0.004
        self.downward_color = "black"

        self.normal_lon_correction = 0
        self.normal_lat_correction = 0.001
        self.normal_color = "black"

        self.arrow_color = "blue"

        # Working directory
        self.working_directory = self._setup_working_dir()

        # Logging
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configure logging."""
        logging.basicConfig(
            level=logging.DEBUG,
            format="[%(levelname)s] %(asctime)s - %(message)s",
        )
        logging.getLogger("PIL").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("sentinelhub").setLevel(logging.WARNING)
        logging.getLogger("http.client").setLevel(logging.WARNING)
        logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

    def _setup_working_dir(self) -> str:
        """Ensure working directory exists."""
        current_directory = os.path.basename(os.getcwd())
        if current_directory != "SentinelDownload":
            logging.warning("Start of SentinelHub downloading !")
            try:
                os.mkdir("SentinelDownload")
                logging.debug("Directory 'SentinelDownload' successfully created!")
            except FileExistsError:
                logging.debug("Directory 'SentinelDownload' already exists!")
            os.chdir("SentinelDownload/")
        return os.getcwd()
