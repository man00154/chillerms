# image_click.py
# Detect chiller ID by pixel coordinates from l1 layout image

IMAGE_WIDTH = 1800
IMAGE_HEIGHT = 900

ZONE_WIDTH = IMAGE_WIDTH // 10     # = 180 px
ZONE_HEIGHT = IMAGE_HEIGHT // 3    # = 300 px


def get_chiller_from_click(x, y):
    """Returns chiller ID (1–30) based on clicked pixel position."""

    if x < 0 or y < 0 or x > IMAGE_WIDTH or y > IMAGE_HEIGHT:
        return None

    col = int(x // ZONE_WIDTH)      # 0–9
    row = int(y // ZONE_HEIGHT)     # 0–2

    ch_id = row * 10 + col + 1      # 1–30

    if 1 <= ch_id <= 30:
        return ch_id
    return None
