#!/usr/bin/env python3
"""
Flask web application for displaying open data from various sources.
"""
from flask import Flask, render_template, request, jsonify
import requests
import io
import csv
import json
from typing import List, Dict, Any, Tuple

app = Flask(__name__)

DEFAULT_URL = "https://data.ntpc.gov.tw/api/datasets/781b822e-214a-4b9a-b4db-32c9f4626d98/csv/file"


def download(url: str) -> Tuple[bytes, str]:
    """Download content from URL and return content and content type."""
    try:
        resp = requests.get(url, timeout=20, verify=False)
        resp.raise_for_status()
        return resp.content, "success"
    except Exception as e:
        return None, str(e)


def try_parse_json(content: bytes):
    """Try to parse content as JSON."""
    try:
        return json.loads(content.decode("utf-8-sig"))
    except Exception:
        return None


def parse_csv(content: bytes) -> List[Dict[str, Any]]:
    """Parse CSV content."""
    text = content.decode("utf-8-sig")
    f = io.StringIO(text)
    reader = csv.reader(f)
    rows = list(reader)
    if not rows:
        return []
    header = rows[0]
    data_rows = rows[1:]
    result = []
    for r in data_rows:
        # pad shorter rows
        if len(r) < len(header):
            r += [""] * (len(header) - len(r))
        result.append({h: v for h, v in zip(header, r)})
    return result


def fetch_data(url: str) -> Tuple[List[Dict[str, Any]], List[str], str]:
    """
    Fetch and parse data from URL.
    Returns: (rows, available_columns, error_message)
    """
    content, error = download(url)
    if error != "success":
        return [], [], error

    # Try JSON first
    parsed_json = try_parse_json(content)
    if parsed_json is not None:
        # Normalize to a list of dicts
        if isinstance(parsed_json, dict):
            # find the first list value if present
            list_values = [v for v in parsed_json.values() if isinstance(v, list)]
            rows = list_values[0] if list_values else []
        elif isinstance(parsed_json, list):
            rows = parsed_json
        else:
            rows = []
        
        if rows and isinstance(rows[0], dict):
            headers = list(rows[0].keys())
            return rows, headers, ""
        else:
            return rows, [], ""

    # Fallback to CSV
    try:
        rows = parse_csv(content)
        if rows:
            headers = list(rows[0].keys())
            return rows, headers, ""
        else:
            return [], [], "No data found"
    except Exception as e:
        return [], [], f"Failed to parse content as CSV: {str(e)}"


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html', default_url=DEFAULT_URL)


@app.route('/api/fetch', methods=['POST'])
def api_fetch():
    """API endpoint to fetch data."""
    data = request.get_json()
    url = data.get('url', DEFAULT_URL)
    selected_columns = data.get('columns', [])
    
    rows, available_columns, error = fetch_data(url)
    
    if error:
        return jsonify({
            'success': False,
            'error': error,
            'rows': [],
            'available_columns': [],
            'total_records': 0
        })
    
    # Filter columns if specified
    if selected_columns:
        filtered_rows = []
        for row in rows:
            filtered_row = {col: row.get(col, "") for col in selected_columns if col in available_columns}
            filtered_rows.append(filtered_row)
        display_columns = selected_columns
        display_rows = filtered_rows
    else:
        display_columns = available_columns
        display_rows = rows
    
    return jsonify({
        'success': True,
        'rows': display_rows[:100],  # Limit to 100 rows for display
        'available_columns': available_columns,
        'selected_columns': display_columns,
        'total_records': len(rows),
        'displayed_records': min(len(display_rows), 100)
    })


@app.route('/api/columns', methods=['POST'])
def api_columns():
    """API endpoint to get available columns without fetching all data."""
    data = request.get_json()
    url = data.get('url', DEFAULT_URL)
    
    rows, available_columns, error = fetch_data(url)
    
    if error:
        return jsonify({
            'success': False,
            'error': error,
            'columns': []
        })
    
    return jsonify({
        'success': True,
        'columns': available_columns,
        'total_records': len(rows)
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
