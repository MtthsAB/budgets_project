#!/usr/bin/env python
import os
import sys
import django
from datetime import timedelta
from django.utils import timezone

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.forms import OrcamentoForm

def teste_final_correcao():
    """Teste final após a correção do formato das datas"""
    
    print("🔧 TESTE FINAL APÓS CORREÇÃO DO FORMATO")
    print("=" * 50)
    
    # Simular exatamente o que a view faz
    hoje = timezone.now().date()
    data_entrega = hoje + timedelta(days=30)
    data_validade = hoje + timedelta(days=15)
    
    inicial_data = {
        'data_entrega': data_entrega,
        'data_validade': data_validade,
        'status': 'rascunho'
    }
    
    form = OrcamentoForm(initial=inicial_data)
    
    print(f"📅 Data atual: {hoje}")
    print(f"📅 Data de entrega: {data_entrega}")
    print(f"📅 Data de validade: {data_validade}")
    print()
    
    print("🔍 HTML GERADO:")
    html_validade = str(form['data_validade'])
    html_entrega = str(form['data_entrega'])
    
    print("Data de Validade:")
    print(f"  {html_validade}")
    print()
    print("Data de Entrega:")
    print(f"  {html_entrega}")
    print()
    
    # Extrair valores do HTML
    import re
    valor_validade = re.search(r'value="([^"]*)"', html_validade)
    valor_entrega = re.search(r'value="([^"]*)"', html_entrega)
    
    print("✅ VERIFICAÇÃO:")
    if valor_validade and valor_entrega:
        val_val = valor_validade.group(1)
        val_ent = valor_entrega.group(1)
        
        print(f"  - Valor data validade: {val_val}")
        print(f"  - Valor data entrega: {val_ent}")
        
        # Verificar formato YYYY-MM-DD
        formato_correto_val = re.match(r'^\d{4}-\d{2}-\d{2}$', val_val)
        formato_correto_ent = re.match(r'^\d{4}-\d{2}-\d{2}$', val_ent)
        
        print(f"  - Formato validade correto: {'✅' if formato_correto_val else '❌'}")
        print(f"  - Formato entrega correto: {'✅' if formato_correto_ent else '❌'}")
        
        if formato_correto_val and formato_correto_ent:
            print("\n🎉 SUCESSO TOTAL!")
            print("   - Os campos estão sendo preenchidos automaticamente")
            print("   - O formato das datas está correto (YYYY-MM-DD)")
            print("   - O navegador deve mostrar as datas corretamente")
            return True
        else:
            print("\n❌ PROBLEMA NO FORMATO")
            return False
    else:
        print("  ❌ Não foi possível extrair valores do HTML")
        return False

if __name__ == '__main__':
    sucesso = teste_final_correcao()
    
    print("\n" + "=" * 50)
    if sucesso:
        print("🚀 IMPLEMENTAÇÃO FINALIZADA COM SUCESSO!")
        print("   Agora recarregue a página no navegador para ver o resultado.")
    else:
        print("⚠️  Ainda há problemas a serem resolvidos.")
    print("=" * 50)
