from flask import Blueprint, abort, jsonify, request
from app.models import User, db
from app.serializers import UserListSchema, UserCreateUpdateSchema, UserSchema
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError


users_bp = Blueprint('users', __name__)

user_schema = UserSchema()
user_create_update_schema = UserCreateUpdateSchema()


def get_user_or_404(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        abort(404, description="User not found")
    return user


@users_bp.route('/', methods=['GET'])
def get_users():
    user_list = UserListSchema(many=True).dump(User.query.all())
    return jsonify({'users': user_list})


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_schema.dump(get_user_or_404(user_id))
    return jsonify({'user': user})


@users_bp.route('/', methods=['POST'])
def create_user():
    json_data = request.get_json()
    try:
        user = user_create_update_schema.load(json_data)
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 422
    except ValidationError as e:
        return jsonify({'error': e.messages}), 422
    user_data = user_schema.dump(user)
    return jsonify({'user_created': user_data}), 201


@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    json_data = request.get_json()
    user = get_user_or_404(user_id)
    try:
        user_create_update_schema.load(json_data, instance=user, partial=True)
        db.session.commit()
        user = db.session.get(User, user_id)
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 422
    except ValidationError as e:
        return jsonify({'error': e.messages}), 422
    return jsonify({'user_updated': user_schema.dump(user)})


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user := db.session.get(User, user_id):
        db.session.delete(user)
        db.session.commit()
        user_data = user_schema.dump(user)
        return jsonify({'user_deleted': user_data}), 200
    return jsonify({'user_deleted': {}}), 204
