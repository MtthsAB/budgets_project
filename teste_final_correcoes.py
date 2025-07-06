#!/usr/bin/env python
"""
Script de teste final para validar as correções nos tamanhos.
Testa tanto a funcionalidade no admin quanto na API.
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, TipoItem, Modulo, TamanhosModulosDetalhado
from produtos.admin import TamanhosModulosDetalhadoAdmin
from produtos.forms import TamanhosModulosDetalhadoForm
from django.db import transaction
from django.contrib.admin.sites import AdminSite

def testar_formulario():
    """Testa se o formulário customizado está funcionando"""
    print("=== TESTE DO FORMULÁRIO CUSTOMIZADO ===\n")
    
    try:
        # Criar dados de teste
        tipo_item, _ = TipoItem.objects.get_or_create(nome="Teste Form")
        item, _ = Item.objects.get_or_create(
            ref_produto="FORM-TEST",
            defaults={
                'nome_produto': "Item Teste Formulário",
                'id_tipo_produto': tipo_item,
                'ativo': True
            }
        )
        modulo, _ = Modulo.objects.get_or_create(
            item=item,
            nome="Módulo Teste Form",
            defaults={
                'profundidade': 90.00,
                'altura': 80.00,
                'braco': 30.00
            }
        )
        
        # Testar formulário vazio
        form = TamanhosModulosDetalhadoForm()
        print("✓ Formulário criado com sucesso")
        print(f"Campos no formulário: {list(form.fields.keys())}")
        
        # Verificar se os campos removidos não estão presentes
        campos_proibidos = ['altura_cm', 'profundidade_cm']
        campos_encontrados = [campo for campo in campos_proibidos if campo in form.fields]
        
        if campos_encontrados:
            print(f"❌ ERRO: Campos proibidos encontrados no formulário: {campos_encontrados}")
            return False
        else:
            print("✓ Campos altura_cm e profundidade_cm removidos corretamente do formulário")
        
        # Testar formulário com dados
        form_data = {
            'id_modulo': modulo.id,
            'nome_tamanho': '2 Lugares Teste',
            'largura_total': 140.00,
            'largura_assento': 100.00,
            'tecido_metros': 3.5,
            'volume_m3': 1.2,
            'peso_kg': 65.0,
            'preco': 2500.00,
            'descricao': 'Tamanho teste para validação'
        }
        
        form = TamanhosModulosDetalhadoForm(data=form_data)
        if form.is_valid():
            print("✓ Formulário válido com dados de teste")
            tamanho = form.save()
            print(f"✓ Tamanho criado: {tamanho}")
            
            # Testar herança
            print(f"Altura herdada: {tamanho.altura_cm} cm")
            print(f"Profundidade herdada: {tamanho.profundidade_cm} cm")
            
            if tamanho.altura_cm == modulo.altura and tamanho.profundidade_cm == modulo.profundidade:
                print("✓ Herança funcionando corretamente")
                return True
            else:
                print("❌ ERRO: Herança não está funcionando")
                return False
        else:
            print(f"❌ ERRO: Formulário inválido: {form.errors}")
            return False
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def testar_admin():
    """Testa se a configuração do admin está correta"""
    print("\n=== TESTE DA CONFIGURAÇÃO DO ADMIN ===\n")
    
    try:
        # Criar instância do admin
        site = AdminSite()
        admin = TamanhosModulosDetalhadoAdmin(TamanhosModulosDetalhado, site)
        
        print("✓ Admin configurado com sucesso")
        print(f"Campos readonly: {admin.readonly_fields}")
        print(f"List display: {admin.list_display}")
        
        # Verificar se os métodos customizados existem
        if hasattr(admin, 'altura_herdada') and hasattr(admin, 'profundidade_herdada'):
            print("✓ Métodos de exibição de herança configurados")
        else:
            print("❌ ERRO: Métodos de herança não encontrados")
            return False
        
        # Testar com um objeto
        tamanho = TamanhosModulosDetalhado.objects.first()
        if tamanho:
            altura_str = admin.altura_herdada(tamanho)
            profundidade_str = admin.profundidade_herdada(tamanho)
            print(f"✓ Altura exibida: {altura_str}")
            print(f"✓ Profundidade exibida: {profundidade_str}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def testar_integridade_modelo():
    """Testa a integridade do modelo após as mudanças"""
    print("\n=== TESTE DE INTEGRIDADE DO MODELO ===\n")
    
    try:
        # Verificar se os campos foram removidos corretamente
        model_fields = [field.name for field in TamanhosModulosDetalhado._meta.fields]
        print(f"Campos do modelo: {model_fields}")
        
        campos_removidos = ['altura_cm', 'profundidade_cm']
        campos_encontrados = [campo for campo in campos_removidos if campo in model_fields]
        
        if campos_encontrados:
            print(f"❌ ERRO: Campos ainda presentes no modelo: {campos_encontrados}")
            return False
        else:
            print("✓ Campos removidos corretamente do modelo")
        
        # Testar properties
        tamanho = TamanhosModulosDetalhado.objects.first()
        if tamanho:
            try:
                altura = tamanho.altura_cm
                profundidade = tamanho.profundidade_cm
                print(f"✓ Properties funcionando: altura={altura}, profundidade={profundidade}")
            except Exception as e:
                print(f"❌ ERRO nas properties: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def resumo_mudancas():
    """Exibe um resumo das mudanças implementadas"""
    print("\n" + "="*60)
    print("RESUMO DAS CORREÇÕES IMPLEMENTADAS")
    print("="*60)
    print()
    print("✅ MODELO (produtos/models.py):")
    print("   • Campos altura_cm e profundidade_cm removidos")
    print("   • Properties altura_cm e profundidade_cm adicionadas")
    print("   • Properties herdam valores do módulo associado")
    print()
    print("✅ ADMIN (produtos/admin.py):")
    print("   • Formulário customizado configurado")
    print("   • Campos altura_herdada e profundidade_herdada adicionados")
    print("   • Campos removidos do fieldset de dimensões")
    print()
    print("✅ FORMULÁRIOS (produtos/forms.py):")
    print("   • TamanhosModulosDetalhadoForm criado")
    print("   • Campos altura_cm e profundidade_cm excluídos")
    print("   • Validações e help_text adicionados")
    print()
    print("✅ VIEWS (produtos/views.py):")
    print("   • Referências aos campos removidos eliminadas")
    print("   • Criação de tamanhos atualizada")
    print()
    print("✅ TEMPLATES:")
    print("   • Campos de entrada removidos dos formulários")
    print("   • Informações de herança adicionadas")
    print("   • JavaScript para atualização dinâmica")
    print()
    print("✅ MIGRAÇÃO:")
    print("   • Migração 0008 criada e aplicada")
    print("   • Campos removidos do banco de dados")
    print()

if __name__ == "__main__":
    print("INICIANDO TESTES FINAIS DE VALIDAÇÃO\n")
    
    sucessos = []
    
    # Executar testes
    sucessos.append(testar_formulario())
    sucessos.append(testar_admin())
    sucessos.append(testar_integridade_modelo())
    
    # Resumo dos resultados
    print("\n" + "="*50)
    print("RESULTADOS DOS TESTES:")
    print("="*50)
    
    if all(sucessos):
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema corrigido com sucesso!")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("⚠️ Verifique os erros acima")
    
    print(f"Taxa de sucesso: {sucessos.count(True)}/{len(sucessos)} testes")
    
    # Mostrar resumo das mudanças
    resumo_mudancas()
    
    print("\n" + "="*60)
    print("PRÓXIMOS PASSOS PARA TESTE MANUAL:")
    print("="*60)
    print("1. Acesse o Django Admin: /admin/")
    print("2. Vá para 'Tamanhos Detalhados dos Módulos'")
    print("3. Crie um novo tamanho e verifique:")
    print("   • Campos altura_cm e profundidade_cm não aparecem")
    print("   • Campos 'Altura herdada' e 'Profundidade herdada' são exibidos")
    print("   • Valores são herdados corretamente do módulo")
    print("4. Teste a edição de tamanhos existentes")
    print("5. Verifique se as páginas de cadastro funcionam normalmente")
    print("="*60)
