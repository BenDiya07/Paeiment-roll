# SNEL Payroll Dashboard - Backend API

Une API Flask complète pour gérer les paies, employés, primes et retenues.

## 🚀 Installation

### Prérequis
- Python 3.8+
- MySQL 5.7+
- pip

### Étapes d'installation

1. **Cloner le projet**
```bash
cd snel-backend
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Configurer la base de données**
   - Copier `.env.example` en `.env`
   - Modifier les paramètres de connexion MySQL
   - Exécuter: `mysql -u root -p < db/schema.sql`

6. **Lancer l'application**
```bash
python app.py
```

L'API sera disponible à `http://localhost:5000`

---

## 📚 Documentation API

### Base URL
```
http://localhost:5000/api
```

### Authentification
Aucune authentification requise (à ajouter selon vos besoins)

---

## 👥 Endpoints - Employés

### Récupérer tous les employés
```
GET /api/employees
```
**Réponse:**
```json
{
  "success": true,
  "count": 5,
  "data": [
    {
      "id": 1,
      "name": "Jean Dupont",
      "email": "jean@example.com",
      "department": "IT",
      "salary_base": 50000,
      "is_active": true
    }
  ]
}
```

### Récupérer un employé
```
GET /api/employees/<id>
```

### Créer un employé
```
POST /api/employees
Content-Type: application/json

{
  "name": "Marie Martin",
  "email": "marie@example.com",
  "phone": "+33612345678",
  "department": "HR",
  "position": "Manager RH",
  "salary_base": 45000,
  "is_active": true
}
```

### Mettre à jour un employé
```
PUT /api/employees/<id>
Content-Type: application/json

{
  "salary_base": 52000,
  "position": "Senior IT"
}
```

### Supprimer un employé
```
DELETE /api/employees/<id>
```

### Récupérer le résumé d'un employé
```
GET /api/employees/<id>/summary
```
Retourne: employé + primes + retenues + salaire net

---

## 💰 Endpoints - Paie

### Générer un cycle de paie
```
POST /api/payroll/generate
Content-Type: application/json

{
  "month": "November",
  "year": 2025
}
```
**Réponse:**
```json
{
  "success": true,
  "message": "Cycle de paie November/2025 généré avec succès",
  "data": {
    "payroll_id": 1,
    "month": "November",
    "year": 2025,
    "total_payroll": 250000,
    "employee_count": 5,
    "items": [
      {
        "employee_name": "Jean Dupont",
        "gross_salary": 50000,
        "total_bonuses": 5000,
        "total_deductions": 10000,
        "net_salary": 45000
      }
    ]
  }
}
```

### Récupérer tous les cycles de paie
```
GET /api/payroll/runs?page=1&per_page=10
```

### Récupérer un cycle de paie
```
GET /api/payroll/runs/<id>
```

### Exporter un cycle de paie
```
GET /api/payroll/runs/<id>/export
```
Retourne: JSON avec tous les détails de paie

### Marquer comme payé
```
PUT /api/payroll/runs/<id>/mark-paid
```

---

## 🎁 Endpoints - Primes

### Récupérer toutes les primes
```
GET /api/bonuses
GET /api/bonuses?employee_id=1
```

### Créer une prime
```
POST /api/bonuses
Content-Type: application/json

{
  "employee_id": 1,
  "amount": 5000,
  "description": "Prime de performance",
  "is_recurring": false
}
```

### Mettre à jour une prime
```
PUT /api/bonuses/<id>
Content-Type: application/json

{
  "amount": 6000,
  "description": "Prime de performance révisée"
}
```

### Supprimer une prime
```
DELETE /api/bonuses/<id>
```

---

## 📉 Endpoints - Retenues

### Récupérer toutes les retenues
```
GET /api/deductions
GET /api/deductions?employee_id=1
```

### Créer une retenue
```
POST /api/deductions
Content-Type: application/json

{
  "employee_id": 1,
  "amount": 1000,
  "description": "Assurance maladie",
  "is_recurring": true
}
```

### Mettre à jour une retenue
```
PUT /api/deductions/<id>
```

### Supprimer une retenue
```
DELETE /api/deductions/<id>
```

---

## 🗄️ Structure de la Base de Données

### Table: employees
```sql
- id (PK)
- name VARCHAR(100)
- email VARCHAR(100) UNIQUE
- phone VARCHAR(20)
- department VARCHAR(50)
- position VARCHAR(100)
- salary_base FLOAT
- hire_date DATETIME
- is_active BOOLEAN
- created_at DATETIME
```

### Table: bonuses
```sql
- id (PK)
- employee_id (FK)
- amount FLOAT
- description VARCHAR(200)
- bonus_date DATETIME
- is_recurring BOOLEAN
- created_at DATETIME
```

### Table: deductions
```sql
- id (PK)
- employee_id (FK)
- amount FLOAT
- description VARCHAR(200)
- deduction_date DATETIME
- is_recurring BOOLEAN
- created_at DATETIME
```

### Table: payroll_runs
```sql
- id (PK)
- month VARCHAR(20)
- year INTEGER
- status VARCHAR(20)
- total_payroll FLOAT
- created_at DATETIME
- processed_at DATETIME
```

### Table: payroll_items
```sql
- id (PK)
- payroll_id (FK)
- employee_id (FK)
- gross_salary FLOAT
- total_bonuses FLOAT
- total_deductions FLOAT
- net_salary FLOAT
- created_at DATETIME
```

---

## 🧪 Testing

Utiliser Postman ou curl pour tester les endpoints:

```bash
# Tester la santé
curl http://localhost:5000/health

# Récupérer les employés
curl http://localhost:5000/api/employees

# Créer un employé
curl -X POST http://localhost:5000/api/employees \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","department":"IT","salary_base":50000}'
```

---

## 📝 Notes

- Les salaires nets ne peuvent pas être négatifs
- Les emails doivent être uniques
- Les employés inactifs ne sont pas inclus dans les cycles de paie
- Les primes et retenues récurrentes peuvent être marquées automatiquement

---

## 🔒 Sécurité (À implémenter)

- [ ] Authentification JWT
- [ ] Validation des rôles (Admin, Manager, Employee)
- [ ] Rate limiting
- [ ] Validation des données stricte
- [ ] Logs d'audit
- [ ] Chiffrement des données sensibles

---

## 📧 Support

Pour toute question, contactez l'équipe de développement.
