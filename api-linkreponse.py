# Sample Flase Application Test HTTP API Stage "Link in response Field"
# Resource URL : http://192.168.0.24:5000/users?$top=5
# Next Page Link Field : /@odata.nextLink
# Stop Condition : ${record:value('/@odata.nextLink') == NULL}
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
