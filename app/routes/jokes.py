from flask import Blueprint, jsonify, request
from app.models import db, Joke

jokes_bp = Blueprint('jokes', __name__)


@jokes_bp.route('/jokes', methods=['GET'])
def get_jokes():
    jokes = Joke.query.all()
    return (jsonify({
        "data": {"jokes": [{"id": j.id, "text": j.text} for j in jokes]},
        "status": "ok"
    }), 200)


@jokes_bp.route('/jokes', methods=['POST'])
def post_joke():
    body = request.get_json(silent=True)
    if not body or not body.get('text'):
        return (jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "The 'text' field is required."
            }
        }), 400)

    text = body['text']

    if text.strip() == '':
        return (jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "The 'text' field cannot be whitespace only."
            }
        }), 400)

    if len(text) > 500:
        return (jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "The 'text' field cannot exceed 500 characters."
            }
        }), 400)

    joke = Joke(text=text, submitted_by=1)
    db.session.add(joke)
    db.session.commit()

    return (jsonify({
        "data": {"id": joke.id, "text": joke.text},
        "status": "created"
    }), 201)
