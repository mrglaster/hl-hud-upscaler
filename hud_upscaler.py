import argparse
import logging

from modules.banner.banner import BannerWriter
from modules.hud_upscaler.hud_upscaler import HudUpscaler
from modules.logging.logging_configuration import LoggingConfiguration


def main():
    LoggingConfiguration.configure_logger()
    parser = argparse.ArgumentParser(description="Half-Life HUD upscaling utility arguments")

    parser.add_argument("--path", type=str, required=True,
                        help="Path to directory with weapon sprites & weapon_NAME.txt")
    parser.add_argument("--umodel", type=str, required=False, default='edsr-base',
                        help="Upscaling model name (check the full list here: https://pypi.org/project/super-image/)")

    args = parser.parse_args()
    BannerWriter.write_banner()
    result = HudUpscaler.upscale_hud(args.path, args.umodel)
    if result:
        logging.info("Upscaling process was successfully completed!")
    else:
        logging.info("Upscaling process was finished with an error!")


if __name__ == '__main__':
    main()
