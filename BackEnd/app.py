
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from models import db, User, DataRecord, UserProgress
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400
    
    user = User(username=username, email=email)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        "msg": "User created successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token), 200

@app.route('/data', methods=['POST'])
@jwt_required()
def add_data():
 
    current_user_id = get_jwt_identity()
    key = request.form.get('id')
    value = request.form.get('value')

    if not key:
        return jsonify({"msg": "Key is required"}), 400
    
    record = DataRecord.query.filter_by(
        user_id=current_user_id,
        data_key=key
    ).first()
    
    if record:
        record.data_value = value
        msg = "Data updated successfully"
    else:
        record = DataRecord(
            user_id=current_user_id,
            data_key=key,
            data_value=value
        )
        db.session.add(record)
        msg = "Data added successfully"
    
    db.session.commit()
    
    return jsonify({
        "msg": msg,
        "data": {
            "key": record.data_key,
            "value": record.data_value
        }
    }), 200

@app.route('/data/<key>', methods=['GET'])
@jwt_required()
def get_data(key):
    current_user_id = get_jwt_identity()
    
    record = DataRecord.query.filter_by(
        user_id=current_user_id,
        data_key=key
    ).first()
    
    if not record:
        return jsonify({"msg": "Data not found"}), 404
    
    return jsonify({
        "key": record.data_key,
        "value": record.data_value
    }), 200

@app.route('/data', methods=['GET'])
@jwt_required()
def get_all_data():
    current_user_id = get_jwt_identity()
    
    records = DataRecord.query.filter_by(user_id=current_user_id).all()
    
    return jsonify({
        "data": [{
            "key": r.data_key,
            "value": r.data_value
        } for r in records]
    }), 200

@app.route('/save-progress', methods=['POST'])
@jwt_required()
def save_progress():
    current_user_id = get_jwt_identity()
    streak = request.form.get('streak')
    unit = request.form.get('unit')
    lesson = request.form.get('lesson')

    if not all([streak, unit, lesson]):
        return jsonify({"error": "Missing fields"}), 400

    user_progress = UserProgress.query.filter_by(user_id=current_user_id).first()
    if user_progress is None:
        user_progress = UserProgress(user_id=current_user_id)

    user_progress.streak = streak
    user_progress.unit = unit
    user_progress.lesson = lesson

    db.session.add(user_progress)
    db.session.commit()

    return jsonify({"status": "progress saved"}), 200

@app.route('/load-progress', methods=['GET'])
@jwt_required()
def load_progress():
    current_user_id = get_jwt_identity()
    user_progress = UserProgress.query.filter_by(user_id=current_user_id).first()

    if user_progress:
        return jsonify({
            "streak": user_progress.streak,
            "unit": user_progress.unit,
            "lesson": user_progress.lesson
        }), 200
    else:
        return jsonify({"streak": 0, "unit": 0, "lesson": 0}), 200


@app.route('/')
def MainHost():
    return send_file("../FrontEnd/login.html")

@app.route('/<path:path>')
def serveFile(path):
    return send_from_directory("../FrontEnd", path)

if __name__ == '__main__':
    app.run(debug=True)