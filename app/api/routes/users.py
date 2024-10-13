from datetime import datetime
from typing import Optional
from flask import Blueprint, jsonify, request
from flask_injector import inject
from flask_pydantic import validate
from pydantic import BaseModel, EmailStr, Field

from api.deps import get_db_connection
import pymysql

users_bp = Blueprint('users', __name__, url_prefix='/users')
class User(BaseModel):
    id: Optional[int]
    handle: str
    email: EmailStr
    created_at: datetime


@users_bp.route('/', methods=['GET'], strict_slashes=False)
def get_users():
    connection: pymysql.connections.Connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Correct SQL syntax to select specific fields from user table
            cursor.execute("SELECT * FROM user ")
            users = cursor.fetchall()  # Fetch the user data
            if users:  # Check if the user was found
                return jsonify({"data":{"users": [User(**{
                    "id": user['id'],  # Add the ID manually
                    "handle": user['handle'],
                    "email": user['email'],
                    "created_at": user['created_at']}).dict() for user in users]}}), 200
            else:
                return jsonify({"error": "User not found"}), 404  # User not found
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400  # Return a meaningful error message
    finally:
        connection.close()  # Ensure the connection is closed

@users_bp.route('/<int:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    connection: pymysql.connections.Connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Correct SQL syntax to select specific fields from user table
            cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
            user = cursor.fetchone()  # Fetch the user data
            if user:  # Check if the user was found
                return jsonify({"data":{"user": User(**{
                    "id": user['id'],  # Add the ID manually
                    "handle": user['handle'],
                    "email": user['email'],
                    "created_at": user['created_at']}).dict()}}), 200
            else:
                return jsonify({"error": "User not found"}), 404  # User not found
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400  # Return a meaningful error message
    finally:
        connection.close()  # Ensure the connection is closed


# Pydantic model for user
class UserCreate(BaseModel):
    handle: str
    email: EmailStr
    password_hash: str


# # RESTful API to create a user
@users_bp.route('/', methods=['POST'], strict_slashes=False)
@validate()
def create_user(body: UserCreate):
    connection: pymysql.connections.Connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO user (handle, email, password_hash) VALUES (%s, %s, %s)", 
                           (body.handle, body.email, body.password_hash))
            connection.commit()
            return jsonify({"message": f"Created User {cursor.lastrowid}"}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400  # Return a meaningful error message