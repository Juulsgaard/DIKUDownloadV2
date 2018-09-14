from flask import Flask

from server.endpoints.authentication import bp as auth
from server.endpoints.calendar import bp as cal


def application(environ, start_response):
    status = '200 OK'
    output = b'Hello World!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]


def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth)
    app.register_blueprint(cal)

    @app.route("/test", methods=["POST"])
    def test():
        return "success"

    return app


# app = create_app()
# if __name__ == "__main__":
#     app.run()
