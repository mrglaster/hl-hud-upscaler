import logging
import warnings


class LoggingConfiguration:

    @staticmethod
    def configure_logger():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        warnings.simplefilter(action='ignore', category=UserWarning)
        logging.basicConfig(level=logging.INFO, format='[HUD UPSCALER] %(asctime)s - %(levelname)s - %(message)s')