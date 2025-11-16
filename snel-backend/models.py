from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Employee(db.Model):
    """Modèle pour les employés"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(100))
    salary_base = db.Column(db.Float, nullable=False)
    hire_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    bonuses = db.relationship('Bonus', backref='employee', lazy=True, cascade='all, delete-orphan')
    deductions = db.relationship('Deduction', backref='employee', lazy=True, cascade='all, delete-orphan')
    payroll_items = db.relationship('PayrollItem', backref='employee', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'department': self.department,
            'position': self.position,
            'salary_base': self.salary_base,
            'hire_date': self.hire_date.strftime('%Y-%m-%d') if self.hire_date else None,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Bonus(db.Model):
    """Modèle pour les primes"""
    __tablename__ = 'bonuses'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    bonus_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_recurring = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.name,
            'amount': self.amount,
            'description': self.description,
            'bonus_date': self.bonus_date.strftime('%Y-%m-%d') if self.bonus_date else None,
            'is_recurring': self.is_recurring,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Deduction(db.Model):
    """Modèle pour les retenues"""
    __tablename__ = 'deductions'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    deduction_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_recurring = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.name,
            'amount': self.amount,
            'description': self.description,
            'deduction_date': self.deduction_date.strftime('%Y-%m-%d') if self.deduction_date else None,
            'is_recurring': self.is_recurring,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class PayrollRun(db.Model):
    """Modèle pour les cycles de paie"""
    __tablename__ = 'payroll_runs'
    
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, processed, paid
    total_payroll = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    
    # Relations
    payroll_items = db.relationship('PayrollItem', backref='payroll_run', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'month': self.month,
            'year': self.year,
            'status': self.status,
            'total_payroll': self.total_payroll,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'processed_at': self.processed_at.strftime('%Y-%m-%d %H:%M:%S') if self.processed_at else None,
            'item_count': len(self.payroll_items)
        }


class PayrollItem(db.Model):
    """Modèle pour les éléments de paie"""
    __tablename__ = 'payroll_items'
    
    id = db.Column(db.Integer, primary_key=True)
    payroll_id = db.Column(db.Integer, db.ForeignKey('payroll_runs.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    gross_salary = db.Column(db.Float, nullable=False)
    total_bonuses = db.Column(db.Float, default=0.0)
    total_deductions = db.Column(db.Float, default=0.0)
    net_salary = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'payroll_id': self.payroll_id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.name,
            'gross_salary': self.gross_salary,
            'total_bonuses': self.total_bonuses,
            'total_deductions': self.total_deductions,
            'net_salary': self.net_salary,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
