from flask import Blueprint, request, jsonify
from models.turnaround import Turnaround, db

turnaround_bp = Blueprint('turnaround', __name__)

# GET ALL TURNAROUNDS
@turnaround_bp.route('/turnaround', methods=['GET'])
def get_all_turnarounds():
    all_turnarounds = Turnaround.query.all()
    output = []
    for ta in all_turnarounds:
        ta_data = {
            'turnaround_id': ta.turnaround_id,
            'turnaround_name': ta.turnaround_name,
            'year': ta.year,
            'start_date': ta.start_date.isoformat(),
            'end_date': ta.end_date.isoformat(),
            'created_at': ta.created_at.isoformat() if ta.created_at else None
        }
        output.append(ta_data)
    return jsonify({'turnarounds': output})

# GET SINGLE TURNAROUND
@turnaround_bp.route('/turnaround/<int:turnaround_id>', methods=['GET'])
def get_one_turnaround(turnaround_id):
    turnaround = Turnaround.query.get_or_404(turnaround_id)
    turnaround_data = {
        'turnaround_id': turnaround.turnaround_id,
        'turnaround_name': turnaround.turnaround_name,
        'year': turnaround.year,
        'start_date': turnaround.start_date.isoformat(),
        'end_date': turnaround.end_date.isoformat(),
        'created_at': turnaround.created_at.isoformat() if turnaround.created_at else None
    }
    return jsonify({'turnaround': turnaround_data})

# CREATE NEW TURNAROUND
@turnaround_bp.route('/turnaround', methods=['POST'])
def create_turnaround():
    data = request.get_json()
    
    new_turnaround = Turnaround(
        turnaround_name=data['turnaround_name'],
        year=data['year'],
        start_date=data['start_date'],
        end_date=data['end_date']
    )
    
    db.session.add(new_turnaround)
    db.session.commit()
    
    return jsonify({'message': 'Turnaround created successfully!', 'turnaround_id': new_turnaround.turnaround_id}), 201

# UPDATE TURNAROUND
@turnaround_bp.route('/turnaround/<int:turnaround_id>', methods=['PUT'])
def update_turnaround(turnaround_id):
    turnaround = Turnaround.query.get_or_404(turnaround_id)
    data = request.get_json()
    
    if 'turnaround_name' in data:
        turnaround.turnaround_name = data['turnaround_name']
    if 'year' in data:
        turnaround.year = data['year']
    if 'start_date' in data:
        turnaround.start_date = data['start_date']
    if 'end_date' in data:
        turnaround.end_date = data['end_date']
    
    db.session.commit()
    
    return jsonify({'message': 'Turnaround updated successfully!'})

# DELETE TURNAROUND
@turnaround_bp.route('/turnaround/<int:turnaround_id>', methods=['DELETE'])
def delete_turnaround(turnaround_id):
    turnaround = Turnaround.query.get_or_404(turnaround_id)
    db.session.delete(turnaround)
    db.session.commit()
    
    return jsonify({'message': 'Turnaround deleted successfully!'})

# GET TURNAROUNDS BY YEAR
@turnaround_bp.route('/turnaround/year/<int:year>', methods=['GET'])
def get_turnarounds_by_year(year):
    turnarounds = Turnaround.query.filter_by(year=year).all()
    output = []
    for ta in turnarounds:
        ta_data = {
            'turnaround_id': ta.turnaround_id,
            'turnaround_name': ta.turnaround_name,
            'start_date': ta.start_date.isoformat(),
            'end_date': ta.end_date.isoformat()
        }
        output.append(ta_data)
    return jsonify({'turnarounds': output})