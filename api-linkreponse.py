"""
# Sample Flask Application Test HTTP API

## Overview
This script is a flask application that simulates a HTTP API that supports pagination. 
It is designed to act as a mock User API to help developers test and implement client-side 
pagination logic.

## API Details

### Base URL:
- `http://192.168.0.24:5000/users`

### Query Parameters:
- `$top` (Optional): Specifies the maximum number of records to retrieve in the current request.
  Example: `http://192.168.0.24:5000/users?$top=5`

### Pagination:
- **Next Page Link Field**: `/@odata.nextLink`
  The API response includes a field `/@odata.nextLink` that points to the next page of records if more data is available.
  
- **Stop Condition**: 
  Pagination should stop when the field `/@odata.nextLink` is `NULL`, indicating no more pages to retrieve.

## Features:
- Simulates user data with pagination support.
- Useful for testing APIs that utilize OData conventions for pagination.

## Example Usage:
1. **Fetch Users**:
   Send a GET request to the URL with or without the `$top` parameter:
"""

from flask import Flask, jsonify, request
from urllib.parse import urlencode

app = Flask(__name__)

# Simulated data (list of users)
users = [
    {"id": 1, "name": "David Leavensworth"},
    {"id": 2, "name": "Aneta Jones"},
    {"id": 3, "name": "John McAvery"},
    {"id": 4, "name": "Richard Licorous"},
    {"id": 5, "name": "Paul Prown"},
    {"id": 6, "name": "Nathen Vee"},
    {"id": 7, "name": "Matthew Nick"},
    {"id": 8, "name": "Phillip Tick"},
    {"id": 9, "name": "Lavendar Han"},
    {"id": 10, "name": "Lady Gaga"},
    {"id": 11, "name": "Michael Jackson"},
    {"id": 12, "name": "Karen Martinez"},
    {"id": 13, "name": "Sharon Stone"},
    {"id": 14, "name": "Jarcec Walker"},
    {"id": 15, "name": "James Taylor"}
]

total_users = len(users)  # Total number of users

def paginate_users(offset, limit):
    start_index = offset
    end_index = min(offset + limit, len(users))
    return users[start_index:end_index]

@app.route('/users', methods=['GET'])
def get_users():
    top = int(request.args.get('$top', 5))  # Default to 5 if $top not provided
    skip_token = int(request.args.get('$skiptoken', 0))  # Default to 0 if $skiptoken not provided

    offset = skip_token

    current_users = paginate_users(offset, top)
    current_count = len(current_users)

    response_data = {
        "value": current_users,
        "count": current_count,
        "total": total_users
    }

    cumulative_count = offset + current_count
    response_data["cumulativeCount"] = cumulative_count

    if offset + top < total_users:
        next_link_params = {
            '$top': top,
            '$skiptoken': offset + top
        }
        next_link = f"{request.base_url}?{urlencode(next_link_params)}"
        response_data["@odata.nextLink"] = next_link

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.24', port=5000)
