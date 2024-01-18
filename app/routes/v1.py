from flask import Blueprint
from app.controller.event import event
v1 = Blueprint('v1', __name__)

v1.register_blueprint(event ,url_prefix='/event')
