from flask import Flask
from game import game_blueprint
from web import web_blueprint
import config

app = Flask(__name__)
app.register_blueprint(game_blueprint)
app.register_blueprint(web_blueprint)

@app.route('/')
def root():
    return """

Welcome to Annaki!
<br>
<h2>Pages</h2>
<ul>
    <li><a href='/web/'>Web Root</a></li>
</ul>
<h2>Games</h2>
<ul>
    <li><a href='/game/ac'>Animal Crossing: Population Growing (Nintendo GameCube)</a></li>
    <li><a href='/game/accf'>Animal Crossing: Let's go to the City (Nintendo Wii)</a></li>
    <li><a href='/game/acnl'>Animal Crossing: New Leaf (Nintendo 3DS)</a></li>
    <li><a href='/game/acnh'>Animal Crossing: New Horizons (Nintendo Switch)</a></li>
    <li><a href='/game/acpc'>Animal Crossing: Pocket Camp (iOS/Android)</a></li>
</ul>
"""

if __name__ == '__main__':
    app.run(config.HOST, config.PORT, config.DEBUG)