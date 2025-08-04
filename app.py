from flask import Flask
from flasgger import Swagger
from config import Config
from models.db import db
from routes.url_routes import url_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
swagger = Swagger(app, template_file='swagger.yml')

app.register_blueprint(url_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
