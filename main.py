from flask import Flask, jsonify
from extensions import db, jwt
from auth import auth_bp
from users import user_bp
def create_app():

    app = Flask(__name__)

    app.config.from_prefixed_env()
    
    #initialize app
    db.init_app(app)
    jwt.init_app(app)
    #register blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')

    # Jwt error handling

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "Message" : "The token has expired",
                    "error" : "token_expired"
                }
            ),401
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ), 401
        )

    return app