#!/usr/bin/env python3
"""
SNEL Payroll - Script de démarrage
Démarre le système complet : Backend Flask + Frontend HTTP
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

# Couleurs pour le terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    print(f"""
{Colors.CYAN}╔════════════════════════════════════════════════════╗
║   {Colors.BOLD}SNEL PAYROLL - DÉMARRAGE DU SYSTÈME{Colors.CYAN}            ║
╚════════════════════════════════════════════════════╝{Colors.ENDC}
    """)

def check_python():
    """Vérifier que Python est disponible"""
    if sys.version_info < (3, 6):
        print(f"{Colors.RED}❌ Erreur: Python 3.6+ requis{Colors.ENDC}")
        sys.exit(1)
    print(f"{Colors.GREEN}✅ Python {sys.version.split()[0]} détecté{Colors.ENDC}")

def check_mysql():
    """Vérifier que MySQL est disponible"""
    try:
        import subprocess
        result = subprocess.run(
            ['mysql', '-u', 'snel_user', '-pmotdepasse', '-e', 'SELECT 1'],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ MySQL est accessible{Colors.ENDC}")
            return True
    except:
        pass
    
    print(f"{Colors.YELLOW}⚠️  MySQL n'est pas accessible{Colors.ENDC}")
    print(f"   Assurez-vous que le serveur MySQL est en cours d'exécution")
    return False

def start_backend():
    """Démarrer le serveur Flask"""
    backend_dir = Path(__file__).parent / 'snel-backend'
    
    if not backend_dir.exists():
        print(f"{Colors.RED}❌ Erreur: Répertoire {backend_dir} non trouvé{Colors.ENDC}")
        return None
    
    print(f"\n{Colors.BLUE}Démarrage du backend Flask...{Colors.ENDC}")
    print(f"   Répertoire: {backend_dir}")
    
    try:
        # Créer un environnement virtuel s'il n'existe pas
        venv_dir = backend_dir / 'venv'
        if not venv_dir.exists():
            print(f"{Colors.YELLOW}   Création de l'environnement virtuel...{Colors.ENDC}")
            subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)], check=True)
        
        # Obtenir le chemin de Python dans le venv
        if sys.platform == 'win32':
            python_exe = venv_dir / 'Scripts' / 'python.exe'
        else:
            python_exe = venv_dir / 'bin' / 'python'
        
        # Installer les dépendances
        print(f"{Colors.YELLOW}   Installation des dépendances...{Colors.ENDC}")
        subprocess.run(
            [str(python_exe), '-m', 'pip', 'install', '-q', '-r', 'requirements.txt'],
            cwd=str(backend_dir),
            capture_output=True
        )
        
        # Démarrer le serveur Flask
        print(f"{Colors.GREEN}✅ Démarrage du serveur Flask...{Colors.ENDC}")
        print(f"   URL: http://localhost:5000")
        
        process = subprocess.Popen(
            [str(python_exe), 'app.py'],
            cwd=str(backend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(2)  # Attendre que le serveur démarre
        return process
    except Exception as e:
        print(f"{Colors.RED}❌ Erreur lors du démarrage du backend: {e}{Colors.ENDC}")
        return None

def start_frontend():
    """Démarrer le serveur HTTP pour le frontend"""
    frontend_dir = Path(__file__).parent / 'all' / 'snel-payroll-dashboard'
    
    if not frontend_dir.exists():
        print(f"{Colors.RED}❌ Erreur: Répertoire {frontend_dir} non trouvé{Colors.ENDC}")
        return None
    
    print(f"\n{Colors.BLUE}Démarrage du serveur HTTP...{Colors.ENDC}")
    print(f"   Répertoire: {frontend_dir}")
    
    try:
        print(f"{Colors.GREEN}✅ Démarrage du serveur sur port 8000...{Colors.ENDC}")
        print(f"   URL: http://localhost:8000")
        
        process = subprocess.Popen(
            [sys.executable, '-m', 'http.server', '8000'],
            cwd=str(frontend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(1)
        return process
    except Exception as e:
        print(f"{Colors.RED}❌ Erreur lors du démarrage du frontend: {e}{Colors.ENDC}")
        return None

def open_browser():
    """Ouvrir le navigateur"""
    print(f"\n{Colors.CYAN}Ouverture du navigateur...{Colors.ENDC}")
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:8000')
        print(f"{Colors.GREEN}✅ Navigateur ouvert sur http://localhost:8000{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.YELLOW}⚠️  Impossible d'ouvrir le navigateur automatiquement{Colors.ENDC}")
        print(f"   Ouvrez manuellement: http://localhost:8000")

def main():
    print_header()
    
    # Vérifications préalables
    print(f"{Colors.CYAN}Vérifications préalables...{Colors.ENDC}")
    check_python()
    has_mysql = check_mysql()
    
    if not has_mysql:
        response = input(f"\n{Colors.YELLOW}Continuer sans MySQL ? (y/n): {Colors.ENDC}")
        if response.lower() != 'y':
            print(f"{Colors.RED}Opération annulée{Colors.ENDC}")
            sys.exit(1)
    
    # Démarrer les services
    print(f"\n{Colors.CYAN}Démarrage des services...{Colors.ENDC}")
    backend_process = start_backend()
    frontend_process = start_frontend()
    
    if not backend_process or not frontend_process:
        print(f"\n{Colors.RED}❌ Erreur lors du démarrage des services{Colors.ENDC}")
        sys.exit(1)
    
    # Ouvrir le navigateur
    open_browser()
    
    # Afficher les informations
    print(f"""
{Colors.CYAN}╔════════════════════════════════════════════════════╗
║{Colors.GREEN}  Système démarré avec succès!{Colors.CYAN}                  ║
╠════════════════════════════════════════════════════╣
║ {Colors.BOLD}Backend:{Colors.ENDC}  http://localhost:5000              {Colors.CYAN}║
║ {Colors.BOLD}Frontend:{Colors.ENDC} http://localhost:8000              {Colors.CYAN}║
╠════════════════════════════════════════════════════╣
║ Appuyez sur Ctrl+C pour arrêter tous les services  ║
╚════════════════════════════════════════════════════╝{Colors.ENDC}
    """)
    
    # Garder les processus actifs
    try:
        while True:
            time.sleep(1)
            if backend_process.poll() is not None:
                print(f"{Colors.RED}❌ Backend arrêté{Colors.ENDC}")
                break
            if frontend_process.poll() is not None:
                print(f"{Colors.RED}❌ Frontend arrêté{Colors.ENDC}")
                break
    except KeyboardInterrupt:
        print(f"\n{Colors.CYAN}Arrêt des services...{Colors.ENDC}")
        backend_process.terminate()
        frontend_process.terminate()
        time.sleep(1)
        backend_process.kill()
        frontend_process.kill()
        print(f"{Colors.GREEN}✅ Services arrêtés{Colors.ENDC}")
        sys.exit(0)

if __name__ == '__main__':
    main()
