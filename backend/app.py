from flask import Flask
from flask_cors import CORS
from catch import catch_blueprint
app = Flask(__name__)
CORS(app)  # CORS aktivieren
# Blueprint registrieren
app.register_blueprint(catch_blueprint)
@app.route('/')
def home():
    return "Welcome to FisherFritz API!"
if __name__ == '__main__':
    app.run(debug=True)