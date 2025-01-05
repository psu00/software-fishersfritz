from flask import Flask
from catch import catch_blueprint

app = Flask(__name__)
app.register_blueprint(catch_blueprint, url_prefix='/api')

@app.route('/')
def home():
    return "Welcome to FisherFritz API!"

if __name__ == '__main__':
    app.run(debug=True)