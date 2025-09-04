#!/usr/bin/env python
"""
Teste de integração completo do cadastro de sofás com acessórios
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from produtos.models import Produto, TipoItem, Acessorio, SofaAcessorio
from produtos.forms import SofaAcessorioFormSet


class TesteAcessoriosSofa(TestCase):
    """Testes para funcionalidade de acessórios em sofás"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        User = get_user_model()
        self.user = User.objects.create_superuser(
            email='test@test.com',
            password='test123'
        )
        
        # Criar tipo sofá se não existir
        self.tipo_sofa, _ = TipoItem.objects.get_or_create(
            nome='Sofás'
        )
        
        # Criar acessórios de teste
        self.acessorio1 = Acessorio.objects.create(
            ref_acessorio='ACC_TEST_1',
            nome='Acessório Teste 1',
            ativo=True,
            preco=100.00
        )
        
        self.acessorio2 = Acessorio.objects.create(
            ref_acessorio='ACC_TEST_2', 
            nome='Acessório Teste 2',
            ativo=True,
            preco=200.00
        )
        
        # Criar sofá de teste
        self.sofa = Produto.objects.create(
            ref_produto='SF_TEST',
            nome_produto='Sofá de Teste',
            id_tipo_produto=self.tipo_sofa,
            ativo=True
        )
    
    def test_modelo_sofa_acessorio(self):
        """Teste do modelo SofaAcessorio"""
        print("🧪 Testando modelo SofaAcessorio...")
        
        # Criar vinculação
        vinculacao = SofaAcessorio.objects.create(
            sofa=self.sofa,
            acessorio=self.acessorio1,
            quantidade=2,
            observacoes='Teste de vinculação'
        )
        
        # Verificar criação
        self.assertEqual(vinculacao.sofa, self.sofa)
        self.assertEqual(vinculacao.acessorio, self.acessorio1)
        self.assertEqual(vinculacao.quantidade, 2)
        self.assertEqual(vinculacao.observacoes, 'Teste de vinculação')
        
        # Verificar string representation
        expected_str = f"SF_TEST + ACC_TEST_1 (Qtd: 2)"
        self.assertEqual(str(vinculacao), expected_str)
        
        print("✅ Modelo SofaAcessorio funcionando corretamente")
    
    def test_formset_valido(self):
        """Teste do FormSet com dados válidos"""
        print("🧪 Testando FormSet com dados válidos...")
        
        post_data = {
            'acessorios-TOTAL_FORMS': '2',
            'acessorios-INITIAL_FORMS': '0',
            'acessorios-MIN_NUM_FORMS': '0',
            'acessorios-MAX_NUM_FORMS': '1000',
            
            'acessorios-0-acessorio': str(self.acessorio1.id),
            'acessorios-0-quantidade': '1',
            'acessorios-0-observacoes': 'Obs 1',
            'acessorios-0-DELETE': '',
            
            'acessorios-1-acessorio': str(self.acessorio2.id),
            'acessorios-1-quantidade': '3',
            'acessorios-1-observacoes': 'Obs 2',
            'acessorios-1-DELETE': '',
        }
        
        formset = SofaAcessorioFormSet(post_data, instance=self.sofa, prefix='acessorios')
        
        self.assertTrue(formset.is_valid(), f"FormSet inválido: {formset.errors}")
        
        # Salvar e verificar
        vinculacoes = formset.save()
        self.assertEqual(len(vinculacoes), 2)
        
        # Verificar dados salvos
        vinc1 = SofaAcessorio.objects.get(sofa=self.sofa, acessorio=self.acessorio1)
        self.assertEqual(vinc1.quantidade, 1)
        self.assertEqual(vinc1.observacoes, 'Obs 1')
        
        vinc2 = SofaAcessorio.objects.get(sofa=self.sofa, acessorio=self.acessorio2)
        self.assertEqual(vinc2.quantidade, 3)
        self.assertEqual(vinc2.observacoes, 'Obs 2')
        
        print("✅ FormSet válido funcionando corretamente")
    
    def test_formset_duplicacao(self):
        """Teste de validação para acessórios duplicados"""
        print("🧪 Testando validação de acessórios duplicados...")
        
        post_data = {
            'acessorios-TOTAL_FORMS': '2',
            'acessorios-INITIAL_FORMS': '0',
            'acessorios-MIN_NUM_FORMS': '0',
            'acessorios-MAX_NUM_FORMS': '1000',
            
            # Mesmo acessório duas vezes
            'acessorios-0-acessorio': str(self.acessorio1.id),
            'acessorios-0-quantidade': '1',
            'acessorios-0-observacoes': '',
            'acessorios-0-DELETE': '',
            
            'acessorios-1-acessorio': str(self.acessorio1.id),
            'acessorios-1-quantidade': '2',
            'acessorios-1-observacoes': '',
            'acessorios-1-DELETE': '',
        }
        
        formset = SofaAcessorioFormSet(post_data, instance=self.sofa, prefix='acessorios')
        
        self.assertFalse(formset.is_valid())
        self.assertIn('Não é possível vincular o mesmo acessório duas vezes.', 
                     formset.non_form_errors())
        
        print("✅ Validação de duplicação funcionando corretamente")
    
    def test_quantidade_invalida(self):
        """Teste de validação para quantidade inválida"""
        print("🧪 Testando validação de quantidade inválida...")
        
        post_data = {
            'acessorios-TOTAL_FORMS': '1',
            'acessorios-INITIAL_FORMS': '0',
            'acessorios-MIN_NUM_FORMS': '0',
            'acessorios-MAX_NUM_FORMS': '1000',
            
            'acessorios-0-acessorio': str(self.acessorio1.id),
            'acessorios-0-quantidade': '0',  # Quantidade inválida
            'acessorios-0-observacoes': '',
            'acessorios-0-DELETE': '',
        }
        
        formset = SofaAcessorioFormSet(post_data, instance=self.sofa, prefix='acessorios')
        
        self.assertFalse(formset.is_valid())
        
        print("✅ Validação de quantidade funcionando corretamente")
    
    def test_unique_constraint(self):
        """Teste da constraint unique_together"""
        print("🧪 Testando constraint unique_together...")
        
        # Criar primeira vinculação
        SofaAcessorio.objects.create(
            sofa=self.sofa,
            acessorio=self.acessorio1,
            quantidade=1
        )
        
        # Tentar criar duplicata deve falhar
        with self.assertRaises(Exception):
            SofaAcessorio.objects.create(
                sofa=self.sofa,
                acessorio=self.acessorio1,
                quantidade=2
            )
        
        print("✅ Constraint unique_together funcionando corretamente")
    
    def test_validacao_modelo(self):
        """Teste das validações customizadas do modelo"""
        print("🧪 Testando validações customizadas...")
        
        # Testar acessório inativo
        acessorio_inativo = Acessorio.objects.create(
            ref_acessorio='ACC_INATIVO',
            nome='Acessório Inativo',
            ativo=False
        )
        
        vinculacao = SofaAcessorio(
            sofa=self.sofa,
            acessorio=acessorio_inativo,
            quantidade=1
        )
        
        with self.assertRaises(Exception):
            vinculacao.full_clean()
        
        print("✅ Validações customizadas funcionando corretamente")


def executar_testes():
    """Executa todos os testes"""
    print("=== EXECUTANDO TESTES DE INTEGRAÇÃO ===\n")
    
    import unittest
    
    # Criar suite de testes
    suite = unittest.TestLoader().loadTestsFromTestCase(TesteAcessoriosSofa)
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n✅ TODOS OS TESTES PASSARAM!")
        return True
    else:
        print(f"\n❌ {len(result.failures)} TESTES FALHARAM")
        print(f"❌ {len(result.errors)} ERROS ENCONTRADOS")
        return False


if __name__ == "__main__":
    sucesso = executar_testes()
    sys.exit(0 if sucesso else 1)
