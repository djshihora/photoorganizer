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
The resulting metadata stored in the database includes a `category` field for
each image describing its type.

## Testing

The test suite relies only on images generated at runtime. No external image
files are required.
