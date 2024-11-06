from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Meme
from scraper import get_memes
from dotenv import load_dotenv
import os



app = Flask(__name__)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Create the database tables
with app.app_context():
    db.create_all()

def retrieve_memes():
    return Meme.query.all()  # Fetch all memes from the database


@app.route('/save_memes', methods=['POST'])
def save_memes():
    try:
        memes = get_memes()  # Call the get_memes function to save memes in the database
        return jsonify({'message': f'{len(memes)} memes saved successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to render the saved memes page
@app.route('/saved_memes')
def saved_memes_page():
    return render_template('saved_memes.html')
    
@app.route('/memes', methods=['GET'])
def fetch_memes():
    memes = Meme.query.all()  # Retrieve all saved memes from the database
    return jsonify([{
        'title': meme.title,
        'url': meme.url,
        'permalink': meme.permalink
    } for meme in memes])



@app.route('/api/memes', methods=['GET'])
def get_memes_api():
    memes = get_memes()
    return jsonify(memes)

@app.route('/')
def index():
    memes = get_memes()
    return render_template('index.html', memes=memes)

if __name__ == '__main__':
    app.run(debug=True)







