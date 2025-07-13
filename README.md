# photoOrganizer

This project provides utilities for organizing photos locally. The CLI can scan a folder for images, extract basic EXIF metadata, and classify each image into a coarse category (selfie, document, screenshot, nature, or other) before storing the results in a SQLite database.

Metadata is now stored as JSON. Existing databases created with earlier
versions may need to be recreated in order to retrieve metadata as
dictionaries.

## Prerequisites

This repository contains both the Python CLI and an Electron-based user
interface. In addition to Python 3, running the UI requires
[Node.js](https://nodejs.org/). Any recent LTS version (18 or later) will work.
Install it from the Node.js website or via your package manager if it's not
already available on your system.


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
Photos can also be grouped into events using `--group-events`. An event is
created whenever the time gap between consecutive photos exceeds a specified
number of hours (six by default). Each entry in the output metadata is assigned
an `event_id` identifying its event. For example:

```bash
python cli.py /path/to/photos --db photo.db --group-events
```

The gap threshold can be changed, e.g. `--group-events 12` uses a 12‑hour
separation. Events may be given a human-friendly name with
`photo_organizer.events.name_event(event_map, event_id, name)` or renamed later
with `rename_event`.
The resulting metadata stored in the database includes a `category` field for
each image describing its type. If an image is classified as a document or ID,
the text content is extracted using Tesseract (when available) and stored under
the `ocr_text` key.

Faces belonging to the same cluster may be labeled. Assign a label with
`--set-face-label` and retrieve it later using `--get-face-label`:

```bash
python cli.py --db photo.db --set-face-label 0 "Alice"
python cli.py --db photo.db --get-face-label 0
```

Labels are stored in the `face_labels` table of the SQLite database.

## UI

The project includes an Electron-based desktop application located in the `ui`
folder. It relies on Node.js, so ensure it is installed before continuing.

Run the UI in development mode:

```bash
cd ui
npm install
npm run dev
```

To create a production build:

```bash
npm run build
```

The Electron code invokes `python cli.py` under the hood using Node's
`child_process.spawn`. This means the Python CLI must be available in your
environment for the desktop app to process photos.

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
