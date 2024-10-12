from flask import Flask
from flask_injector import FlaskInjector
from injector import Binder
import injector
import pymysql

from api.deps import MySQLModule

from api.main import api_base_bp

app = Flask("newsfeed_app")
app.register_blueprint(api_base_bp)


# Flask-Injector setup
# def configure(binder: Binder):
#     # Bind MySQLModule to create a new connection for each request
#     binder.bind(pymysql.connections.Connection, to=MySQLModule.data_base_connection)

# FlaskInjector(app=app, modules=[configure])

if __name__ == '__main__':
    for rule in app.url_map.iter_rules():
        print(f"Endpoint: {rule.endpoint}, URL: {rule}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
