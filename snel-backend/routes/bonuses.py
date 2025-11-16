from flask import Blueprint, request, jsonify
from models import Bonus, Employee, db

bonus_bp = Blueprint('bonuses', __name__)


@bonus_bp.route('/', methods=['GET'])
def get_bonuses():
    """Récupérer toutes les primes"""
    try:
        employee_id = request.args.get('employee_id', type=int)
        
        if employee_id:
            bonuses = Bonus.query.filter_by(employee_id=employee_id).all()
        else:
            bonuses = Bonus.query.all()
        
        return jsonify({
            'success': True,
            'count': len(bonuses),
            'data': [b.to_dict() for b in bonuses]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bonus_bp.route('/<int:bonus_id>', methods=['GET'])
def get_bonus(bonus_id):
    """Récupérer une prime par ID"""
    try:
        bonus = Bonus.query.get(bonus_id)
        if not bonus:
            return jsonify({'success': False, 'error': 'Prime non trouvée'}), 404
        
        return jsonify({
            'success': True,
            'data': bonus.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bonus_bp.route('/', methods=['POST'])
def create_bonus():
    """Créer une nouvelle prime"""
    try:
        data = request.get_json()
        
        # Validation
        if 'employee_id' not in data or 'amount' not in data:
            return jsonify({'success': False, 'error': 'employee_id et amount requis'}), 400
        
        # Vérifier que l'employé existe
        employee = Employee.query.get(data['employee_id'])
        if not employee:
            return jsonify({'success': False, 'error': 'Employé non trouvé'}), 404
        
        bonus = Bonus(
            employee_id=data['employee_id'],
            amount=data['amount'],
            description=data.get('description'),
            is_recurring=data.get('is_recurring', False)
        )
        
        db.session.add(bonus)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Prime créée avec succès',
            'data': bonus.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bonus_bp.route('/<int:bonus_id>', methods=['PUT'])
def update_bonus(bonus_id):
    """Mettre à jour une prime"""
    try:
        bonus = Bonus.query.get(bonus_id)
        if not bonus:
            return jsonify({'success': False, 'error': 'Prime non trouvée'}), 404
        
        data = request.get_json()
        
        if 'amount' in data:
            bonus.amount = data['amount']
        if 'description' in data:
            bonus.description = data['description']
        if 'is_recurring' in data:
            bonus.is_recurring = data['is_recurring']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Prime mise à jour avec succès',
            'data': bonus.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bonus_bp.route('/<int:bonus_id>', methods=['DELETE'])
def delete_bonus(bonus_id):
    """Supprimer une prime"""
    try:
        bonus = Bonus.query.get(bonus_id)
        if not bonus:
            return jsonify({'success': False, 'error': 'Prime non trouvée'}), 404
        
        db.session.delete(bonus)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Prime supprimée avec succès'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
