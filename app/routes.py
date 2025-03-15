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
    """
    Get all users
    ---
    tags:
      - users
    responses:
      200:
        description: A list of all users
        schema:
          type: object
          properties:
            users:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: User ID
                  name:
                    type: string
                    description: User's name
                  email:
                    type: string
                    description: User's email
                  created_at:
                    type: string
                    description: Creation timestamp in ISO format
    """
    user_list = UserListSchema(many=True).dump(User.query.all())
    return jsonify({'users': user_list})


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a specific user by ID
    ---
    tags:
      - users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The user ID
    responses:
      200:
        description: User found
        schema:
          type: object
          properties:
            user:
              type: object
              properties:
                id:
                  type: integer
                  description: User ID
                name:
                  type: string
                  description: User's name
                email:
                  type: string
                  description: User's email
                created_at:
                  type: string
                  description: Creation timestamp in ISO format
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    user = user_schema.dump(get_user_or_404(user_id))
    return jsonify({'user': user})


@users_bp.route('/', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - users
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
          properties:
            name:
              type: string
              description: User's name
              example: John Doe
            email:
              type: string
              description: User's email address
              example: john@example.com
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            user_created:
              type: object
              properties:
                id:
                  type: integer
                  description: User ID
                name:
                  type: string
                  description: User's name
                email:
                  type: string
                  description: User's email
                created_at:
                  type: string
                  description: Creation timestamp in ISO format
      422:
        description: Validation error or duplicate email
        schema:
          type: object
          properties:
            error:
              type: object
              description: Error messages
    """
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
    """
    Update an existing user
    ---
    tags:
      - users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The user ID to update
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: User's name
              example: John Doe
            email:
              type: string
              description: User's email address
              example: john@example.com
    responses:
      200:
        description: User updated successfully
        schema:
          type: object
          properties:
            user_updated:
              type: object
              properties:
                id:
                  type: integer
                  description: User ID
                name:
                  type: string
                  description: User's name
                email:
                  type: string
                  description: User's email
                created_at:
                  type: string
                  description: Creation timestamp in ISO format
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      422:
        description: Validation error or duplicate email
        schema:
          type: object
          properties:
            error:
              type: object
              description: Error messages
    """
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
    """
    Delete a user
    ---
    tags:
      - users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The user ID to delete
    responses:
      200:
        description: User successfully deleted
        schema:
          type: object
          properties:
            user_deleted:
              type: object
              properties:
                id:
                  type: integer
                  description: User ID
                name:
                  type: string
                  description: User's name
                email:
                  type: string
                  description: User's email
                created_at:
                  type: string
                  description: Creation timestamp in ISO format
      204:
        description: User not found (no content)
        schema:
          type: object
          properties:
            user_deleted:
              type: object
              description: Empty object
    """
    if user := db.session.get(User, user_id):
        db.session.delete(user)
        db.session.commit()
        user_data = user_schema.dump(user)
        return jsonify({'user_deleted': user_data}), 200
    return jsonify({'user_deleted': {}}), 204
