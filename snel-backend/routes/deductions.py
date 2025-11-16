from flask import Blueprint, request, jsonify
from models import Deduction, Employee, db

deduction_bp = Blueprint('deductions', __name__)


@deduction_bp.route('/', methods=['GET'])
def get_deductions():
    """Récupérer toutes les retenues"""
    try:
        employee_id = request.args.get('employee_id', type=int)
        
        if employee_id:
            deductions = Deduction.query.filter_by(employee_id=employee_id).all()
        else:
            deductions = Deduction.query.all()
        
        return jsonify({
            'success': True,
            'count': len(deductions),
            'data': [d.to_dict() for d in deductions]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@deduction_bp.route('/<int:deduction_id>', methods=['GET'])
def get_deduction(deduction_id):
    """Récupérer une retenue par ID"""
    try:
        deduction = Deduction.query.get(deduction_id)
        if not deduction:
            return jsonify({'success': False, 'error': 'Retenue non trouvée'}), 404
        
        return jsonify({
            'success': True,
            'data': deduction.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@deduction_bp.route('/', methods=['POST'])
def create_deduction():
    """Créer une nouvelle retenue"""
    try:
        data = request.get_json()
        
        # Validation
        if 'employee_id' not in data or 'amount' not in data:
            return jsonify({'success': False, 'error': 'employee_id et amount requis'}), 400
        
        # Vérifier que l'employé existe
        employee = Employee.query.get(data['employee_id'])
        if not employee:
            return jsonify({'success': False, 'error': 'Employé non trouvé'}), 404
        
        deduction = Deduction(
            employee_id=data['employee_id'],
            amount=data['amount'],
            description=data.get('description'),
            is_recurring=data.get('is_recurring', False)
        )
        
        db.session.add(deduction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Retenue créée avec succès',
            'data': deduction.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@deduction_bp.route('/<int:deduction_id>', methods=['PUT'])
def update_deduction(deduction_id):
    """Mettre à jour une retenue"""
    try:
        deduction = Deduction.query.get(deduction_id)
        if not deduction:
            return jsonify({'success': False, 'error': 'Retenue non trouvée'}), 404
        
        data = request.get_json()
        
        if 'amount' in data:
            deduction.amount = data['amount']
        if 'description' in data:
            deduction.description = data['description']
        if 'is_recurring' in data:
            deduction.is_recurring = data['is_recurring']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Retenue mise à jour avec succès',
            'data': deduction.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@deduction_bp.route('/<int:deduction_id>', methods=['DELETE'])
def delete_deduction(deduction_id):
    """Supprimer une retenue"""
    try:
        deduction = Deduction.query.get(deduction_id)
        if not deduction:
            return jsonify({'success': False, 'error': 'Retenue non trouvée'}), 404
        
        db.session.delete(deduction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Retenue supprimée avec succès'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
