from flask import Flask

from .endpoints.authentication import bp as auth
from .endpoints.calendar import bp as cal

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
