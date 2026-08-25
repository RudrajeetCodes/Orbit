"""
vision_module.py
-----------------
Basic vision module for a larger project.

Scope (intentionally kept simple/reliable):
    - Capture the current screen (full or a region)
    - Run OCR on a captured/loaded image
    - Locate text and return its screen coordinates
    - No advanced CV, no model training, no fancy preprocessing

Designed to be imported and used by other modules/functions in the project:

    from vision_module import capture_screen, get_text_locations, find_text

Dependencies (install with pip):
    pip install mss pillow pytesseract

You also need the Tesseract OCR *engine* installed on the system (this is
separate from the pytesseract python package):
    - Windows: https://github.com/UB-Mannheim/tesseract/wiki
    - macOS:   brew install tesseract
    - Linux:   sudo apt-get install tesseract-ocr

If tesseract isn't on your PATH, set the path manually near the top of
this file (see TESSERACT_CMD below).
"""

import asyncio
import os
import tempfile
import time
from datetime import datetime
from urllib.parse import urlparse

import pytesseract
from dbus_next import Message, MessageType, Variant
from dbus_next.aio import MessageBus
from PIL import Image, ImageDraw

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# If tesseract isn't found automatically, uncomment and set the full path:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

DEFAULT_SAVE_DIR = "screenshots"
DEFAULT_MIN_CONFIDENCE = 60  # 0-100, OCR confidence threshold for a "hit"


# ---------------------------------------------------------------------------
# Screenshot capture
# ---------------------------------------------------------------------------


def capture_screen(region=None, save_path=None, monitor_index=1):
    """
    Capture the current screen through the GNOME Screenshot portal.

    Designed for Wayland. Uses raw D-Bus messages to avoid relying on
    portal introspection, which can fail with some GNOME interfaces.
    """

    if region is not None:
        raise NotImplementedError(
            "Region capture is not currently supported on Wayland."
        )

    async def _capture():
        bus = await MessageBus().connect()

        try:
            token = f"orbit_{os.getpid()}_{int(time.time() * 1000)}"

            # Call the Screenshot portal directly.
            reply = await bus.call(
                Message(
                    destination="org.freedesktop.portal.Desktop",
                    path="/org/freedesktop/portal/desktop",
                    interface="org.freedesktop.portal.Screenshot",
                    member="Screenshot",
                    signature="sa{sv}",
                    body=[
                        "",
                        {
                            "interactive": Variant("b", False),
                            "modal": Variant("b", False),
                            "handle_token": Variant("s", token),
                        },
                    ],
                )
            )

            if reply.message_type == MessageType.ERROR:
                raise RuntimeError(
                    f"Screenshot portal error: {reply.error_name}: {reply.body}"
                )

            request_path = reply.body[0]

            response_future = asyncio.get_running_loop().create_future()

            def on_message(message):
                if (
                    message.message_type == MessageType.SIGNAL
                    and message.path == request_path
                    and message.interface == "org.freedesktop.portal.Request"
                    and message.member == "Response"
                ):
                    if not response_future.done():
                        response_future.set_result(message.body)

            bus.add_message_handler(on_message)

            response, results = await response_future

            bus.remove_message_handler(on_message)

            if response != 0:
                raise RuntimeError(
                    f"Screenshot request failed with response code {response}"
                )

            uri_variant = results.get("uri")

            if uri_variant is None:
                raise RuntimeError("Screenshot portal returned no image URI.")

            screenshot_path = urlparse(uri_variant.value).path

            return screenshot_path

        finally:
            bus.disconnect()

    screenshot_path = asyncio.run(_capture())

    img = Image.open(screenshot_path).convert("RGB")

    if save_path:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        img.save(save_path)

    return img

def mask_regions(image, regions):
    """Mask excluded screen regions so OCR ignores them."""
    image = image.copy()
    draw = ImageDraw.Draw(image)

    for left, top, right, bottom in regions:
        draw.rectangle(
            (left, top, right, bottom),
            fill="black",
        )

    return image


def capture_screen_to_file(directory=DEFAULT_SAVE_DIR, prefix="screenshot"):
    """
    Convenience wrapper: capture the full screen and save it with an
    auto-generated timestamped filename.

    Returns:
        str: path to the saved screenshot file.
    """
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(directory, f"{prefix}_{timestamp}.png")
    capture_screen(save_path=path)
    return path


# ---------------------------------------------------------------------------
# OCR / text detection
# ---------------------------------------------------------------------------


def run_ocr(image):
    """
    Run basic OCR on an image and return the extracted text as a string.

    Args:
        image (PIL.Image.Image or str): a PIL image, or a path to an image
            file on disk.

    Returns:
        str: raw extracted text.
    """
    image = _load_image(image)
    return pytesseract.image_to_string(image)


