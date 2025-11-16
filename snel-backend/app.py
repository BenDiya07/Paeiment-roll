import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from models import db
from routes.employees import employee_bp
from routes.payroll import payroll_bp
from routes.bonuses import bonus_bp
from routes.deductions import deduction_bp


def create_app(config_name=None):
    """Factory function pour créer l'application Flask"""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")
    
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config["development"]))
    
    # Initialiser l'extension SQLAlchemy
    db.init_app(app)
    
    # Activer CORS
    CORS(app)
    
    # Enregistrer les blueprints
    app.register_blueprint(employee_bp, url_prefix='/api/employees')
    app.register_blueprint(payroll_bp, url_prefix='/api/payroll')
    app.register_blueprint(bonus_bp, url_prefix='/api/bonuses')
    app.register_blueprint(deduction_bp, url_prefix='/api/deductions')
    
    # Routes de base
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({
            'message': 'SNEL Payroll API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'employees': '/api/employees',
                'payroll': '/api/payroll',
                'bonuses': '/api/bonuses',
                'deductions': '/api/deductions'
            }
        }), 200
    
    @app.route('/health', methods=['GET'])
    def health():
        """Endpoint de santé"""
        return jsonify({
            'status': 'healthy',
            'timestamp': __import__('datetime').datetime.utcnow().isoformat()
        }), 200
    
    # Gestion des erreurs
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Route non trouvée',
            'status': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Erreur serveur interne',
            'status': 500
        }), 500
    
    # Contexte pour créer les tables
    with app.app_context():
        db.create_all()
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
