from flask import Flask

from .server.endpoints.authentication import bp as auth
from .server.endpoints.calendar import bp as cal


def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth)
    app.register_blueprint(cal)

    @app.route("/test", methods=["POST"])
    def test():
        return "success"

    return app


app = create_app()
if __name__ == "__main__":
    app.run()