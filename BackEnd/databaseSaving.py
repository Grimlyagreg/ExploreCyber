from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable Flask-SQLAlchemy's modification tracking
db = SQLAlchemy(app)

class UserProgress(db.Model):
    username = db.Column(db.String(255), primary_key=True)
    streak = db.Column(db.Integer, default=0)
    unit = db.Column(db.Integer, default=0)
    lesson = db.Column(db.Integer, default=0)

@app.route('/save-progress', methods=['POST'])
def save_progress():
    data = request.get_json()
    required = ['username', 'streak', 'unit', 'lesson']
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    user_progress = UserProgress.query.get(data['username'])
    if user_progress is None:
        user_progress = UserProgress(username=data['username'])

    user_progress.streak = data['streak']
    user_progress.unit = data['unit']
    user_progress.lesson = data['lesson']

    db.session.add(user_progress)
    db.session.commit()

    return jsonify({"status": "progress saved"})

@app.route('/load-progress/<username>', methods=['GET'])
def load_progress(username):
    user_progress = UserProgress.query.get(username)

    if user_progress:
        return jsonify({
            "streak": user_progress.streak,
            "unit": user_progress.unit,
            "lesson": user_progress.lesson
        })
    else:
        return jsonify({"streak": 0, "unit": 0, "lesson": 0})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
