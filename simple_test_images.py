#!/usr/bin/env python3
"""
Script simples para testar se a seção de imagens aparece corretamente
"""

import requests
import re

def test_image_section():
    """Testa se a seção de imagens está presente na página"""
    try:
        # Fazer requisição para a página de cadastro
        response = requests.get('http://localhost:8000/produtos/cadastro/')
        
        print(f"Status da resposta: {response.status_code}")
        
        if response.status_code != 200:
            print("❌ Erro: Página não carregou corretamente")
            return False
        
        content = response.text
        
        # Verificar elementos essenciais
        checks = {
            'Seção de imagens presente': 'id="secao-imagens"' in content,
            'Include funcionando': 'Imagens do Produto' in content,
            'Função toggleCamposPorTipo': 'function toggleCamposPorTipo()' in content,
            'Select de tipo': 'id="tipo_produto"' in content,
            'Campo imagem principal': 'name="imagem_principal"' in content,
            'Campo imagem secundária': 'name="imagem_secundaria"' in content,
            'JavaScript para exibir seção': 'secaoImagens.style.display = \'block\'' in content,
        }
        
        print("\n=== VERIFICAÇÃO DOS ELEMENTOS ===")
        all_ok = True
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            print(f"{status} {check_name}: {'OK' if result else 'FALTANDO'}")
            if not result:
                all_ok = False
        
        # Extrair e mostrar a linha relevante da função JavaScript
        pattern = r'secaoImagens\.style\.display = [\'"]([^\'"]*)[\'"]'
        matches = re.findall(pattern, content)
        if matches:
            print(f"\n=== CONTROLE DE EXIBIÇÃO ENCONTRADO ===")
            for match in matches:
                print(f"- secaoImagens.style.display = '{match}'")
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Erro ao testar: {e}")
        return False

if __name__ == '__main__':
    print("🔍 Testando visibilidade da seção de imagens...")
    
    result = test_image_section()
    
    if result:
        print("\n✅ TESTE PASSOU: Elementos básicos estão presentes!")
    else:
        print("\n❌ TESTE FALHOU: Alguns elementos estão faltando!")
