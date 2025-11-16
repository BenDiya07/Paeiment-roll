from flask import Blueprint, jsonify, request
from models import Employee, Bonus, Deduction, db

employee_bp = Blueprint('employees', __name__)


@employee_bp.route('/', methods=['GET'])
def get_employees():
    """Récupérer tous les employés"""
    try:
        employees = Employee.query.all()
        return jsonify({
            'success': True,
            'count': len(employees),
            'data': [e.to_dict() for e in employees]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@employee_bp.route('/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Récupérer un employé par ID"""
    try:
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({'success': False, 'error': 'Employé non trouvé'}), 404
        
        return jsonify({
            'success': True,
            'data': employee.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@employee_bp.route('/', methods=['POST'])
def create_employee():
    """Créer un nouvel employé"""
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['name', 'email', 'department', 'salary_base']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Champs requis manquants'}), 400
        
        # Vérifier l'email unique
        if Employee.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'error': 'Email déjà utilisé'}), 400
        
        employee = Employee(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            department=data['department'],
            position=data.get('position'),
            salary_base=data['salary_base'],
            is_active=data.get('is_active', True)
        )
        
        db.session.add(employee)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Employé créé avec succès',
            'data': employee.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@employee_bp.route('/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Mettre à jour un employé"""
    try:
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({'success': False, 'error': 'Employé non trouvé'}), 404
        
        data = request.get_json()
        
        # Mettre à jour les champs
        if 'name' in data:
            employee.name = data['name']
        if 'email' in data:
            # Vérifier l'unicité de l'email
            if data['email'] != employee.email:
                if Employee.query.filter_by(email=data['email']).first():
                    return jsonify({'success': False, 'error': 'Email déjà utilisé'}), 400
            employee.email = data['email']
        if 'phone' in data:
            employee.phone = data['phone']
        if 'department' in data:
            employee.department = data['department']
        if 'position' in data:
            employee.position = data['position']
        if 'salary_base' in data:
            employee.salary_base = data['salary_base']
        if 'is_active' in data:
            employee.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Employé mis à jour avec succès',
            'data': employee.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@employee_bp.route('/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Supprimer un employé"""
    try:
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({'success': False, 'error': 'Employé non trouvé'}), 404
        
        db.session.delete(employee)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Employé supprimé avec succès'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@employee_bp.route('/<int:employee_id>/summary', methods=['GET'])
def get_employee_summary(employee_id):
    """Récupérer un résumé complet d'un employé avec primes et retenues"""
    try:
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({'success': False, 'error': 'Employé non trouvé'}), 404
        
        bonuses = Bonus.query.filter_by(employee_id=employee_id).all()
        deductions = Deduction.query.filter_by(employee_id=employee_id).all()
        
        total_bonuses = sum(b.amount for b in bonuses)
        total_deductions = sum(d.amount for d in deductions)
        net_salary = employee.salary_base + total_bonuses - total_deductions
        
        return jsonify({
            'success': True,
            'data': {
                **employee.to_dict(),
                'bonuses': [b.to_dict() for b in bonuses],
                'deductions': [d.to_dict() for d in deductions],
                'total_bonuses': total_bonuses,
                'total_deductions': total_deductions,
                'net_salary': net_salary
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
