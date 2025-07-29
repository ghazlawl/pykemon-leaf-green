import pytesseract

# Set the tesseract executable location.
# TODO: Move this to the .env file.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def get_ocr_text(screenshot: any):
    """
    Uses the pytesseract library to extract the text from the specified
    image. This function mostly reliable but isn't perfect!

    Args:
        screenshot (Image): The screenshot to extract text from.

    Returns:
        str: The extracted text.

    Example:
        >>> _get_ocr_text(screenshot)
        not even a nibble...
        >>> _get_ocr_text(screenshot)
        you landed a pokemon!
    """

    # Use pytesseract to do OCR on the image.
    custom_config = r"--oem 3 --psm 6"
    text = pytesseract.image_to_string(screenshot, lang="eng", config=custom_config)
    text = text.strip()

    return text


def get_ocr_numbers(screenshot: any):
    # Use pytesseract to do OCR on the image.
    custom_config = r"--oem 3 --psm 6  -c tessedit_char_whitelist=0123456789"
    text = pytesseract.image_to_string(screenshot, lang="eng", config=custom_config)
    text = text.strip()

    return text
