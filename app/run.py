from flask import Flask
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from app.database import db
from app.controllers.restaurant_controller import restaurant_bp
from app.controllers.reservation_controller import reservation_bp
from app.controllers.user_controller import user_bp


app = Flask(__name__)

# Configuración de la clave secreta para JWT
app.config["JWT_SECRET_KEY"] = "tu_clave_secreta_aqui"
# Configuración de la URL de la documentación OpenAPI
# Ruta para servir Swagger UI
SWAGGER_URL = "/api/docs"
# Ruta de tu archivo OpenAPI/Swagger
API_URL = "/static/swagger.json"


# Inicializa el Blueprint de Swagger UI
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Examen Final Web III - API"}
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///restaurant.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(restaurant_bp, url_prefix="/api")
app.register_blueprint(reservation_bp, url_prefix="/api")
app.register_blueprint(user_bp, url_prefix="/api")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)