# PassTheKeys technical test

This repository is intended to handle the technical test for Django Developer at PassTheKeys

## Requirements

- [Python-3.10.5](https://www.python.org/downloads/release/python-3105/)
- Docker

## Setup

- Create a virtualenv and activate it with the commands:

```
python3 -m venv env
source env/bin/activate
```

- Install the dependencies:
```
make install
```

- Generated the output file containing the outcode informations of the listings:

```
make generate-listings-outcode-csv-file
```

**Important**: A file with the host listings informations should existing in `/backend/listings.csv` for this command to work.

- Run the application
```
make run
```

- To run the tests use the command:
```
PYTHONPATH=. DJANGO_SETTINGS_MODULE='backend.settings' pytest
```

## Setup Using Docker

- Build the image with the command:
```
make build
```

- Run the image with the command:
```
make run-docker
```