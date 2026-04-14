from flask import Blueprint, jsonify, request, current_app

jokes_bp = Blueprint("jokes", __name__)

# ---- Configuration Constants ----
MAX_JOKE_LENGTH = 500

# ---- In-memory Store (for ICEX scope) ----
_jokes = []
_next_id = 1


def _validation_error(message):
    return jsonify(
        {
            "status": "error",
            "error": {
                "code": "VALIDATION_ERROR",
                "message": message,
            },
        }
    ), 400


@jokes_bp.route("/jokes", methods=["GET"])
def get_jokes():
    """
    Return all submitted jokes.
    """
    return jsonify(
        {
            "status": "ok",
            "data": {"jokes": _jokes},
        }
    ), 200


@jokes_bp.route("/jokes", methods=["POST"])
def post_joke():
    """
    Create a new joke with validation.

    Validation Rules:
    - 'text' field must exist
    - must not be empty or whitespace-only
    - must be <= MAX_JOKE_LENGTH characters
    """
    global _next_id

    body = request.get_json(silent=True)

    if not body or "text" not in body:
        return _validation_error("The 'text' field is required.")

    text = body["text"]

    if not isinstance(text, str):
        return _validation_error("The 'text' field must be a string.")

    stripped_text = text.strip()

    if not stripped_text:
        return _validation_error("The 'text' field cannot be empty.")

    if len(stripped_text) > MAX_JOKE_LENGTH:
        return _validation_error(
            f"The 'text' field must not exceed {MAX_JOKE_LENGTH} characters."
        )

    joke = {
        "id": _next_id,
        "text": stripped_text,
    }

    _jokes.append(joke)
    _next_id += 1

    # ---- Logging (Dev Lead requirement) ----
    current_app.logger.info(
        "Joke created",
        extra={
            "event": "joke_created",
            "user_id": None,
            "joke_id": joke["id"],
            "endpoint": "POST /jokes",
            "status_code": 201,
        },
    )

    return jsonify(
        {
            "status": "created",
            "data": joke,
        }
    ), 201
