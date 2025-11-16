# Paeiment-roll

## Gérer MySQL avec XAMPP et VS Code (méthode simple et propre)

Voici la méthode la plus simple et propre pour gérer ta base MySQL avec XAMPP en utilisant VS Code, sans passer par phpMyAdmin, et sans erreur `pma`.

### ✅ Objectif

Tu vas pouvoir :

- Te connecter à MySQL depuis VS Code
- Créer ta base `snel_paiement`
- Créer tes tables
- Écrire tes scripts SQL directement dans VS Code
- Éviter les erreurs de phpMyAdmin

---

### 1) Installer l’extension MySQL dans VS Code

Dans VS Code :

1. Clique sur **Extensions** (icône carré)
2. Cherche : **SQLTools**
3. Installe :

	 - **SQLTools**
	 - **SQLTools MySQL/MariaDB Driver**

👉 C'est officiel, stable et parfait pour XAMPP.

---

### 2) Vérifier que MySQL tourne dans XAMPP

Dans XAMPP :

- **Démarre MySQL**
- Port par défaut → `3306`

---

### 3) Créer une connexion MySQL dans VS Code

Dans VS Code :

1. Ouvre la palette : **Ctrl + Shift + P**
2. Recherche : **SQLTools: Add new connection**
3. Choisis : **MySQL / MariaDB**

Renseigne :

```
Host: 127.0.0.1
Port: 3306
User: root
Password: (laisser vide)
Database: (laisser vide pour maintenant)
```

Clique **Test Connection** → **Should be Success** ✔️ Ensuite **Save Connection**.

---

### 4) Créer la base de données depuis VS Code

Dans la barre gauche → SQLTools → Connections
Clique ta connexion → Clique **Open Query**

Colle :

```sql
CREATE DATABASE IF NOT EXISTS snel_paiement
	DEFAULT CHARACTER SET utf8mb4
	DEFAULT COLLATE utf8mb4_general_ci;
```

Puis clique **Run**.

Ta base est créée 🎉.

---

### 5) Se connecter à la base `snel_paiement`

Dans SQLTools :

- Clique ta connexion →
- **Switch Database** → choisis `snel_paiement`.

---

### 6) Créer toutes les tables depuis VS Code

Exemple pour commencer :

```sql
CREATE TABLE users (
		id INT AUTO_INCREMENT PRIMARY KEY,
		full_name VARCHAR(100),
		email VARCHAR(100) UNIQUE,
		role ENUM('admin','payroll_manager','hr') DEFAULT 'hr',
		password_hash VARCHAR(255),
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Puis clique **Run**.

Tu peux créer toutes les autres tables facilement.

---

### 7) Avantages par rapport à phpMyAdmin

| VS Code + SQLTools    | phpMyAdmin         |
| --------------------- | ------------------ |
| Aucun bug "pma user"  | erreurs fréquentes |
| Très rapide           | lent               |
| Autocomplétion SQL    | limité             |
| Historique SQL        | non                |
| Tout dans le même IDE | switching constant |

C'est la méthode des professionnels.

---

Si tu veux, je peux aussi :

- ajouter un fichier `MYSQL_XAMPP_VSCODE.md` dans le repo avec ces instructions (pratique pour l'équipe),
- ou automatiser la création de la base/tables via un script SQL prêt à importer depuis `snel-backend/db/`.

Dites-moi ce que tu préfères.