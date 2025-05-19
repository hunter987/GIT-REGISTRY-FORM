def create_app():
    app = Flask(__name__)
    app.secret_key = get_secret_key()
    configure_app(app)
    register_blueprints(app)
    return app


def get_secret_key():
    return os.getenv("FLASK_SECRET_KEY", "dev")


def configure_app(app):
    env = os.getenv("ENV", "development").lower()
    is_production = env == "production"

    app.config['DEBUG'] = not is_production

    if is_production:
        configure_production(app)
    else:
        configure_development(app)


def configure_production(app):
    configure_ssl(app)
    configure_database(app, use_prod_db=True)


def configure_development(app):
    configure_database(app, use_prod_db=False)


def configure_ssl(app):
    if os.getenv("USE_SSL", "false").lower() == "true":
        from flask_sslify import SSLify
        SSLify(app)


def configure_database(app, use_prod_db):
    use_external_db = os.getenv("USE_DB", "false").lower() == "true"
    if use_prod_db and use_external_db:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' if use_prod_db else 'sqlite:///dev.db'


def register_blueprints(app):
    if os.getenv("USE_BLUEPRINTS", "false").lower() == "true":
        from .routes import main_bp
        app.register_blueprint(main_bp)

    if os.getenv("ENABLE_API", "false").lower() == "true":
        from .api import api_bp
        app.register_blueprint(api_bp, url_prefix="/api")