# Desarrollado por:
# - Fuentes Rangel, Jesús Eduardo
# - López Barajas, Andrés Esaú
import os
from flask import Flask
from database import init_db
from decouple import config

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        # Secret key used to hash sessions for the authentication flow
        SECRET_KEY=config('SECRET_KEY')
    )

    import database

    database.init_app(app)

    import auth, project

    # Register both the auth and project controller
    app.register_blueprint(auth.bp)
    app.register_blueprint(project.bp)

    # Set the default home route to the index of the project controller
    app.add_url_rule('/', endpoint="project.index")

    return app


if __name__ == "__main__":
    create_app().run()
