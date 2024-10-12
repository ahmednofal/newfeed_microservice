from flask import Blueprint, jsonify, request
from flask_injector import inject
from flask_pydantic import validate
from pydantic import BaseModel, EmailStr
from typing import Optional

from api.deps import get_db_connection
import pymysql

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['GET'])
def get_users():
    return jsonify({"message": "List of users"})

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({"message": f"User {user_id}"})


# Pydantic model for user
class UserCreate(BaseModel):
    handle: str
    email: EmailStr
    password_hash: str


# # RESTful API to create a user
@users_bp.route('/', methods=['POST'])
@validate()
def create_user(body: UserCreate):
    connection: pymysql.connections.Connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (handle, email, password_hash) VALUES (%s, %s, %s)", 
                           (body.handle, body.email, body.password_hash))
            connection.commit()
            body.id = cursor.lastrowid  # Get the last inserted ID
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400  # Return a meaningful error message