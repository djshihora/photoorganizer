# photoOrganizer

This project provides utilities for organizing photos locally. The initial CLI can scan a folder for images, extract basic EXIF metadata, and store the results in a SQLite database.

## Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the scanner:

```bash
python cli.py /path/to/photos --db photo.db
```
