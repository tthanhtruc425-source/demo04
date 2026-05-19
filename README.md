# Kaohsiung OpenData Reader

This small Python script downloads and displays the Kaohsiung City tourism events dataset.

Files added:
- `kaohsiung_opendata.py` — main script
- `requirements.txt` — Python dependencies

Quick start:

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the script (uses the default dataset URL):

```bash
python kaohsiung_opendata.py
```

You can also pass a different URL as the first argument.
