from flask import Blueprint

game_blueprint = Blueprint('game', __name__)

from . import animal_crossing