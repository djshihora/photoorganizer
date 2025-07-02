# photoOrganizer

This project provides utilities for organizing photos locally. The CLI can scan a folder for images, extract basic EXIF metadata, and classify each image into a coarse category (selfie, document, screenshot, nature, or other) before storing the results in a SQLite database.

Metadata is now stored as JSON. Existing databases created with earlier
versions may need to be recreated in order to retrieve metadata as
dictionaries.


## Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

OCR features require the system `tesseract` executable. Install it with:

```bash
sudo apt-get install tesseract-ocr  # Ubuntu
brew install tesseract              # macOS (Homebrew)
```

Run the scanner:

```bash
python cli.py /path/to/photos --db photo.db
```
The resulting metadata stored in the database includes a `category` field for
each image describing its type. If an image is classified as a document or ID,
the text content is extracted using Tesseract (when available) and stored under
the `ocr_text` key.

## Testing

The test suite relies only on images generated at runtime. No external image
files are required.
