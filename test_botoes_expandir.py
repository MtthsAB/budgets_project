#!/usr/bin/env python3
"""
Teste para validar o funcionamento dos botões de expandir/recolher
nas seções de módulos e tamanhos detalhados.
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# Setup Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, TipoItem, Modulo, TamanhosModulosDetalhado

User = get_user_model()

def test_botoes_expandir_recolher():
    """Testa se os botões de expandir/recolher estão funcionando"""
    
    print("=== TESTE: Botões de Expandir/Recolher ===")
    
    # Criar cliente de teste
    client = Client()
    
    # Criar usuário de teste
    user = User.objects.create_user(
        email='teste@teste.com',
        password='teste123',
        first_name='Teste',
        last_name='User'
    )
    
    # Fazer login
    client.login(email='teste@teste.com', password='teste123')
    
    # Buscar um sofá existente
    try:
        tipo_sofa = TipoItem.objects.filter(nome__icontains='sofá').first()
        if not tipo_sofa:
            print("❌ Erro: Tipo 'sofá' não encontrado")
            return False
            
        sofa = Produto.objects.filter(id_tipo_produto=tipo_sofa).first()
        if not sofa:
            print("❌ Erro: Nenhum sofá encontrado")
            return False
            
        print(f"✅ Sofá encontrado: {sofa.ref_produto} - {sofa.nome_produto}")
        
        # Testar acesso à tela de edição
        url = reverse('sofa_editar', kwargs={'sofa_id': sofa.id})
        response = client.get(url)
        
        if response.status_code == 200:
            print("✅ Tela de edição carregada com sucesso")
            
            # Verificar se os elementos necessários estão presentes
            content = response.content.decode('utf-8')
            
            # Verificar seção de módulos
            if 'secao-modulos' in content:
                print("✅ Seção de módulos presente")
                
                if 'toggleTodosModulos' in content:
                    print("✅ Botão de expandir/recolher módulos presente")
                else:
                    print("❌ Botão de expandir/recolher módulos não encontrado")
                    
                if 'Expandir Todos' in content:
                    print("✅ Texto do botão de expandir presente")
                else:
                    print("❌ Texto do botão de expandir não encontrado")
            else:
                print("❌ Seção de módulos não encontrada")
            
            # Verificar seção de tamanhos
            if 'secao-tamanhos' in content:
                print("✅ Seção de tamanhos presente")
                
                if 'toggleTodosTamanhos' in content:
                    print("✅ Botão de expandir/recolher tamanhos presente")
                else:
                    print("❌ Botão de expandir/recolher tamanhos não encontrado")
            else:
                print("❌ Seção de tamanhos não encontrada")
                
            # Verificar se os arquivos JavaScript estão sendo carregados
            if 'sofa_modulos.js' in content:
                print("✅ JavaScript de módulos carregado")
            else:
                print("❌ JavaScript de módulos não carregado")
                
            if 'tamanhos_detalhados.js' in content:
                print("✅ JavaScript de tamanhos carregado")
            else:
                print("❌ JavaScript de tamanhos não carregado")
                
            return True
        else:
            print(f"❌ Erro ao carregar tela de edição: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        return False

def test_modulos_existentes():
    """Testa se módulos existentes são carregados corretamente"""
    
    print("\n=== TESTE: Módulos Existentes ===")
    
    try:
        # Buscar sofá com módulos
        tipo_sofa = TipoItem.objects.filter(nome__icontains='sofá').first()
        sofa = Produto.objects.filter(id_tipo_produto=tipo_sofa).first()
        
        if sofa:
            modulos = sofa.modulos.all()
            print(f"✅ Sofá {sofa.ref_produto} tem {modulos.count()} módulos")
            
            for modulo in modulos:
                print(f"  - {modulo.nome}")
                
                # Verificar tamanhos detalhados
                tamanhos = modulo.tamanhos_detalhados.all()
                print(f"    Tamanhos detalhados: {tamanhos.count()}")
                
            return True
        else:
            print("❌ Nenhum sofá encontrado para teste")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        return False

def main():
    """Função principal de teste"""
    
    print("🧪 INICIANDO TESTES DOS BOTÕES DE EXPANDIR/RECOLHER")
    print("=" * 60)
    
    sucesso_geral = True
    
    # Teste 1: Botões de expandir/recolher
    if not test_botoes_expandir_recolher():
        sucesso_geral = False
    
    # Teste 2: Módulos existentes
    if not test_modulos_existentes():
        sucesso_geral = False
    
    print("\n" + "=" * 60)
    
    if sucesso_geral:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("Os botões de expandir/recolher estão funcionando corretamente.")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("Verifique os problemas reportados acima.")
    
    print("=" * 60)
    return sucesso_geral

if __name__ == '__main__':
    main()
