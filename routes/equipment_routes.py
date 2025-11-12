from flask import Blueprint, request, jsonify
from models.equipment import Equipment, db

equipment_bp = Blueprint('equipment', __name__)

# GET ALL EQUIPMENT
@equipment_bp.route('/equipment', methods=['GET'])
def get_all_equipment():
    all_equipment = Equipment.query.all()
    output = []
    for equipment in all_equipment:
        equipment_data = {
            'equipment_id': equipment.equipment_id,
            'equipment_tag': equipment.equipment_tag,
            'description': equipment.description,
            'location': equipment.location,
            'type': equipment.type,
            'service': equipment.service,
            'pml_number': equipment.pml_number,
            'dosh_number': equipment.dosh_number,
            'is_active': equipment.is_active,
            'created_by_user_id': equipment.created_by_user_id,
            'created_at': equipment.created_at.isoformat() if equipment.created_at else None
        }
        output.append(equipment_data)
    return jsonify({'equipment': output})

# GET SINGLE EQUIPMENT
@equipment_bp.route('/equipment/<int:equipment_id>', methods=['GET'])
def get_one_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    equipment_data = {
        'equipment_id': equipment.equipment_id,
        'equipment_tag': equipment.equipment_tag,
        'description': equipment.description,
        'location': equipment.location,
        'type': equipment.type,
        'service': equipment.service,
        'pml_number': equipment.pml_number,
        'dosh_number': equipment.dosh_number,
        'is_active': equipment.is_active,
        'created_by_user_id': equipment.created_by_user_id,
        'created_at': equipment.created_at.isoformat() if equipment.created_at else None
    }
    return jsonify({'equipment': equipment_data})

# CREATE NEW EQUIPMENT
@equipment_bp.route('/equipment', methods=['POST'])
def create_equipment():
    data = request.get_json()
    
    # Check if equipment tag already exists
    existing_equipment = Equipment.query.filter_by(equipment_tag=data['equipment_tag']).first()
    if existing_equipment:
        return jsonify({'error': 'Equipment tag already exists!'}), 400
    
    new_equipment = Equipment(
        equipment_tag=data['equipment_tag'],
        description=data['description'],
        location=data.get('location'),
        type=data.get('type'),
        service=data.get('service'),
        pml_number=data.get('pml_number'),
        dosh_number=data.get('dosh_number'),
        created_by_user_id=data['created_by_user_id']
    )
    
    db.session.add(new_equipment)
    db.session.commit()
    
    return jsonify({'message': 'Equipment created successfully!', 'equipment_id': new_equipment.equipment_id}), 201

# UPDATE EQUIPMENT
@equipment_bp.route('/equipment/<int:equipment_id>', methods=['PUT'])
def update_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    data = request.get_json()
    
    # Update fields if provided
    if 'equipment_tag' in data:
        equipment.equipment_tag = data['equipment_tag']
    if 'description' in data:
        equipment.description = data['description']
    if 'location' in data:
        equipment.location = data['location']
    if 'type' in data:
        equipment.type = data['type']
    if 'service' in data:
        equipment.service = data['service']
    if 'pml_number' in data:
        equipment.pml_number = data['pml_number']
    if 'dosh_number' in data:
        equipment.dosh_number = data['dosh_number']
    if 'is_active' in data:
        equipment.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({'message': 'Equipment updated successfully!'})

# DELETE EQUIPMENT
@equipment_bp.route('/equipment/<int:equipment_id>', methods=['DELETE'])
def delete_equipment(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
    db.session.delete(equipment)
    db.session.commit()
    
    return jsonify({'message': 'Equipment deleted successfully!'})

# GET ACTIVE EQUIPMENT ONLY
@equipment_bp.route('/equipment/active', methods=['GET'])
def get_active_equipment():
    active_equipment = Equipment.query.filter_by(is_active=True).all()
    output = []
    for equipment in active_equipment:
        equipment_data = {
            'equipment_id': equipment.equipment_id,
            'equipment_tag': equipment.equipment_tag,
            'description': equipment.description,
            'location': equipment.location,
            'type': equipment.type
        }
        output.append(equipment_data)
    return jsonify({'active_equipment': output})