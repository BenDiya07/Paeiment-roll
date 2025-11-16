from flask import Blueprint, request, jsonify
from datetime import datetime
from models import Employee, Bonus, Deduction, PayrollRun, PayrollItem, db

payroll_bp = Blueprint('payroll', __name__)


@payroll_bp.route('/generate', methods=['POST'])
def generate_payroll():
    """Générer un cycle de paie"""
    try:
        data = request.get_json()
        month = data.get('month')
        year = data.get('year')
        
        if not month or not year:
            return jsonify({'success': False, 'error': 'Mois et année requis'}), 400
        
        # Vérifier si un run existe déjà pour ce mois/année
        existing = PayrollRun.query.filter_by(month=month, year=year).first()
        if existing:
            return jsonify({'success': False, 'error': f'Un cycle de paie existe déjà pour {month}/{year}'}), 400
        
        # Créer un nouveau cycle de paie
        payroll_run = PayrollRun(month=month, year=year, status='processed')
        db.session.add(payroll_run)
        db.session.flush()  # Pour obtenir l'ID sans commit
        
        employees = Employee.query.filter_by(is_active=True).all()
        results = []
        total_payroll = 0.0
        
        for emp in employees:
            # Calculer les primes et retenues
            bonuses = Bonus.query.filter_by(employee_id=emp.id).all()
            deductions = Deduction.query.filter_by(employee_id=emp.id).all()
            
            total_bonuses = sum(b.amount for b in bonuses)
            total_deductions = sum(d.amount for d in deductions)
            net_salary = emp.salary_base + total_bonuses - total_deductions
            
            # Créer un élément de paie
            payroll_item = PayrollItem(
                payroll_id=payroll_run.id,
                employee_id=emp.id,
                gross_salary=emp.salary_base,
                total_bonuses=total_bonuses,
                total_deductions=total_deductions,
                net_salary=max(net_salary, 0)  # Pas de salaire négatif
            )
            db.session.add(payroll_item)
            
            total_payroll += max(net_salary, 0)
            
            results.append({
                'employee_id': emp.id,
                'employee_name': emp.name,
                'department': emp.department,
                'gross_salary': emp.salary_base,
                'total_bonuses': total_bonuses,
                'total_deductions': total_deductions,
                'net_salary': max(net_salary, 0)
            })
        
        payroll_run.total_payroll = total_payroll
        payroll_run.processed_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Cycle de paie {month}/{year} généré avec succès',
            'data': {
                'payroll_id': payroll_run.id,
                'month': month,
                'year': year,
                'total_payroll': total_payroll,
                'employee_count': len(results),
                'items': results
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@payroll_bp.route('/runs', methods=['GET'])
def get_payroll_runs():
    """Récupérer tous les cycles de paie"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        runs = PayrollRun.query.order_by(PayrollRun.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'total': runs.total,
            'pages': runs.pages,
            'current_page': page,
            'data': [r.to_dict() for r in runs.items]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@payroll_bp.route('/runs/<int:run_id>', methods=['GET'])
def get_payroll_run(run_id):
    """Récupérer un cycle de paie spécifique"""
    try:
        payroll_run = PayrollRun.query.get(run_id)
        if not payroll_run:
            return jsonify({'success': False, 'error': 'Cycle de paie non trouvé'}), 404
        
        return jsonify({
            'success': True,
            'data': {
                **payroll_run.to_dict(),
                'items': [item.to_dict() for item in payroll_run.payroll_items]
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@payroll_bp.route('/runs/<int:run_id>/export', methods=['GET'])
def export_payroll(run_id):
    """Exporter un cycle de paie (format JSON)"""
    try:
        payroll_run = PayrollRun.query.get(run_id)
        if not payroll_run:
            return jsonify({'success': False, 'error': 'Cycle de paie non trouvé'}), 404
        
        export_data = {
            'payroll_info': payroll_run.to_dict(),
            'items': [item.to_dict() for item in payroll_run.payroll_items],
            'summary': {
                'total_gross': sum(item.gross_salary for item in payroll_run.payroll_items),
                'total_bonuses': sum(item.total_bonuses for item in payroll_run.payroll_items),
                'total_deductions': sum(item.total_deductions for item in payroll_run.payroll_items),
                'total_net': payroll_run.total_payroll
            }
        }
        
        return jsonify({
            'success': True,
            'data': export_data
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@payroll_bp.route('/runs/<int:run_id>/mark-paid', methods=['PUT'])
def mark_payroll_paid(run_id):
    """Marquer un cycle de paie comme payé"""
    try:
        payroll_run = PayrollRun.query.get(run_id)
        if not payroll_run:
            return jsonify({'success': False, 'error': 'Cycle de paie non trouvé'}), 404
        
        payroll_run.status = 'paid'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cycle de paie marqué comme payé',
            'data': payroll_run.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
