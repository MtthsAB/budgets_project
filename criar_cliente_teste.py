#!/usr/bin/env python3
"""
Script para criar cliente de teste
"""
import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from clientes.models import Cliente
from authentication.models import CustomUser

def main():
    print("Criando cliente de teste...")
    
    # Obter usuário admin
    admin_user = CustomUser.objects.filter(email='admin@essere.com').first()
    
    if not admin_user:
        print("✗ Usuário admin não encontrado!")
        return
    
    # Verificar se cliente teste já existe
    cliente_teste = Cliente.objects.filter(email='cliente@teste.com').first()
    
    if cliente_teste:
        print(f"✓ Cliente teste já existe: {cliente_teste.nome_empresa}")
    else:
        # Criar cliente teste
        cliente_teste = Cliente.objects.create(
            nome_empresa='Empresa Teste Ltda',
            representante='João Silva',
            cnpj='12.345.678/0001-90',
            inscricao_estadual='123456789',
            logradouro='Rua Teste',
            numero='123',
            complemento='Sala 1',
            bairro='Centro',
            cidade='São Paulo',
            estado='SP',
            cep='01234-567',
            telefone='(11) 99999-9999',
            email='cliente@teste.com',
            created_by=admin_user,
            updated_by=admin_user
        )
        
        print(f"✓ Cliente teste criado: {cliente_teste.nome_empresa}")
        print(f"  - Email: {cliente_teste.email}")
        print(f"  - Telefone: {cliente_teste.telefone}")
        print(f"  - CNPJ: {cliente_teste.cnpj}")
    
    # Verificar total de clientes
    total_clientes = Cliente.objects.count()
    print(f"\nTotal de clientes no sistema: {total_clientes}")

if __name__ == "__main__":
    main()
