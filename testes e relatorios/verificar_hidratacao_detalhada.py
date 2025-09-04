#!/usr/bin/env python
"""
Script para verificar quais campos específicos não estão sendo hidratados.
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
sys.path.append('/home/matas/projetos/Project')
django.setup()

# Adicionar testserver ao ALLOWED_HOSTS
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from bs4 import BeautifulSoup
from django.test import Client
from authentication.models import CustomUser, TipoPermissao
from produtos.models import Produto


def main():
    print("🔍 Verificando hidratação detalhada dos campos...")
    
    try:
        # Configurar cliente de teste
        client = Client()
        
        # Criar/atualizar usuário admin
        user, created = CustomUser.objects.get_or_create(
            email='admin@test.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'Test',
                'is_staff': True,
                'is_superuser': True,
                'tipo_permissao': TipoPermissao.ADMIN
            }
        )
        
        if not created:
            user.tipo_permissao = TipoPermissao.ADMIN
            user.is_staff = True
            user.is_superuser = True
            user.save()
        
        # Fazer login
        client.force_login(user)
        
        # Buscar o sofá para comparar com os dados no form
        sofa = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá').first()
        print(f"🛋️ Sofá: {sofa.ref_produto} - {sofa.nome_produto}")
        
        # Verificar dados dos módulos no banco
        print("\n📦 Dados dos Módulos no Banco:")
        for i, modulo in enumerate(sofa.modulos.all()):
            print(f"   Módulo {i}: {modulo.nome}")
            print(f"      📏 Profundidade: {modulo.profundidade}")
            print(f"      📏 Altura: {modulo.altura}")
            print(f"      📏 Braço: {modulo.braco}")
            print(f"      📝 Descrição: {modulo.descricao}")
            
            for j, tamanho in enumerate(modulo.tamanhos_detalhados.all()):
                print(f"      Tamanho {j}: {tamanho.descricao}")
                print(f"         📏 Largura Total: {tamanho.largura_total}")
                print(f"         📏 Largura Assento: {tamanho.largura_assento}")
                print(f"         🧵 Tecido (m): {tamanho.tecido_metros}")
                print(f"         📦 Volume (m³): {tamanho.volume_m3}")
                print(f"         ⚖️ Peso (kg): {tamanho.peso_kg}")
                print(f"         💰 Preço: {tamanho.preco}")
        
        # Acessar a página de edição
        url = '/sofas/6/editar-formsets/'
        response = client.get(url)
        
        if response.status_code != 200:
            print(f"❌ Erro ao acessar página: {response.status_code}")
            return
        
        # Analisar o HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print("\n🔍 Verificando hidratação no HTML:")
        
        # Verificar campos dos módulos
        for i in range(2):  # Sabemos que temos 2 módulos
            print(f"\n📦 Módulo {i}:")
            
            # Nome
            nome_input = soup.find('input', {'name': f'modulos-{i}-nome'})
            print(f"   📝 Nome: {nome_input.get('value') if nome_input else 'CAMPO NÃO ENCONTRADO'}")
            
            # Profundidade
            prof_input = soup.find('input', {'name': f'modulos-{i}-profundidade'})
            print(f"   📏 Profundidade: {prof_input.get('value') if prof_input else 'CAMPO NÃO ENCONTRADO'}")
            
            # Altura
            altura_input = soup.find('input', {'name': f'modulos-{i}-altura'})
            print(f"   📏 Altura: {altura_input.get('value') if altura_input else 'CAMPO NÃO ENCONTRADO'}")
            
            # Braço
            braco_input = soup.find('input', {'name': f'modulos-{i}-braco'})
            print(f"   📏 Braço: {braco_input.get('value') if braco_input else 'CAMPO NÃO ENCONTRADO'}")
            
            # Descrição
            desc_input = soup.find('textarea', {'name': f'modulos-{i}-descricao'})
            print(f"   📝 Descrição: {desc_input.get_text().strip() if desc_input else 'CAMPO NÃO ENCONTRADO'}")
        
        # Verificar campos dos tamanhos
        print(f"\n📏 Verificando Tamanhos:")
        tamanho_inputs = soup.find_all('input', {'name': lambda x: x and 'largura_total' in x})
        
        for i, input_field in enumerate(tamanho_inputs):
            prefix = input_field.get('name').replace('-largura_total', '')
            print(f"\n   Tamanho {i} (prefix: {prefix}):")
            
            # Largura Total
            print(f"      📏 Largura Total: {input_field.get('value') or 'VAZIO'}")
            
            # Largura Assento
            assento_input = soup.find('input', {'name': f'{prefix}-largura_assento'})
            print(f"      📏 Largura Assento: {assento_input.get('value') if assento_input else 'CAMPO NÃO ENCONTRADO'}")
            
            # Tecido
            tecido_input = soup.find('input', {'name': f'{prefix}-tecido_metros'})
            print(f"      🧵 Tecido: {tecido_input.get('value') if tecido_input else 'CAMPO NÃO ENCONTRADO'}")
            
            # Volume
            volume_input = soup.find('input', {'name': f'{prefix}-volume_m3'})
            print(f"      📦 Volume: {volume_input.get('value') if volume_input else 'CAMPO NÃO ENCONTRADO'}")
            
            # Peso
            peso_input = soup.find('input', {'name': f'{prefix}-peso_kg'})
            print(f"      ⚖️ Peso: {peso_input.get('value') if peso_input else 'CAMPO NÃO ENCONTRADO'}")
            
            # Preço
            preco_input = soup.find('input', {'name': f'{prefix}-preco'})
            print(f"      💰 Preço: {preco_input.get('value') if preco_input else 'CAMPO NÃO ENCONTRADO'}")
            
            # Descrição
            desc_input = soup.find('textarea', {'name': f'{prefix}-descricao'})
            if desc_input:
                print(f"      📝 Descrição: {desc_input.get_text().strip() or 'VAZIO'}")
            else:
                print(f"      📝 Descrição: CAMPO NÃO ENCONTRADO")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
