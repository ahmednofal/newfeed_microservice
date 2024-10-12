from flask import Flask

from api.main import api_base_bp

app = Flask("newsfeed_app")
app.register_blueprint(api_base_bp)

# # Pydantic model for user
# class User(BaseModel):
#     id: Optional[int]
#     username: str

# # RESTful API to create a user
# @app.route('/api/users', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     try:
#         user = User(username=data['username'])
#     except ValidationError as e:
#         return jsonify(e.errors()), 400

#     connection = get_db_connection()
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("INSERT INTO users (username) VALUES (%s)", (user.username,))
#             connection.commit()
#             user.id = cursor.lastrowid  # Get the last inserted ID
#     finally:
#         connection.close()

#     return jsonify({'id': user.id, 'username': user.username}), 201

# # RESTful API to fetch all users
# @app.route('/api/users', methods=['GET'])
# def get_users():
#     connection = get_db_connection()
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM users")
#             users = cursor.fetchall()
#     finally:
#         connection.close()

#     return jsonify(users), 200

# # RESTful API to fetch a user by ID
# @app.route('/api/users/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     connection = get_db_connection()
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
#             user = cursor.fetchone()
#     finally:
#         connection.close()

#     if user:
#         return jsonify(user), 200
#     return jsonify({'error': 'User not found'}), 404

# # RESTful API to delete a user by ID
# @app.route('/api/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     connection = get_db_connection()
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
#             if cursor.rowcount == 0:
#                 return jsonify({'error': 'User not found'}), 404
#             connection.commit()
#     finally:
#         connection.close()

#     return jsonify({'message': 'User deleted'}), 200

if __name__ == '__main__':
    for rule in app.url_map.iter_rules():
        print(f"Endpoint: {rule.endpoint}, URL: {rule}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
