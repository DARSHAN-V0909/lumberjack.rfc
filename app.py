from flask import Flask, render_template
from routes.auth_routes import auth_bp
from routes.material_routes import material_bp

import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(material_bp)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)