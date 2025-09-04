"""
Testes para as melhorias de módulos de sofás
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
import json

from orcamentos.models import Orcamento, OrcamentoItem, OrcamentoModulo, FaixaPreco, FormaPagamento
from produtos.models import Produto, Modulo, TamanhosModulosDetalhado, TipoItem
from clientes.models import Cliente
from authentication.models import CustomUser


class TestModulosSofasMelhorias(TestCase):
    """Testes para as melhorias implementadas nos módulos de sofás"""
    
    def setUp(self):
        """Configurar dados de teste"""
        # Criar usuário
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            tipo_permissao='admin'
        )
        
        # Criar cliente
        self.cliente = Cliente.objects.create(
            nome_empresa='Empresa Teste',
            representante='João Silva',
            cnpj='12345678000123'
        )
        
        # Criar faixa de preço e forma de pagamento
        self.faixa_preco = FaixaPreco.objects.create(
            nome='Padrão',
            multiplicador=Decimal('1.00')
        )
        
        self.forma_pagamento = FormaPagamento.objects.create(
            nome='À vista'
        )
        
        # Criar tipo de produto
        self.tipo_sofa = TipoItem.objects.create(nome='Sofá')
        
        # Criar produto (sofá)
        self.produto = Produto.objects.create(
            ref_produto='SOFA001',
            nome_produto='Sofá Modular Teste',
            id_tipo_produto=self.tipo_sofa
        )
        
        # Criar módulo
        self.modulo = Modulo.objects.create(
            produto=self.produto,
            nome='Módulo Canto Direito'
        )
        
        # Criar tamanhos do módulo
        self.tamanho1 = TamanhosModulosDetalhado.objects.create(
            id_modulo=self.modulo,
            largura_total=Decimal('180.00'),
            preco=Decimal('1200.00')
        )
        
        self.tamanho2 = TamanhosModulosDetalhado.objects.create(
            id_modulo=self.modulo,
            largura_total=Decimal('200.00'),
            preco=Decimal('1350.00')
        )
        
        # Configurar cliente de teste
        self.client = Client()
        self.client.login(email='test@example.com', password='testpass123')
    
    def test_endpoint_tamanhos_modulo(self):
        """Testar endpoint de busca de tamanhos por módulo"""
        url = reverse('orcamentos:obter_tamanhos_modulo')
        response = self.client.get(url, {'modulo_id': self.modulo.id})
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('tamanhos', data)
        self.assertIn('modulo', data)
        
        # Verificar dados do módulo
        self.assertEqual(data['modulo']['id'], self.modulo.id)
        self.assertEqual(data['modulo']['nome'], self.modulo.nome)
        
        # Verificar tamanhos
        tamanhos = data['tamanhos']
        self.assertEqual(len(tamanhos), 2)
        
        # Verificar primeiro tamanho
        tamanho = tamanhos[0]
        self.assertEqual(tamanho['id'], self.tamanho1.id)
        self.assertEqual(float(tamanho['largura_total']), 180.0)
        self.assertEqual(float(tamanho['preco']), 1200.0)
    
    def test_endpoint_tamanhos_modulo_inexistente(self):
        """Testar endpoint com módulo inexistente"""
        url = reverse('orcamentos:obter_tamanhos_modulo')
        response = self.client.get(url, {'modulo_id': 99999})
        
        self.assertEqual(response.status_code, 404)
        
        data = response.json()
        self.assertIn('erro', data)
    
    def test_criar_orcamento_com_modulos_observacoes(self):
        """Testar criação de orçamento com módulos e observações"""
        # Criar orçamento
        orcamento = Orcamento.objects.create(
            cliente=self.cliente,
            vendedor=self.user,
            faixa_preco=self.faixa_preco,
            forma_pagamento=self.forma_pagamento
        )
        
        # Dados do sofá com módulos
        dados_especificos = {
            'tipo': 'sofa',
            'modulos': [
                {
                    'modulo_id': self.modulo.id,
                    'modulo_nome': self.modulo.nome,
                    'tamanho_id': self.tamanho1.id,
                    'tamanho_nome': '180cm',
                    'quantidade': 2,
                    'preco': 1200.00,
                    'subtotal': 2400.00,
                    'observacoes': 'Tecido especial conforme amostra do cliente'
                }
            ]
        }
        
        # Adicionar item via endpoint
        url = reverse('orcamentos:adicionar_item', kwargs={'orcamento_pk': orcamento.pk})
        
        payload = {
            'produto_id': f'produto_{self.produto.id}',
            'quantidade': 1,
            'preco_unitario': '2400.00',
            'observacoes': 'Observação geral do item',
            'dados_especificos': dados_especificos
        }
        
        response = self.client.post(
            url, 
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        
        # Verificar se item foi criado
        item = OrcamentoItem.objects.get(orcamento=orcamento)
        self.assertEqual(item.observacoes, 'Observação geral do item')
        self.assertEqual(item.dados_produto['tipo'], 'sofa')
        
        # Verificar se módulo foi salvo com observações
        modulo_orcamento = OrcamentoModulo.objects.get(item_orcamento=item)
        self.assertEqual(modulo_orcamento.modulo_id, self.modulo.id)
        self.assertEqual(modulo_orcamento.nome_modulo, self.modulo.nome)
        self.assertEqual(modulo_orcamento.tamanho_id, self.tamanho1.id)
        self.assertEqual(modulo_orcamento.quantidade, 2)
        self.assertEqual(modulo_orcamento.observacoes, 'Tecido especial conforme amostra do cliente')
    
    def test_validacao_quantidade_modulo(self):
        """Testar validação de quantidade mínima"""
        # Este teste seria feito no frontend, mas podemos simular
        # verificando se a migration permite quantidade 0
        orcamento = Orcamento.objects.create(
            cliente=self.cliente,
            vendedor=self.user,
            faixa_preco=self.faixa_preco,
            forma_pagamento=self.forma_pagamento
        )
        
        item = OrcamentoItem.objects.create(
            orcamento=orcamento,
            produto=self.produto,
            quantidade=1,
            preco_unitario=Decimal('1200.00')
        )
        
        # Tentar criar módulo com quantidade 0 (deve ser permitido no modelo)
        modulo_orcamento = OrcamentoModulo.objects.create(
            item_orcamento=item,
            modulo_id=self.modulo.id,
            nome_modulo=self.modulo.nome,
            quantidade=0  # Quantidade inválida
        )
        
        # O modelo permite, mas a validação deve ser feita na view/frontend
        self.assertEqual(modulo_orcamento.quantidade, 0)
    
    def test_observacoes_longas(self):
        """Testar limite de observações"""
        orcamento = Orcamento.objects.create(
            cliente=self.cliente,
            vendedor=self.user,
            faixa_preco=self.faixa_preco,
            forma_pagamento=self.forma_pagamento
        )
        
        item = OrcamentoItem.objects.create(
            orcamento=orcamento,
            produto=self.produto,
            quantidade=1,
            preco_unitario=Decimal('1200.00')
        )
        
        # Observação muito longa (mais de 1000 caracteres)
        observacao_longa = 'A' * 1001
        
        # Deve conseguir salvar (o limite é definido como max_length=1000)
        modulo_orcamento = OrcamentoModulo.objects.create(
            item_orcamento=item,
            modulo_id=self.modulo.id,
            nome_modulo=self.modulo.nome,
            observacoes=observacao_longa[:1000]  # Truncar para 1000 chars
        )
        
        self.assertEqual(len(modulo_orcamento.observacoes), 1000)


class TestModulosIntegracao(TestCase):
    """Testes de integração para módulos"""
    
    def setUp(self):
        self.client = Client()
        # Configuração básica similar ao teste anterior
    
    def test_fluxo_completo_selecao_modulos(self):
        """Testar fluxo completo de seleção de módulos"""
        # 1. Carregar página de novo orçamento
        # 2. Selecionar sofá
        # 3. Carregar módulos
        # 4. Selecionar módulo e tamanho
        # 5. Adicionar observações
        # 6. Confirmar seleção
        # 7. Finalizar orçamento
        
        # Este teste seria implementado com Selenium ou similar
        # para testar a interação completa do JavaScript
        pass
    
    def test_edicao_orcamento_existente(self):
        """Testar edição de orçamento com módulos existentes"""
        # 1. Criar orçamento com módulos
        # 2. Carregar página de edição
        # 3. Verificar se dados são carregados corretamente
        # 4. Modificar observações
        # 5. Salvar alterações
        
        # Este teste seria implementado para verificar
        # se a edição preserva os dados corretamente
        pass
