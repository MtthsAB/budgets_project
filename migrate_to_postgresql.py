#!/usr/bin/env python
"""
Script de Migração SQLite para PostgreSQL
Sistema de Produtos - Migração de Dados

Este script realiza a migração completa dos dados do SQLite para PostgreSQL
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command, description):
    """Executa um comando e exibe o resultado"""
    print(f"\n📋 {description}")
    print(f"Comando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro: {e.stderr}")
        return False

def main():
    print("=" * 60)
    print("🔄 MIGRAÇÃO SQLite PARA PostgreSQL")
    print("Sistema de Produtos")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not Path('manage.py').exists():
        print("❌ Erro: Arquivo manage.py não encontrado!")
        print("Execute este script no diretório raiz do projeto Django")
        sys.exit(1)
    
    # 1. Backup dos dados SQLite
    sqlite_db = Path('db.sqlite3')
    backup_file = Path('backup_sqlite_data.json')
    
    if sqlite_db.exists():
        print("\n1️⃣ Fazendo backup dos dados do SQLite...")
        success = run_command(
            'python manage.py dumpdata --natural-foreign --natural-primary '
            '--exclude=contenttypes --exclude=auth.Permission '
            '--exclude=admin.logentry --exclude=sessions.session '
            '> backup_sqlite_data.json',
            "Criando backup dos dados"
        )
        
        if success and backup_file.exists():
            file_size = backup_file.stat().st_size
            print(f"✅ Backup criado: {backup_file.name} ({file_size} bytes)")
        else:
            print("❌ Falha ao criar backup")
    else:
        print("\n⚠️  Arquivo db.sqlite3 não encontrado - criando projeto do zero")
    
    # 2. Criar migrations
    print("\n2️⃣ Criando migrations...")
    run_command('python manage.py makemigrations', "Gerando migrations")
    
    # 3. Aplicar migrations no PostgreSQL
    print("\n3️⃣ Aplicando migrations no PostgreSQL...")
    success = run_command('python manage.py migrate', "Aplicando migrations")
    
    if not success:
        print("❌ Falha ao aplicar migrations. Verifique:")
        print("   - Se o PostgreSQL está rodando")
        print("   - Se as configurações do .env estão corretas")
        print("   - Se o banco 'sistema_produtos' existe")
        sys.exit(1)
    
    # 4. Carregar dados do backup (se existir)
    if backup_file.exists():
        print("\n4️⃣ Carregando dados do backup...")
        success = run_command(
            'python manage.py loaddata backup_sqlite_data.json',
            "Carregando dados salvos"
        )
        
        if success:
            print("✅ Dados migrados com sucesso!")
        else:
            print("⚠️  Alguns dados podem não ter sido migrados corretamente")
    
    # 5. Verificar se existe superuser
    print("\n5️⃣ Verificando superuser...")
    try:
        # Definir o path do Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
        
        import django
        django.setup()
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(is_superuser=True).exists():
            print("🔧 Criando superuser padrão...")
            User.objects.create_superuser(
                username='admin',
                email='admin@sistema.com',
                password='admin123'
            )
            print("✅ Superuser criado:")
            print("   👤 Usuário: admin")
            print("   🔑 Senha: admin123")
        else:
            print("✅ Superuser já existe")
            
    except Exception as e:
        print(f"⚠️  Erro ao verificar superuser: {e}")
    
    # 6. Teste final
    print("\n6️⃣ Testando conexão com PostgreSQL...")
    success = run_command(
        'python manage.py check --database default',
        "Verificando configuração do banco"
    )
    
    # Resumo final
    print("\n" + "=" * 60)
    print("🎉 MIGRAÇÃO CONCLUÍDA!")
    print("=" * 60)
    
    if success:
        print("✅ Sistema migrado para PostgreSQL com sucesso!")
        print("\n📝 Próximos passos:")
        print("   1. python manage.py runserver")
        print("   2. Acesse: http://localhost:8000")
        print("   3. Admin: http://localhost:8000/admin")
        print("   4. Login: admin / admin123")
        
        print("\n📁 Arquivos importantes:")
        print(f"   - {backup_file.name} (backup dos dados SQLite)")
        print("   - .env (configurações PostgreSQL)")
        print("   - migrate_to_postgresql.py (este script)")
        
        print("\n⚠️  Lembrete: Altere as senhas padrão em produção!")
    else:
        print("❌ Migração com problemas. Verifique os logs acima.")
        sys.exit(1)

if __name__ == '__main__':
    main()
