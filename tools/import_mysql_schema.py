#!/usr/bin/env python3
"""
import_mysql_schema.py
---------------------
Script pour créer la base `snel_paiement` et importer schema + seeds SQL.
Supporte options CLI et variables d'environnement.

Usage:
    python tools\import_mysql_schema.py [--host HOST] [--port PORT] [--user USER] [--password PWD] [--database DB]

Exemples:
    python tools\import_mysql_schema.py --host 127.0.0.1 --port 3307 --user root --database snel_paiement
    set MYSQL_HOST=127.0.0.1 && set MYSQL_PORT=3307 && python tools\import_mysql_schema.py
"""

import os
import argparse
import mysql.connector
from mysql.connector import Error


def run_sql_file(cursor, filepath):
    """Exécute toutes les requêtes SQL d'un fichier en les séparant par ';'."""
    if not os.path.isfile(filepath):
        print(f"⚠️  Fichier non trouvé: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # On split par ';' simple, ça suffit pour des dumps propres sans procedures complexes
    statements = content.split(';')
    for stmt in statements:
        stmt = stmt.strip()
        if not stmt:
            continue
        try:
            cursor.execute(stmt)
        except Error as e:
            print(f"Erreur SQL: {e}\nStatement: {stmt[:200]}...")


def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    default_schema = os.path.join(repo_root, 'snel-backend', 'db', 'schema.sql')
    default_seeds = os.path.join(repo_root, 'snel-backend', 'db', 'seeds.sql')

    parser = argparse.ArgumentParser(description='Importer schema et seeds MySQL pour SNEL Payroll')
    parser.add_argument('--host', default=os.getenv('MYSQL_HOST', '127.0.0.1'))
    parser.add_argument('--port', type=int, default=int(os.getenv('MYSQL_PORT', 3307)))
    parser.add_argument('--user', default=os.getenv('MYSQL_USER', 'root'))
    parser.add_argument('--password', default=os.getenv('MYSQL_PASSWORD', ''))
    parser.add_argument('--database', default=os.getenv('MYSQL_DB', 'snel_paiement'))
    parser.add_argument('--schema', default=os.getenv('SCHEMA_PATH', default_schema))
    parser.add_argument('--seeds', default=os.getenv('SEEDS_PATH', default_seeds))

    args = parser.parse_args()

    try:
        print(f"Connexion à MySQL (host={args.host} port={args.port} user={args.user})...")
        conn = mysql.connector.connect(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password,
            autocommit=True,
        )
        cursor = conn.cursor()

        # Créer la base si nécessaire
        print(f"Création de la base '{args.database}' si nécessaire...")
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {args.database} DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_general_ci;"
        )

        # Se connecter à la DB
        conn.database = args.database

        # Importer le schema
        print(f"📥 Import du schema depuis: {args.schema}")
        run_sql_file(cursor, args.schema)

        # Importer les seeds
        print(f"📥 Import des seeds depuis: {args.seeds}")
        run_sql_file(cursor, args.seeds)

        print('🎉 Import terminé avec succès !')

    except Error as e:
        print(f"❌ Erreur MySQL: {e}")
        raise SystemExit(1)
    finally:
        try:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
                print('🔒 Connexion MySQL fermée.')
        except Exception:
            pass


if __name__ == '__main__':
    main()