def get_text_locations(image, min_confidence=DEFAULT_MIN_CONFIDENCE):
    """
    Run OCR and return every detected text chunk along with its
    coordinates and confidence score.

    Args:
        image (PIL.Image.Image or str): a PIL image, or a path to an image
            file on disk.
        min_confidence (int): ignore OCR results below this confidence
            (0-100).

    Returns:
        list[dict]: each dict has:
            {
                "text": str,
                "left": int, "top": int, "width": int, "height": int,
                "center_x": int, "center_y": int,
                "confidence": int
            }
    """
    image = _load_image(image)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    results = []
    n_boxes = len(data["text"])
    for i in range(n_boxes):
        text = data["text"][i].strip()
        conf_raw = data["conf"][i]

        # tesseract returns -1 for non-text regions; skip empty/low-confidence
        try:
            conf = int(float(conf_raw))
        except (ValueError, TypeError):
            conf = -1

        if not text or conf < min_confidence:
            continue

        left, top = data["left"][i], data["top"][i]
        width, height = data["width"][i], data["height"][i]

        results.append(
            {
                "text": text,
                "left": left,
                "top": top,
                "width": width,
                "height": height,
                "center_x": left + width // 2,
                "center_y": top + height // 2,
                "confidence": conf,
            }
        )

    return results


def find_text(
    image, target_text, case_sensitive=False, min_confidence=DEFAULT_MIN_CONFIDENCE
):
    """
    Search OCR results for a specific piece of text and return its
    location(s) if found.

    Args:
        image (PIL.Image.Image or str): image to search.
        target_text (str): text to look for (substring match).
        case_sensitive (bool): whether matching should respect case.
        min_confidence (int): OCR confidence threshold.

    Returns:
        list[dict]: matching entries from get_text_locations(), i.e. any
            detected text chunk that contains target_text.
    """
    locations = get_text_locations(image, min_confidence=min_confidence)

    if not case_sensitive:
        target_text = target_text.lower()

    matches = []
    for entry in locations:
        haystack = entry["text"] if case_sensitive else entry["text"].lower()
        if target_text in haystack:
            matches.append(entry)

    return matches


def find_text_center(
    image, target_text, case_sensitive=False, min_confidence=DEFAULT_MIN_CONFIDENCE
):
    """
    Find text on screen and return the center coordinates of the
    best matching result.
    """
    matches = find_text(
        image,
        target_text,
        case_sensitive=case_sensitive,
        min_confidence=min_confidence,
    )

    if not matches:
        return None

    # Prefer the highest-confidence match.
    best = max(matches, key=lambda entry: entry["confidence"])

    return best["center_x"], best["center_y"]


# ---------------------------------------------------------------------------
# Combined convenience function
# ---------------------------------------------------------------------------


def capture_and_find(
    target_text,
    region=None,
    case_sensitive=False,
    min_confidence=DEFAULT_MIN_CONFIDENCE,
):
    """
    Take a fresh screenshot and immediately search it for target_text.
    Useful as the main entry point other modules will likely call.

    Args:
        target_text (str): text to search for on screen.
        region (tuple, optional): (left, top, width, height) to limit the
            screenshot to a specific area.
        case_sensitive (bool): whether matching should respect case.
        min_confidence (int): OCR confidence threshold.

    Returns:
        list[dict]: matches, see find_text(). Note: if `region` was used,
            coordinates are relative to that region, not the full screen.
            Add region[0]/region[1] back in if you need absolute screen
            coordinates.
    """
    screenshot = capture_screen(region=region)
    return find_text(
        screenshot,
        target_text,
        case_sensitive=case_sensitive,
        min_confidence=min_confidence,
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _load_image(image):
    """Accept either a PIL Image or a file path and always return a PIL Image."""
    if isinstance(image, Image.Image):
        return image
    if isinstance(image, str):
        return Image.open(image)
    raise TypeError("image must be a PIL.Image.Image or a file path string")


# ---------------------------------------------------------------------------
# Simple self-test / demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Testing vision_module...")

    # 1. Capture screen
    print("1. Capturing screen...")
    shot_path = capture_screen_to_file()
    print(f"   Saved screenshot to: {shot_path}")

    # 2. Run OCR
    print("2. Running OCR...")
    text = run_ocr(shot_path)
    preview = text.strip().replace("\n", " ")[:150]
    print(f"   Extracted text (preview): {preview!r}")

    # 3. Get text + coordinates
    print("3. Locating text and coordinates...")
    locations = get_text_locations(shot_path)
    print(
        f"   Found {len(locations)} text elements with confidence >= {DEFAULT_MIN_CONFIDENCE}"
    )
    for entry in locations[:5]:
        print(
            f"     '{entry['text']}' at ({entry['center_x']}, {entry['center_y']}) "
            f"conf={entry['confidence']}"
        )

    print("Done.")
