from flask import Flask
from pydantic import BaseModel
from json import JSONEncoder
from flask_injector import FlaskInjector
from injector import Binder
import injector
import pymysql

from api.deps import MySQLModule
from api.main import api_base_bp
from core.db import apply_ddl_if_needed

# class PydanticEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, BaseModel):
#             return obj.dict()  # Automatically convert Pydantic models to dict
#         return super().default(obj)

app = Flask("newsfeed_app")
app.register_blueprint(api_base_bp)
# app.json_encoder = PydanticEncoder


# Flask-Injector setup
# def configure(binder: Binder):
#     # Bind MySQLModule to create a new connection for each request
#     binder.bind(pymysql.connections.Connection, to=MySQLModule.data_base_connection)

# FlaskInjector(app=app, modules=[configure])

if __name__ == '__main__':
    for rule in app.url_map.iter_rules():
        print(f"Endpoint: {rule.endpoint}, URL: {rule}")
    
    apply_ddl_if_needed()
    app.run(host='0.0.0.0', port=5000, debug=True)
