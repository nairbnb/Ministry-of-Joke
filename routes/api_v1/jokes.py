from flask import jsonify
from app.models import Joke
from . import api_v1_bp

@api_v1_bp.route('/jokes/count', methods=['GET'])
def get_joke_count():
    """Return the total number of jokes in the database."""
    try:
        count = Joke.query.count()
        return jsonify({
            "data": {"count": count},
            "status": "ok"
        }), 200
    except Exception:
        # Standard error envelope for server failures
        return jsonify({
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Unable to retrieve joke count."
            }
        }), 500

@api_v1_bp.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": {
            "code": "NOT_FOUND",
            "message": "The requested resource does not exist."
        }
    }), 404

@api_v1_bp.errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        "error": {
            "code": "METHOD_NOT_ALLOWED",
            "message": "This HTTP method is not supported for this endpoint."
        }
    }), 405
