from datetime import datetime
from typing import Optional
from flask import Blueprint, jsonify, request
from flask_injector import inject
from flask_pydantic import validate
from pydantic import BaseModel, EmailStr, Field

from api.deps import get_db_connection
import pymysql

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')
class Post(BaseModel):
    id: Optional[int]  # Optional since it will be auto-generated
    content: str
    author_id: int
    created_at: datetime

@posts_bp.route('/', methods=['GET'], strict_slashes=False)
def get_posts():
    return jsonify({"message": "List of post"})

@posts_bp.route('/<int:post_id>', methods=['GET'], strict_slashes=False)
def get_post(post_id):
    connection: pymysql.connections.Connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Correct SQL syntax to select specific fields from user table
            cursor.execute("SELECT * FROM post WHERE id = %s", (post_id,))
            post = cursor.fetchone()  # Fetch the post data
            if post:  # Check if the post was found
                return jsonify({"data":{"post": Post(**{
                    "id": post['id'],  # Add the ID manually
                    "author_id": post['author_id'],
                    "content": post['content'],
                    "created_at": post['created_at']}).dict()}}), 200
            else:
                return jsonify({"error": "Post not found"}), 404  # User not found
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400  # Return a meaningful error message
    finally:
        connection.close()  # Ensure the connection is closed

class PostCreate(BaseModel):
    content: str
    author_id: int

class PostUpdate(BaseModel):
    content: str

@posts_bp.route('/', methods=['POST'], strict_slashes=False)
@validate()
def create_post(body: PostCreate):
    connection: pymysql.connections.Connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO post (content, author_id) VALUES (%s, %s)", 
                           (body.content, body.author_id))
            connection.commit()
            return jsonify({"message": f"Created Post {cursor.lastrowid}"}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400  # Return a meaningful error message


@posts_bp.route('/<int:post_id>', methods=['PUT'], strict_slashes=False)
@validate()
def update_post(body:PostUpdate, post_id: int):
    connection = get_db_connection()
    try:
        # Validate incoming JSON data using the Post model
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE post SET content = %s WHERE id = %s",
                (body.content, post_id)
            )
            # Commit the changes and handle potential exceptions
            connection.commit()
            if cursor.rowcount == 0:
                cursor.execute("SELECT * from post WHERE id = %s", (post_id))

                post = cursor.fetchone()  # Fetch the post data
                if post:
                    return jsonify({"message": "Post not updated, no new data"}), 404
                else:
                    return jsonify({"message": f"no post with id {post_id}"}), 404
            return jsonify({"message": "Post update successfully"}), 200

    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        connection.close()

@posts_bp.route('/<int:post_id>', methods=['DELETE'], strict_slashes=False)
def delete_post(post_id: int):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM post WHERE id = %s", (post_id,))
            connection.commit()
            if cursor.rowcount > 0:
                return jsonify({"message": "Post deleted successfully"}), 200
            else:
                return jsonify({"message": "Post not deleted, nothing to delete"}), 404
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400
    finally:
        connection.close()

@posts_bp.route('/<int:post_id>/comments', methods=['GET'], strict_slashes=False)
def get_comments(post_id):
    return jsonify({"message": f"Post {post_id} Comments"})

@posts_bp.route('/<int:post_id>/comments/<int:comment_id>', methods=['GET'], strict_slashes=False)
def get_comment(post_id, comment_id):
    return jsonify({"message": f"Post {post_id}, Comment {comment_id}"})

@posts_bp.route('/<int:post_id>/likes', methods=['GET'], strict_slashes=False)
def get_likes(post_id):
    return jsonify({"message": f"Post {post_id} Likes"})

@posts_bp.route('/<int:post_id>/likes/<int:like_id>', methods=['GET'], strict_slashes=False)
def get_like(post_id, like_id):
    return jsonify({"message": f"Post {post_id}, Like {like_id}"})

@posts_bp.route('/<int:post_id>/shares', methods=['GET'], strict_slashes=False)
def get_shares(post_id):
    return jsonify({"message": f"Post {post_id} Shares"})

@posts_bp.route('/<int:post_id>/shares/<int:share_id>', methods=['GET'], strict_slashes=False)
def get_share(post_id, share_id):
    return jsonify({"message": f"Post {post_id}, Share {share_id}"})
