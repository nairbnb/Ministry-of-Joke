from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models import db, Rating, Joke

ratings_bp = Blueprint('ratings', __name__)


@ratings_bp.route('/jokes/<int:joke_id>/ratings', methods=['POST'])
@login_required
def create_rating(joke_id):
    """Create a new rating for a joke. Non-idempotent — use PUT to update."""
    joke = Joke.query.get(joke_id)
    if joke is None:
        return jsonify({'error': {'code': 'NOT_FOUND',
                                  'message': 'Joke not found'}}), 404

    data = request.get_json()

    for axis in ['funniness', 'appropriateness', 'originality']:
        value = data.get(axis) if data else None
        if not isinstance(value, int) or not (1 <= value <= 5):
            msg = f'{axis} must be an integer between 1 and 5'
            return jsonify({'error': {'code': 'INVALID_INPUT',
                                      'message': msg}}), 400

    existing = Rating.query.filter_by(
        user_id=current_user.id,
        joke_id=joke_id
    ).first()
    if existing:
        return jsonify({'error': {'code': 'DUPLICATE_RATING',
                                  'message': 'You have already rated this joke'}}), 409

    rating = Rating(
        user_id=current_user.id,
        joke_id=joke_id,
        funniness=data['funniness'],
        appropriateness=data['appropriateness'],
        originality=data['originality']
    )
    db.session.add(rating)
    db.session.commit()

    current_app.logger.info(
        "Rating created",
        extra={
            "event": "rating_created",
            "user_id": current_user.id,
            "joke_id": joke_id,
            "funniness": data['funniness'],
            "appropriateness": data['appropriateness'],
            "originality": data['originality'],
            "endpoint": "POST /jokes/<id>/ratings",
            "status_code": 201
        }
    )

    return jsonify({
        'id': rating.id,
        'joke_id': rating.joke_id,
        'user_id': rating.user_id,
        'funniness': rating.funniness,
        'appropriateness': rating.appropriateness,
        'originality': rating.originality,
        'created_at': rating.created_at.isoformat()
    }), 201


@ratings_bp.route('/jokes/<int:joke_id>/ratings/me', methods=['GET'])
@login_required
def get_my_rating(joke_id):
    """Get the current user's rating for a joke."""
    rating = Rating.query.filter_by(
        user_id=current_user.id,
        joke_id=joke_id
    ).first()

    if rating is None:
        return jsonify({'error': {'code': 'NOT_FOUND',
                                  'message': 'You have not rated this joke'}}), 404

    return jsonify({
        'id': rating.id,
        'joke_id': rating.joke_id,
        'user_id': rating.user_id,
        'funniness': rating.funniness,
        'appropriateness': rating.appropriateness,
        'originality': rating.originality,
        'created_at': rating.created_at.isoformat()
    }), 200


@ratings_bp.route('/jokes/<int:joke_id>/ratings/me', methods=['PUT'])
@login_required
def update_my_rating(joke_id):
    """Update the current user's rating. Idempotent — safe to retry."""
    rating = Rating.query.filter_by(
        user_id=current_user.id,
        joke_id=joke_id
    ).first()
    if rating is None:
        return jsonify({'error': {'code': 'NOT_FOUND',
                                  'message': 'You have not rated this joke'}}), 404

    data = request.get_json()

    for axis in ['funniness', 'appropriateness', 'originality']:
        value = data.get(axis) if data else None
        if not isinstance(value, int) or not (1 <= value <= 5):
            msg = f'{axis} must be an integer between 1 and 5'
            return jsonify({'error': {'code': 'INVALID_INPUT',
                                      'message': msg}}), 400

    rating.funniness = data['funniness']
    rating.appropriateness = data['appropriateness']
    rating.originality = data['originality']
    db.session.commit()

    return jsonify({
        'id': rating.id,
        'joke_id': rating.joke_id,
        'user_id': rating.user_id,
        'funniness': rating.funniness,
        'appropriateness': rating.appropriateness,
        'originality': rating.originality,
        'updated_at': rating.updated_at.isoformat() if rating.updated_at else None
    }), 200