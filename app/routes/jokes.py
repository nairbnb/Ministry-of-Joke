from flask import Blueprint, jsonify, request

jokes_bp = Blueprint('jokes', __name__)

# In-memory store - no database yet. Week 9 will fix this.
_jokes = []

@jokes_bp.route('/jokes', methods=['GET'])
def get_jokes():
    return (jsonify({
        "data":
            {"jokes": _jokes},
        "status": "ok"
    }), 200)

@jokes_bp.route('/jokes', methods=['POST'])
def post_jokes():
    body = request.get_json(silent=True)
    if not body or not body.get('text'):
        return jsonify({
            "error": {
                "code": "VAILDATION_ERROR",
                "message": "The 'text' field is required."
            }
        }), 400
    joke = {"text": body['text']}
    _jokes.append(joke)
    return jsonify({
        "data": joke,
        "status": "ok"
    }), 201
