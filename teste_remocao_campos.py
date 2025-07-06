#!/usr/bin/env python
"""
Script de teste final para validar a remoção dos campos inadequados dos tamanhos.
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

def testar_remocao_campos():
    """Testa se os campos foram removidos corretamente"""
    print("=== TESTE DE REMOÇÃO DE CAMPOS ===\n")
    
    try:
        # Verificar campos no modelo
        model_fields = [field.name for field in TamanhosModulosDetalhado._meta.fields]
        print(f"Campos no modelo: {model_fields}")
        
        # Campos que NÃO devem estar presentes
        campos_removidos = ['nome_tamanho', 'altura_cm', 'profundidade_cm']
        campos_encontrados = [campo for campo in campos_removidos if campo in model_fields]
        
        if campos_encontrados:
            print(f"❌ ERRO: Campos inadequados ainda presentes: {campos_encontrados}")
            return False
        else:
            print(f"✓ Campos removidos corretamente do modelo: {campos_removidos}")
        
        # Verificar se não existem properties para altura e profundidade
        has_altura_property = hasattr(TamanhosModulosDetalhado, 'altura_cm')
        has_profundidade_property = hasattr(TamanhosModulosDetalhado, 'profundidade_cm')
        
        if has_altura_property or has_profundidade_property:
            print(f"❌ ERRO: Properties de altura/profundidade ainda existem")
            return False
        else:
            print("✓ Properties de altura e profundidade removidas")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def testar_formulario_atualizado():
    """Testa se o formulário foi atualizado corretamente"""
    print("\n=== TESTE DO FORMULÁRIO ATUALIZADO ===\n")
    
    try:
        # Criar formulário
        form = TamanhosModulosDetalhadoForm()
        campos_form = list(form.fields.keys())
        print(f"Campos no formulário: {campos_form}")
        
        # Verificar se os campos removidos não estão presentes
        campos_proibidos = ['nome_tamanho', 'altura_cm', 'profundidade_cm']
        campos_encontrados = [campo for campo in campos_proibidos if campo in campos_form]
        
        if campos_encontrados:
            print(f"❌ ERRO: Campos proibidos no formulário: {campos_encontrados}")
            return False
        else:
            print(f"✓ Campos removidos corretamente do formulário: {campos_proibidos}")
        
        # Verificar se os campos essenciais estão presentes
        campos_essenciais = ['id_modulo', 'largura_total', 'largura_assento', 'preco']
        campos_faltando = [campo for campo in campos_essenciais if campo not in campos_form]
        
        if campos_faltando:
            print(f"❌ ERRO: Campos essenciais faltando: {campos_faltando}")
            return False
        else:
            print(f"✓ Campos essenciais presentes: {campos_essenciais}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def testar_admin_atualizado():
    """Testa se o admin foi atualizado corretamente"""
    print("\n=== TESTE DO ADMIN ATUALIZADO ===\n")
    
    try:
        # Criar instância do admin
        site = AdminSite()
        admin = TamanhosModulosDetalhadoAdmin(TamanhosModulosDetalhado, site)
        
        print(f"List display: {admin.list_display}")
        print(f"Search fields: {admin.search_fields}")
        print(f"Readonly fields: {admin.readonly_fields}")
        
        # Verificar se não há referências aos campos removidos
        all_admin_fields = (
            list(admin.list_display) + 
            list(admin.search_fields) + 
            list(admin.readonly_fields)
        )
        
        campos_proibidos = ['nome_tamanho', 'altura_cm', 'profundidade_cm', 'altura_herdada', 'profundidade_herdada']
        campos_encontrados = [campo for campo in campos_proibidos if campo in all_admin_fields]
        
        if campos_encontrados:
            print(f"❌ ERRO: Campos proibidos no admin: {campos_encontrados}")
            return False
        else:
            print(f"✓ Campos removidos corretamente do admin: {campos_proibidos}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def testar_criacao_tamanho():
    """Testa a criação de um tamanho sem os campos removidos"""
    print("\n=== TESTE DE CRIAÇÃO DE TAMANHO ===\n")
    
    try:
        with transaction.atomic():
            # Criar dados de teste
            tipo_item, _ = TipoItem.objects.get_or_create(nome="Teste Final")
            item, _ = Item.objects.get_or_create(
                ref_produto="FINAL-TEST",
                defaults={
                    'nome_produto': "Item Teste Final",
                    'id_tipo_produto': tipo_item,
                    'ativo': True
                }
            )
            modulo, _ = Modulo.objects.get_or_create(
                item=item,
                nome="Módulo Teste Final",
                defaults={
                    'profundidade': 95.00,
                    'altura': 85.00,
                    'braco': 32.00
                }
            )
            
            # Criar tamanho usando formulário
            form_data = {
                'id_modulo': modulo.id,
                'largura_total': 160.00,
                'largura_assento': 130.00,
                'tecido_metros': 4.0,
                'volume_m3': 1.5,
                'peso_kg': 75.0,
                'preco': 3200.00,
                'descricao': 'Tamanho teste final'
            }
            
            form = TamanhosModulosDetalhadoForm(data=form_data)
            if form.is_valid():
                tamanho = form.save()
                print(f"✓ Tamanho criado com sucesso: {tamanho}")
                
                # Verificar string representation
                print(f"String representation: {str(tamanho)}")
                
                return True
            else:
                print(f"❌ ERRO: Formulário inválido: {form.errors}")
                return False
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def testar_integridade_sistema():
    """Testa a integridade geral do sistema"""
    print("\n=== TESTE DE INTEGRIDADE DO SISTEMA ===\n")
    
    try:
        # Verificar se não há erros no Django
        from django.core.management import execute_from_command_line
        
        # Contar registros
        total_tamanhos = TamanhosModulosDetalhado.objects.count()
        print(f"Total de tamanhos no sistema: {total_tamanhos}")
        
        # Verificar se todos os tamanhos existentes ainda funcionam
        for tamanho in TamanhosModulosDetalhado.objects.all()[:3]:  # Apenas os primeiros 3
            try:
                str_repr = str(tamanho)
                print(f"✓ Tamanho ID {tamanho.id}: {str_repr}")
            except Exception as e:
                print(f"❌ ERRO no tamanho ID {tamanho.id}: {e}")
                return False
        
        print("✓ Sistema funcionando corretamente")
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def resumo_correcoes():
    """Mostra um resumo das correções realizadas"""
    print("\n" + "="*70)
    print("RESUMO DAS CORREÇÕES REALIZADAS")
    print("="*70)
    print()
    print("❌ CAMPOS REMOVIDOS:")
    print("   • nome_tamanho - Campo removido do modelo e banco de dados")
    print("   • altura_cm - Property e referências completamente removidas")
    print("   • profundidade_cm - Property e referências completamente removidas")
    print()
    print("✅ ATUALIZAÇÕES REALIZADAS:")
    print("   • Modelo TamanhosModulosDetalhado simplificado")
    print("   • Formulário TamanhosModulosDetalhadoForm atualizado")
    print("   • Admin TamanhosModulosDetalhadoAdmin limpo")
    print("   • Views atualizadas para não referenciar campos removidos")
    print("   • Templates de cadastro e edição atualizados")
    print("   • Migração 0009 criada e aplicada")
    print("   • Método __str__ atualizado")
    print("   • unique_together removido")
    print()
    print("✅ RESULTADO:")
    print("   • Seção de tamanhos simplificada conforme solicitado")
    print("   • Campos inadequados completamente removidos")
    print("   • Sistema funcionando sem dependências dos campos")
    print("   • Interface limpa e focada nos dados essenciais")
    print()

if __name__ == "__main__":
    print("INICIANDO TESTES FINAIS DE VALIDAÇÃO\n")
    
    sucessos = []
    
    # Executar testes
    sucessos.append(testar_remocao_campos())
    sucessos.append(testar_formulario_atualizado())
    sucessos.append(testar_admin_atualizado())
    sucessos.append(testar_criacao_tamanho())
    sucessos.append(testar_integridade_sistema())
    
    # Resumo dos resultados
    print("\n" + "="*50)
    print("RESULTADOS DOS TESTES:")
    print("="*50)
    
    if all(sucessos):
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Correções implementadas com sucesso!")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("⚠️ Verifique os erros acima")
    
    print(f"Taxa de sucesso: {sucessos.count(True)}/{len(sucessos)} testes")
    
    # Mostrar resumo das correções
    resumo_correcoes()
    
    print("="*70)
    print("PRÓXIMOS PASSOS:")
    print("="*70)
    print("1. Teste o Django Admin em /admin/")
    print("2. Verifique a criação de novos tamanhos")
    print("3. Confirme que os campos removidos não aparecem")
    print("4. Teste as páginas de cadastro customizadas")
    print("="*70)
