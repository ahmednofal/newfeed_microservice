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
@inject
def get_posts(connection: pymysql.connections.Connection):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
        # Correct SQL syntax to select specific fields from user table
            cursor.execute("SELECT * FROM post ")
            posts = cursor.fetchall()  # Fetch the user data
            if posts:  # Check if the user was found
                return jsonify({"data":{"posts": [Post(**{
                    "id": post['id'],  # Add the ID manually
                    "content": post['content'],
                    "author_id": post['author_id'],
                    "created_at": post['created_at']}).dict() for post in posts]}}), 200
            else:
                return jsonify({"error": "post not found"}), 404  # User not found
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        connection.close()


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

# Model for creating a comment
class CommentCreate(BaseModel):
    author_id: int
    post_id: int
    content: str

# Model for updating a comment
class CommentUpdate(BaseModel):
    content: str

# Model for creating a like
class LikeCreate(BaseModel):
    liker_id: int
    post_id: int

# Model for creating a share
class ShareCreate(BaseModel):
    sharer_id: int
    post_id: int

@posts_bp.route('/<int:post_id>/comments', methods=['GET'], strict_slashes=False)
def get_comments(post_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM comment WHERE post_id = %s", (post_id,))
            comments = cursor.fetchall()  # Fetch all comments for the post
            return jsonify(comments), 200
    finally:
        connection.close()

@posts_bp.route('/<int:post_id>/comments/<int:comment_id>', methods=['GET'], strict_slashes=False)
def get_comment(post_id, comment_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM comment WHERE post_id = %s AND id = %s", (post_id, comment_id))
            comment = cursor.fetchone()  # Fetch the specific comment
            if comment:
                return jsonify(comment), 200
            return jsonify({"message": "Comment not found"}), 404
    finally:
        connection.close()

@posts_bp.route('/<int:post_id>/comments', methods=['POST'], strict_slashes=False)
@validate()
def create_comment(body: CommentCreate, post_id: int):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO comment (post_id, author_id, content) VALUES (%s, %s, %s)",
                (post_id, body.author_id, body.content)
            )
            connection.commit()  # Commit the new comment
            return jsonify({"message": "Comment created"}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400
    finally:
        connection.close()

@posts_bp.route('/<int:post_id>/comments/<int:comment_id>', methods=['PUT'], strict_slashes=False)
@validate()
def update_comment(body: CommentUpdate, post_id: int, comment_id: int):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE comment SET content = %s WHERE post_id = %s AND id = %s",
                (body.content, post_id, comment_id)
            )
            connection.commit()  # Commit the update
            if cursor.rowcount > 0:
                return jsonify({"message": "Comment updated"}), 200
            return jsonify({"message": "Comment not found or nothing to update"}), 404
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400
    finally:
        connection.close()

@posts_bp.route('/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'], strict_slashes=False)
def delete_comment(post_id, comment_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM comment WHERE post_id = %s AND id = %s", (post_id, comment_id))
            connection.commit()  # Commit the delete
            if cursor.rowcount > 0:
                return jsonify({"message": "Comment deleted"}), 204
            return jsonify({"message": "Comment not found"}), 404
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400
    finally:
        connection.close()

@posts_bp.route('/<int:post_id>/likes', methods=['GET'], strict_slashes=False)
def get_likes(post_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM like_up WHERE post_id = %s", (post_id,))
            likes = cursor.fetchall()  # Fetch all likes for the post
            return jsonify(likes), 200
    finally:
        connection.close()

@posts_bp.route('/<int:post_id>/likes/<int:like_id>', methods=['GET'], strict_slashes=False)
def get_like(post_id, like_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM like_up WHERE post_id = %s AND liker_id = %s", (post_id, like_id))
            like = cursor.fetchone()  # Fetch the specific like
            if like:
                return jsonify(like), 200
            return jsonify({"message": "Like not found"}), 404
    finally:
        connection.close()

@posts_bp.route('/<int:post_id>/likes', methods=['POST'], strict_slashes=False)
@validate()
def create_like(body: LikeCreate, post_id: int):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO like_up (liker_id, post_id) VALUES (%s, %s)",
                (body.liker_id, post_id)
            )
            connection.commit()  # Commit the new like
            return jsonify({"message": "Like created"}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400
    finally:
        connection.close()

@posts_bp.route('/<int:post_id>/likes/<int:like_id>', methods=['DELETE'], strict_slashes=False)
def delete_like(post_id, like_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM like_up WHERE post_id = %s AND liker_id = %s", (post_id, like_id))
            connection.commit()  # Commit the delete
            if cursor.rowcount > 0:
                return jsonify({"message": "Like deleted"}), 204
            return jsonify({"message": "Like not found"}), 404
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400
    finally:
        connection.close()

@posts_bp.route('/<int:post_id>/shares', methods=['GET'], strict_slashes=False)
def get_shares(post_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM share WHERE post_id = %s", (post_id,))
            shares = cursor.fetchall()  # Fetch all shares for the post
            return jsonify(shares), 200
    finally:
        connection.close()

@posts_bp.route('/<int:post_id>/shares/<int:share_id>', methods=['GET'], strict_slashes=False)
def get_share(post_id, share_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM share WHERE post_id = %s AND id = %s", (post_id, share_id))
            share = cursor.fetchone()  # Fetch the specific share
            if share:
                return jsonify(share), 200
            return jsonify({"message": "Share not found"}), 404
    finally:
        connection.close()

@posts_bp.route('/<int:post_id>/shares', methods=['POST'], strict_slashes=False)
@validate()
def create_share(body: ShareCreate, post_id: int):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO share (sharer_id, post_id) VALUES (%s, %s)",
                (body.sharer_id, post_id)
            )
            connection.commit()  # Commit the new share
            return jsonify({"message": "Share created"}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400
    finally:
        connection.close()

@posts_bp.route('/<int:post_id>/shares/<int:share_id>', methods=['DELETE'], strict_slashes=False)
def delete_share(post_id, share_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM share WHERE post_id = %s AND id = %s", (post_id, share_id))
            connection.commit()  # Commit the delete
            if cursor.rowcount > 0:
                return jsonify({"message": "Share deleted"}), 204
            return jsonify({"message": "Share not found"}), 404
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 400
    finally:
        connection.close()
