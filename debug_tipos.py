from produtos.models import TipoItem, Produto

print('=== Tipos de Item Disponíveis ===')
tipos = TipoItem.objects.all()
for tipo in tipos:
    print(f'ID: {tipo.id}, Nome: {tipo.nome}')

print('\n=== Produtos por Tipo ===')
for produto in Produto.objects.filter(ativo=True):
    print(f'Produto: {produto.nome_produto} - Tipo: {produto.id_tipo_produto}')

print('\n=== Buscar tipo Sofá ===')
tipo_sofa = TipoItem.objects.filter(nome__icontains='Sofá').first()
if tipo_sofa:
    print(f'Tipo Sofá encontrado: {tipo_sofa.nome}')
    produtos_sofa = Produto.objects.filter(id_tipo_produto=tipo_sofa, ativo=True)
    print(f'Produtos do tipo Sofá: {produtos_sofa.count()}')
    for produto in produtos_sofa:
        print(f'  - {produto.nome_produto} (ID: {produto.id})')
else:
    print('Tipo Sofá não encontrado')
