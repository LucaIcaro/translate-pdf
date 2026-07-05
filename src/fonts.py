import fitz


DEJAVU_SANS_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def get_font_path() -> str:
    return DEJAVU_SANS_PATH


def font_available() -> bool:
    try:
        with open(DEJAVU_SANS_PATH, "rb"):
            return True
    except OSError:
        return False


def load_font() -> fitz.Font:
    return fitz.Font(fontbuffer=open(DEJAVU_SANS_PATH, "rb").read())
