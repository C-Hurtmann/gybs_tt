from flask import Blueprint, jsonify, request, abort
from app.models import User, db
from app.serializers import UserListSchema, UserCreateUpdateSchema, UserSchema
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


users_bp = Blueprint('users', __name__)

user_schema = UserSchema()
user_create_update_schema = UserCreateUpdateSchema()

@users_bp.route('/', methods=['GET'])
def get_users():
    user_list = UserListSchema(many=True).dump(User.query.all())
    return jsonify({'users': user_list})


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_schema.dump(User.query.get_or_404(user_id))
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
    except Exception as e:
        return jsonify({'error': str(e)}), 422
    user_data = user_create_update_schema.dump(user)
    return jsonify({'user_created': user_data}), 201


@users_bp.route('/<int:user_id>/', methods=['PUT'])
def update_user(user_id):
    json_data = request.get_json()
    try:
        user_data = user_create_update_schema.load(json_data, partial=True)
    except Exception as e:
        return jsonify({'errors': str(e)}), 422
    user = User.query.get_or_404(user_id)
    for key, value in user_data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify({'user_updated': user_data})


@users_bp.route('/<int:user_id>/', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    user_data = user_schema.dump(user)
    return jsonify({'user_deleted': user_data})