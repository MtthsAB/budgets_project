#!/usr/bin/env python3
"""
Script para iniciar o servidor Django de forma prática
Alternativa em Python para o script start.sh
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Exibe o banner de inicialização"""
    print("🚀 Iniciando Sistema de Produtos...")
    print("=" * 50)

def check_manage_py():
    """Verifica se o manage.py existe"""
    if not Path("manage.py").exists():
        print("❌ Erro: manage.py não encontrado!")
        print("   Execute este script a partir do diretório raiz do projeto.")
        sys.exit(1)

def check_virtual_env():
    """Verifica se está em um ambiente virtual"""
    if not os.environ.get('VIRTUAL_ENV'):
        print("⚠️  Aviso: Nenhum ambiente virtual detectado.")
        print("   Recomenda-se usar um ambiente virtual.")
        print()

def run_command(command, description, exit_on_error=True):
    """Executa um comando e trata erros"""
    print(f"📦 {description}...")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} concluído com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao {description.lower()}: {e}")
        if e.stderr:
            print(f"   Erro: {e.stderr.strip()}")
        if exit_on_error:
            sys.exit(1)
        return False

def install_dependencies():
    """Instala dependências se requirements.txt existir"""
    if Path("requirements.txt").exists():
        print("📋 Verificando dependências...")
        run_command("pip install -r requirements.txt --quiet", 
                   "Instalação de dependências", exit_on_error=False)
    else:
        print("⚠️  Arquivo requirements.txt não encontrado.")

def main():
    """Função principal"""
    print_banner()
    
    # Verificações iniciais
    check_manage_py()
    check_virtual_env()
    
    # Aplicar migrações
    run_command("python manage.py migrate", "Aplicando migrações")
    print()
    
    # Coletar arquivos estáticos
    run_command("python manage.py collectstatic --noinput --verbosity 0", 
               "Coletando arquivos estáticos", exit_on_error=False)
    print()
    
    # Instalar dependências
    install_dependencies()
    print()
    
    # Iniciar servidor
    print("🌐 Iniciando servidor de desenvolvimento...")
    print("   Acesse: http://127.0.0.1:8000")
    print("   Para parar o servidor: Ctrl+C")
    print()
    print("=" * 50)
    
    try:
        subprocess.run("python manage.py runserver 0.0.0.0:8000", shell=True)
    except KeyboardInterrupt:
        print("\n\n👋 Servidor parado. Até logo!")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
