from flask import Blueprint, jsonify, request

"""
1st element : name of Blueprint
2nd element : location(module) - app.routes.jokes
"""
jokes_bp = Blueprint('jokes', __name__)

# In-memory store - no database yet.
_jokes = []

# If you receive GET request to /jokes, execute get_jokes()
@jokes_bp.route('/jokes', methods=['GET'])
def get_jokes():
    """
    Flask's jsonify function converts
    Python Dictionary -> HTTP JSON Response
    """
    return (jsonify({
        "data": {"jokes": _jokes},
        "status": "ok"
    }), 200)
    """
    When Flask receives a tuple as a return value, 
    it automatically interprets:
    - first element : Response Body
    - second element : HTTP status code
    """

@jokes_bp.route('/jokes', methods=['POST'])
def post_jokes():
    """
    HTTP Request from Browser or Postman
    -> Packets
    -> TCP protocol reassemble by OS
    -> request object

    .get_json() : parse request's body
                -> JSON
                -> Python Dictionary
    (silent=True) : if parsing fails,
                    return None instead of error.
    """
    body = request.get_json(silent=True)
    """
    not body : if body is None or empty dictionary, {}
    not body.get('text') : if body has no 'text' key or empty dictionary, {}
    """
    if not body or not body.get('text'):
        return (jsonify({
            "error": {
                "code": "VAILDATION_ERROR",
                "message": "The 'text' field is required."
            }
        }), 400)
    joke = {"text": body['text']}
    """
    java: arraylist.add(joke)
    """
    _jokes.append(joke)
    return (jsonify({
        "data": joke,
        "status": "ok"
    }), 201)
