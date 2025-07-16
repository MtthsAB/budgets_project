#!/usr/bin/env python3

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.db import connection
from produtos.models import Acessorio

print("=== INVESTIGAÇÃO TABELA INTERMEDIÁRIA ===")

# Obter o nome da tabela intermediária M2M
acessorio_meta = Acessorio._meta
for field in acessorio_meta.get_fields():
    if field.name == 'produtos_vinculados':
        print(f"Campo: {field.name}")
        print(f"Tipo: {type(field)}")
        if hasattr(field, 'through'):
            print(f"Tabela intermediária: {field.through._meta.db_table}")
        if hasattr(field, 'remote_field'):
            print(f"Remote field: {field.remote_field}")
        break

# Verificar tabelas no banco (PostgreSQL)
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """)
    tabelas = cursor.fetchall()
    
    print(f"\nTodas as tabelas do banco ({len(tabelas)}):")
    tabelas_acessorio = []
    for tabela in tabelas:
        nome_tabela = tabela[0]
        if 'acessorio' in nome_tabela.lower():
            tabelas_acessorio.append(nome_tabela)
            print(f"  ✓ {nome_tabela}")
        elif nome_tabela.startswith('produtos_'):
            print(f"  ! {nome_tabela}")
    
    print(f"\nTabelas relacionadas a acessórios: {tabelas_acessorio}")
    
    # Verificar conteúdo da tabela intermediária
    for tabela in tabelas_acessorio:
        if 'produtos_vinculados' in tabela or 'acessorio_produtos' in tabela:
            print(f"\nConteúdo da tabela {tabela}:")
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabela};")
                count = cursor.fetchone()[0]
                print(f"  Total de registros: {count}")
                
                if count > 0:
                    cursor.execute(f"SELECT * FROM {tabela} LIMIT 5;")
                    registros = cursor.fetchall()
                    
                    # Obter nomes das colunas
                    cursor.execute(f"PRAGMA table_info({tabela});")
                    colunas = [col[1] for col in cursor.fetchall()]
                    print(f"  Colunas: {colunas}")
                    
                    for registro in registros:
                        print(f"  Registro: {registro}")
            except Exception as e:
                print(f"  Erro ao acessar tabela: {e}")

print("\n=== FIM INVESTIGAÇÃO ===")
