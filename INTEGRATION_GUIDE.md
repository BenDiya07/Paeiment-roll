# 🚀 GUIDE D'INTÉGRATION BACKEND-FRONTEND

## 📋 État de l'intégration

Le système SNEL Payroll est maintenant intégré avec une API backend Flask. Voici comment démarrer.

---

## 1️⃣ AJOUT DES SCRIPTS AUX PAGES HTML

Pour que l'intégration fonctionne, ajoutez ces scripts à **CHAQUE page** HTML dans le `<head>` ou avant `</body>` :

```html
<!-- Configuration et Client API -->
<script src="assets/js/api-config.js"></script>
<script src="assets/js/api-client.js"></script>

<!-- Auth et Utils (déjà existants) -->
<script src="assets/js/auth.js"></script>
<script src="assets/js/utils.js"></script>

<!-- Gestionnaires spécifiques par page -->
<!-- Pour index.html -->
<script src="assets/js/app.js"></script>

<!-- Pour employees.html -->
<script src="assets/js/employees-manager.js"></script>

<!-- Pour advances.html -->
<script src="assets/js/bonuses-deductions-manager.js"></script>

<!-- Pour payroll.html -->
<script src="assets/js/payroll-manager.js"></script>
```

---

## 2️⃣ DÉMARRER LE BACKEND

### Sur Windows (CMD):

```bash
# Aller dans le répertoire backend
cd f:\CODING\All\Paeiment-roll-1\snel-backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
python app.py
```

Le serveur démarre sur **http://localhost:5000**

---

## 3️⃣ INITIALISER LA BASE DE DONNÉES

### Prérequis:
- MySQL installé et en cours d'exécution
- Utilisateur root ou utilisateur avec droits admin

### Initialiser la DB:

```bash
# Se connecter à MySQL
mysql -u root -p

# Créer la base et l'utilisateur
CREATE DATABASE snel_payroll;
CREATE USER 'snel_user'@'localhost' IDENTIFIED BY 'motdepasse';
GRANT ALL PRIVILEGES ON snel_payroll.* TO 'snel_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Importer le schéma
mysql -u snel_user -p snel_payroll < db/schema.sql

# Importer les données d'exemple
mysql -u snel_user -p snel_payroll < db/seeds.sql
```

---

## 4️⃣ LANCER LE FRONTEND

### Avec Python (recommandé):

```bash
cd f:\CODING\All\Paeiment-roll-1\all\snel-payroll-dashboard
python -m http.server 8000
```

Accédez à **http://localhost:8000**

---

## 5️⃣ VÉRIFIER L'INTÉGRATION

### Checklist:
- ✅ Backend Flask en cours d'exécution (localhost:5000)
- ✅ MySQL en cours d'exécution
- ✅ Frontend en cours d'exécution (localhost:8000)
- ✅ Console du navigateur sans erreurs CORS

### Tester l'API:

```bash
# Dans un terminal, tester un endpoint
curl http://localhost:5000/api/employees

# Doit retourner quelque chose comme:
# {"success":true,"count":0,"data":[...]}
```

---

## 🔧 CONFIGURATION

### Modifier l'URL de l'API

Si vous utilisez un serveur différent, modifiez `api-config.js`:

```javascript
const API_CONFIG = {
    BASE_URL: 'http://localhost:5000/api',  // ← Changer ici
    TIMEOUT: 10000,
    RETRY_ATTEMPTS: 3,
    RETRY_DELAY: 1000
};
```

### Configuration MySQL

Si vous avez d'autres identifiants, modifiez `snel-backend/config.py`:

```python
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://USERNAME:PASSWORD@localhost/snel_payroll"
)
```

---

## 📊 ARCHITECTURE D'INTÉRACTION

```
┌─────────────────────────────────────┐
│    FRONTEND (localhost:8000)        │
│  - index.html                       │
│  - employees.html                   │
│  - payroll.html                     │
│  - advances.html                    │
└──────────────────┬──────────────────┘
                   │ HTTP/JSON
                   │ (api-client.js)
┌──────────────────▼──────────────────┐
│    BACKEND FLASK (localhost:5000)   │
│  - /api/employees                   │
│  - /api/payroll                     │
│  - /api/bonuses                     │
│  - /api/deductions                  │
└──────────────────┬──────────────────┘
                   │ SQL
┌──────────────────▼──────────────────┐
│    MySQL (snel_payroll)             │
│  - employees table                  │
│  - bonuses table                    │
│  - deductions table                 │
│  - payroll_runs table               │
└─────────────────────────────────────┘
```

---

## 🐛 DÉPANNAGE

### "Impossible de se connecter à l'API"
- ✅ Vérifier que Flask est en cours d'exécution
- ✅ Vérifier que le port 5000 est disponible
- ✅ Vérifier les logs du terminal Flask

### "Erreur CORS"
- ✅ Flask-CORS est activé dans app.py
- ✅ Vérifier les en-têtes de réponse

### "Pas de données dans les tables"
- ✅ Vérifier que les données ont été importées: `mysql -u snel_user -p snel_payroll < db/seeds.sql`
- ✅ Vérifier la connexion DB: Aller sur http://localhost:5000 (doit voir "SNEL Payroll API")

### "Erreur 401 Unauthorized"
- ✅ Authentification requise (non implémentée pour l'instant)
- ✅ Ajouter un header Authorization si nécessaire

---

## 📚 FICHIERS CLÉS

### Frontend
- `api-config.js` - Configuration des endpoints API
- `api-client.js` - Client HTTP pour appels API
- `app.js` - Logique du tableau de bord
- `employees-manager.js` - Gestion des employés
- `bonuses-deductions-manager.js` - Gestion primes/retenues
- `payroll-manager.js` - Gestion de la paie
- `auth.js` - Gestion de l'authentification
- `utils.js` - Utilitaires

### Backend
- `app.py` - Application Flask principale
- `models.py` - Modèles SQLAlchemy
- `config.py` - Configuration
- `routes/` - Endpoints API

---

## ✨ FONCTIONNALITÉS INTÉGRÉES

### ✅ Employés
- [x] Lister tous les employés
- [x] Créer un employé
- [x] Modifier un employé
- [x] Supprimer un employé
- [x] Rechercher un employé

### ✅ Paie
- [x] Générer un cycle de paie
- [x] Voir les détails d'un cycle
- [x] Exporter en CSV
- [x] Marquer comme payé

### ✅ Primes & Retenues
- [x] Ajouter une prime
- [x] Ajouter une retenue
- [x] Modifier/Supprimer
- [x] Filtrer par employé

### ✅ Dashboard
- [x] Statistiques en temps réel
- [x] Graphiques interactifs
- [x] Génération de paie
- [x] Export CSV

---

## 🎯 PROCHAINES ÉTAPES

1. ✅ Tester l'intégration complète
2. ✅ Implémenter l'authentification avec JWT
3. ✅ Ajouter les validations côté client
4. ✅ Gestion des rôles (Admin/RH/Comptable)
5. ✅ Génération PDF des bulletins
6. ✅ Audit logs
7. ✅ Tests unitaires

---

**Bon développement! 🚀**
