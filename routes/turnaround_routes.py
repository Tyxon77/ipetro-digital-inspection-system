from flask import Blueprint, request, jsonify
from ..extensions import supabase_admin
from ..utils.decorators import admin_required, inspector_required

turnaround_bp = Blueprint('turnaround_bp', __name__, url_prefix="/turnarounds")

# ============================================================
# CREATE TURNAROUND
# ============================================================
@turnaround_bp.route('', methods=['POST'])
@inspector_required
def create_turnaround(current_user):
    data = request.get_json()

    required_fields = ['turnaround_name', 'year', 'start_date', 'end_date']
    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    turnaround_data = {
        "turnaround_name": data['turnaround_name'],
        "year": data['year'],
        "start_date": data['start_date'],
        "end_date": data['end_date']
    }

    try:
        response = supabase_admin.table('turnaround').insert(turnaround_data).execute()
        if response.data:
            return jsonify(response.data[0]), 201
        return jsonify({"error": "Failed to create turnaround"}), 500
    except Exception as e:
        print("ERROR in create_turnaround:", e)
        return jsonify({"error": str(e)}), 500


# ============================================================
# LIST TURNAROUNDS
# ============================================================
@turnaround_bp.route('', methods=['GET'])
@inspector_required
def list_turnarounds(current_user):
    try:
        query = supabase_admin.table('turnaround').select('*')
        response = query.execute()
        return jsonify(response.data or []), 200
    except Exception as e:
        print("ERROR in list_turnarounds:", e)
        return jsonify({"error": str(e)}), 500


# ============================================================
# GET SINGLE TURNAROUND
# ============================================================
@turnaround_bp.route('/<turnaround_id>', methods=['GET'])
@inspector_required
def get_turnaround(current_user, turnaround_id):
    try:
        response = supabase_admin.table('turnaround').select('*').eq('turnaround_id', turnaround_id).execute()
        if not response.data:
            return jsonify({"error": "Turnaround not found"}), 404
        return jsonify(response.data[0]), 200
    except Exception as e:
        print("ERROR in get_turnaround:", e)
        return jsonify({"error": str(e)}), 500


# ============================================================
# UPDATE TURNAROUND
# ============================================================
@turnaround_bp.route('/<turnaround_id>', methods=['PUT'])
@inspector_required
def update_turnaround(current_user, turnaround_id):
    data = request.get_json()

    allowed_fields = ["turnaround_name", "year", "start_date", "end_date"]

    update_data = {k: v for k, v in data.items() if k in allowed_fields}

    if not update_data:
        return jsonify({"error": "No valid fields to update"}), 400

    try:
        response = supabase_admin.table('turnaround').update(update_data).eq('turnaround_id', turnaround_id).execute()
        if response.data:
            return jsonify(response.data[0]), 200
        return jsonify({"error": "Failed to update turnaround"}), 500
    except Exception as e:
        print("ERROR in update_turnaround:", e)
        return jsonify({"error": str(e)}), 500


# ============================================================
# DELETE TURNAROUND
# ============================================================
@turnaround_bp.route('/<turnaround_id>', methods=['DELETE'])
@admin_required
def delete_turnaround(current_user, turnaround_id):
    try:
        response = supabase_admin.table('turnaround').delete().eq('turnaround_id', turnaround_id).execute()
        if response.data:
            return jsonify({"message": "Turnaround deleted"}), 200
        return jsonify({"error": "Turnaround not found"}), 404
    except Exception as e:
        print("ERROR in delete_turnaround:", e)
        return jsonify({"error": str(e)}), 500
