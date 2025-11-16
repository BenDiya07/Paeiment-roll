# MYSQL_XAMPP_VSCODE.md

## Gérer MySQL avec XAMPP et VS Code (Méthode Simple et Propre)

Ce guide explique comment gérer ta base MySQL avec **XAMPP** directement depuis **VS Code**, de manière rapide et sans les erreurs classiques de phpMyAdmin (comme `pma@localhost`).

---

## 🎯 **Objectifs**

Avec cette méthode, tu vas pouvoir :

* Te connecter à MySQL depuis VS Code
* Créer la base `snel_paiement`
* Créer toutes tes tables
* Exécuter tes scripts SQL via VS Code
* Éviter les erreurs phpMyAdmin
* Gagner en productivité (vitesse + autocomplétion)

---

## 1️⃣ Installer MySQL dans VS Code

Dans VS Code :

1. Ouvre l’onglet **Extensions**
2. Installe :

   * **SQLTools**
   * **SQLTools MySQL/MariaDB Driver**

Ces extensions sont officielles, rapides et parfaitement compatibles avec XAMPP.

---

## 2️⃣ Vérifier que MySQL tourne dans XAMPP

Dans XAMPP -> démarre :

✔️ **MySQL (port 3306)**
✔️ Rien d’autre à configurer

---

## 3️⃣ Créer une connexion MySQL dans VS Code

Dans VS Code :

1. `Ctrl + Shift + P`
2. Tape : **SQLTools: Add new connection**
3. Choisir : **MySQL / MariaDB**

Configurer :

```
Host: 127.0.0.1
Port: 3306
User: root
Password: (laisser vide)
Database: (laisser vide pour commencer)
```

Puis :

* **Test Connection** → Success ✔️
* **Save Connection**

---

## 4️⃣ Créer la base de données `snel_paiement`

Depuis SQLTools → **Open Query**

Exécute :

```sql
CREATE DATABASE IF NOT EXISTS snel_paiement
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_general_ci;
```

La base est créée 🎉

---

## 5️⃣ Se connecter à la base

Dans SQLTools :

* Clique ta connexion
* **Switch Database** → `snel_paiement`

Maintenant tu peux créer/modifier les tables.

---

## 6️⃣ Créer les tables depuis VS Code

Exemple avec la table `users` :

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

Puis **Run**.

Tu peux ensuite ajouter toutes les autres tables.

---

## 7️⃣ Pourquoi utiliser VS Code au lieu de phpMyAdmin ?

| VS Code + SQLTools   | phpMyAdmin             |
| -------------------- | ---------------------- |
| Ultra rapide         | Lent                   |
| Pas de bugs `pma`    | Beaucoup d'erreurs     |
| Autocomplétion SQL   | Très limité            |
| Historique SQL       | Non                    |
| Tout dans l’IDE      | Changements de fenêtre |
| Pro (usage pro)      | Dépannage / léger      |

---

## Propositions d'améliorations (optionnel)

* Ajouter ce fichier `docs/MYSQL_XAMPP_VSCODE.md` au repo (déjà fait).
* Ajouter un script d'import automatique qui exécute `snel-backend/db/schema.sql` et `snel-backend/db/seeds.sql` dans la base `snel_paiement`.
* Documenter la commande Windows (cmd) pour importer le SQL automatiquement si souhaité.

---

Si tu veux, je peux aussi :

* Fournir le script d'import (fichier `.bat` ou script Python) pour Windows/XAMPP.
* Ajouter une section rapide dans le `README.md` qui pointe vers ce fichier `docs/MYSQL_XAMPP_VSCODE.md`.

Dis-moi ce que tu préfères.
