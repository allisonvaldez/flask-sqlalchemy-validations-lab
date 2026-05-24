from flask import Flask, make_response
from flask_migrate import Migrate
from models import db, Author, Post

# Create Flask app and provide all configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create migrate so the Flask db runs
migrate = Migrate(app, db)

# Create a db instance of the Flask app 
db.init_app(app)

# Create index route
@app.route('/')
def index():
    return 'Validations lab'

if __name__ == '__main__':
    app.run(port=5555, debug=True)