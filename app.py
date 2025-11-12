from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inspection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db first
db = SQLAlchemy(app)

# Import models and initialize them with db
from models.equipment import Equipment
from models.turnaround import Turnaround

# Import routes after db is initialized
from routes.equipment_routes import equipment_bp
from routes.turnaround_routes import turnaround_bp

app.register_blueprint(equipment_bp)
app.register_blueprint(turnaround_bp)

# Initialize models with db
Equipment.db = db
Turnaround.db = db

@app.route('/')
def home():
    return 'API is working!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Server running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)