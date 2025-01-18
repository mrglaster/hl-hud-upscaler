from pathlib import Path


class BannerWriter:

    @staticmethod
    def write_banner():
        with open(f'{Path(__file__).parent.resolve()}/banner.txt', 'r', encoding="utf_8_sig") as f:
            lines = f.readlines()
            for i in lines:
                print(i.replace('\n', ''))
        print()
