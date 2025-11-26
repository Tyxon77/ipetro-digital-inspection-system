from flask import Blueprint, request, jsonify
from ..extensions import supabase_admin
from ..utils.decorators import admin_required, inspector_required

equipment_bp = Blueprint('equipment_bp', __name__, url_prefix="/equipments")

# ============================================================
# CREATE EQUIPMENT
# ============================================================
@equipment_bp.route('', methods=['POST'])
@inspector_required
def create_equipment(current_user):
    data = request.get_json()

    required_fields = ['equipment_tag']
    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    equipment_data = {
        "equipment_tag": data['equipment_tag'],
        "description": data.get('description'),
        "location": data.get('location'),
        "type": data.get('type'),
        "service": data.get('service'),
        "pml_number": data.get('pml_number'),
        "dosh_number": data.get('dosh_number'),
        "is_active": data.get('is_active', True),
        "created_by_user_id": current_user['user_id']
    }

    try:
        response = supabase_admin.table('equipment').insert(equipment_data).execute()
        if response.data:
            return jsonify(response.data[0]), 201
        return jsonify({"error": "Failed to create equipment"}), 500
    except Exception as e:
        print("ERROR in create_equipment:", e)
        return jsonify({"error": str(e)}), 500


# ============================================================
# LIST EQUIPMENTS
# ============================================================
@equipment_bp.route('', methods=['GET'])
@inspector_required
def list_equipments(current_user):
    try:
        status_filter = request.args.get('is_active')
        query = supabase_admin.table('equipment').select('*')

        if status_filter is not None:
            query = query.eq('is_active', status_filter.lower() == 'true')

        response = query.execute()
        return jsonify(response.data or []), 200
    except Exception as e:
        print("ERROR in list_equipments:", e)
        return jsonify({"error": str(e)}), 500


# ============================================================
# GET SINGLE EQUIPMENT
# ============================================================
@equipment_bp.route('/<equipment_id>', methods=['GET'])
@inspector_required
def get_equipment(current_user, equipment_id):
    try:
        response = supabase_admin.table('equipment').select('*').eq('equipment_id', equipment_id).execute()
        if not response.data:
            return jsonify({"error": "Equipment not found"}), 404
        return jsonify(response.data[0]), 200
    except Exception as e:
        print("ERROR in get_equipment:", e)
        return jsonify({"error": str(e)}), 500


# ============================================================
# UPDATE EQUIPMENT
# ============================================================
@equipment_bp.route('/<equipment_id>', methods=['PUT'])
@inspector_required
def update_equipment(current_user, equipment_id):
    data = request.get_json()

    allowed_fields = [
        "equipment_tag",
        "description",
        "location",
        "type",
        "service",
        "pml_number",
        "dosh_number",
        "is_active"
    ]

    update_data = {k: v for k, v in data.items() if k in allowed_fields}

    if not update_data:
        return jsonify({"error": "No valid fields to update"}), 400

    try:
        response = supabase_admin.table('equipment').update(update_data).eq('equipment_id', equipment_id).execute()
        if response.data:
            return jsonify(response.data[0]), 200
        return jsonify({"error": "Failed to update equipment"}), 500
    except Exception as e:
        print("ERROR in update_equipment:", e)
        return jsonify({"error": str(e)}), 500


# ============================================================
# DELETE EQUIPMENT
# ============================================================
@equipment_bp.route('/<equipment_id>', methods=['DELETE'])
@admin_required
def delete_equipment(current_user, equipment_id):
    try:
        response = supabase_admin.table('equipment').delete().eq('equipment_id', equipment_id).execute()
        if response.data:
            return jsonify({"message": "Equipment deleted"}), 200
        return jsonify({"error": "Equipment not found"}), 404
    except Exception as e:
        print("ERROR in delete_equipment:", e)
        return jsonify({"error": str(e)}), 500
