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

Run the scanner:

```bash
python cli.py /path/to/photos --db photo.db
```
To group photos by location, pass `--group-by` with a level such as `city`:

```bash
python cli.py /path/to/photos --db photo.db --group-by city
```
The resulting metadata stored in the database includes a `category` field for
each image describing its type. If an image is classified as a document or ID,
the text content is extracted using Tesseract (when available) and stored under
the `ocr_text` key.

## Testing

Install the minimal dependencies for running the tests:

```bash
pip install -r dev-requirements.txt
```

Then execute the test suite with `pytest`:

```bash
pytest
```

Alternatively, run `make test` to set up a virtual environment and execute the
suite automatically.

The test suite relies only on images generated at runtime. No external image
files are required.
