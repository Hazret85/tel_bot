from datetime import datetime
from flask import Flask, jsonify, request
from models import BotLog, session

app = Flask(__name__)

@app.route('/logs', methods=['GET'])
def get_logs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = session.query(BotLog)

    if start_date and end_date:
        start_date = datetime.fromisoformat(start_date)
        end_date = datetime.fromisoformat(end_date)
        query = query.filter(BotLog.timestamp.between(start_date, end_date))

    logs = query.order_by(BotLog.timestamp.desc()).offset((page - 1) * per_page).limit(per_page).all()

    return jsonify([{
        'id': log.id,
        'user_id': log.user_id,
        'username': log.username,
        'command': log.command,
        'message': log.message,
        'response': log.response,
        'timestamp': log.timestamp.isoformat()
    } for log in logs])

@app.route('/logs/<int:user_id>', methods=['GET'])
def get_user_logs(user_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    logs = session.query(BotLog).filter(BotLog.user_id == user_id).order_by(BotLog.timestamp.desc()).offset((page - 1) * per_page).limit(per_page).all()

    return jsonify([{
        'id': log.id,
        'user_id': log.user_id,
        'username': log.username,
        'command': log.command,
        'message': log.message,
        'response': log.response,
        'timestamp': log.timestamp.isoformat()
    } for log in logs])
