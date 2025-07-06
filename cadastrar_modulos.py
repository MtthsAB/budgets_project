import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, Modulo, TamanhosModulosDetalhado

def main():
    # Buscar o produto BIG BOSS
    big_boss = Item.objects.get(ref_produto='SF982')
    print(f"✓ Produto encontrado: {big_boss.nome_produto}")

    # MOD 02 1LUGAR S/BR
    print("\n📦 Criando MOD 02 1LUGAR S/BR...")
    mod02, created = Modulo.objects.get_or_create(
        item=big_boss,
        nome='MOD 02 1LUGAR S/BR',
        defaults={
            'profundidade': Decimal('110.00'),
            'altura': Decimal('37.00'),
            'braco': Decimal('25.00'),
            'descricao': 'Com opção de automação\nProfundidade: 125 cm (aberto)'
        }
    )
    print(f"{'✨ Criado' if created else '✓ Já existe'}: {mod02.nome}")

    # Tamanhos do MOD 02
    tamanhos_mod02 = [
        (120, 120, 7.2, 1.4, 45, 2659),
        (110, 110, 6.8, 1.3, 43, 2501),
        (100, 100, 5.8, 1.2, 41, 2353),
        (90, 90, 5.4, 1.1, 39, 2212)
    ]

    for lt, la, tm, vm, pk, pr in tamanhos_mod02:
        tamanho, created = TamanhosModulosDetalhado.objects.get_or_create(
            id_modulo=mod02,
            largura_total=Decimal(str(lt)),
            largura_assento=Decimal(str(la)),
            defaults={
                'tecido_metros': Decimal(str(tm)),
                'volume_m3': Decimal(str(vm)),
                'peso_kg': Decimal(str(pk)),
                'preco': Decimal(str(pr))
            }
        )
        print(f"   {'✨' if created else '✓'} {lt}x{la}cm - R${pr}")

    # MOD 03 CHAISE
    print("\n📦 Criando MOD 03 CHAISE...")
    mod03, created = Modulo.objects.get_or_create(
        item=big_boss,
        nome='MOD 03 CHAISE',
        defaults={
            'profundidade': Decimal('157.00'),
            'altura': Decimal('37.00'),
            'braco': Decimal('25.00'),
            'descricao': 'Com opção de automação\nProfundidade: 172 cm (aberto)'
        }
    )
    print(f"{'✨ Criado' if created else '✓ Já existe'}: {mod03.nome}")

    # Tamanhos do MOD 03
    tamanhos_mod03 = [
        (145, 120, 9.0, 2.3, 70, 3575),
        (135, 110, 8.6, 2.2, 68, 3363),
        (125, 100, 8.4, 2.1, 65, 3163),
        (115, 90, 7.7, 2.0, 60, 2974)
    ]

    for lt, la, tm, vm, pk, pr in tamanhos_mod03:
        tamanho, created = TamanhosModulosDetalhado.objects.get_or_create(
            id_modulo=mod03,
            largura_total=Decimal(str(lt)),
            largura_assento=Decimal(str(la)),
            defaults={
                'tecido_metros': Decimal(str(tm)),
                'volume_m3': Decimal(str(vm)),
                'peso_kg': Decimal(str(pk)),
                'preco': Decimal(str(pr))
            }
        )
        print(f"   {'✨' if created else '✓'} {lt}x{la}cm - R${pr}")

    # MOD 05 AUXILIAR
    print("\n📦 Criando MOD 05 AUXILIAR...")
    mod05, created = Modulo.objects.get_or_create(
        item=big_boss,
        nome='MOD 05 AUXILIAR',
        defaults={
            'profundidade': Decimal('107.00'),
            'altura': Decimal('45.00'),
            'braco': None,
            'descricao': 'Acessórios Opcionais:\nTorre Usb\nLuminária\nCarregador Indução'
        }
    )
    print(f"{'✨ Criado' if created else '✓ Já existe'}: {mod05.nome}")

    # Tamanho do MOD 05 (apenas um)
    tamanho, created = TamanhosModulosDetalhado.objects.get_or_create(
        id_modulo=mod05,
        largura_total=Decimal('44.00'),
        largura_assento=Decimal('107.00'),
        defaults={
            'tecido_metros': Decimal('2.3'),
            'volume_m3': Decimal('0.6'),
            'peso_kg': Decimal('30.00'),
            'preco': Decimal('1169.00')
        }
    )
    print(f"   {'✨' if created else '✓'} 44x107cm - R$1169")

    # MOD 06 PUFE
    print("\n📦 Criando MOD 06 PUFE...")
    mod06, created = Modulo.objects.get_or_create(
        item=big_boss,
        nome='MOD 06 PUFE',
        defaults={
            'profundidade': Decimal('63.00'),
            'altura': Decimal('45.00'),
            'braco': None,
            'descricao': ''
        }
    )
    print(f"{'✨ Criado' if created else '✓ Já existe'}: {mod06.nome}")

    # Tamanhos do MOD 06
    tamanhos_mod06 = [
        (120, 63, 3.0, 0.6, 35, 1164),
        (110, 63, 2.8, 0.5, 33, 1095),
        (100, 63, 2.5, 0.4, 30, 1029),
        (90, 63, 2.3, 0.3, 28, 968)
    ]

    for lt, la, tm, vm, pk, pr in tamanhos_mod06:
        tamanho, created = TamanhosModulosDetalhado.objects.get_or_create(
            id_modulo=mod06,
            largura_total=Decimal(str(lt)),
            largura_assento=Decimal(str(la)),
            defaults={
                'tecido_metros': Decimal(str(tm)),
                'volume_m3': Decimal(str(vm)),
                'peso_kg': Decimal(str(pk)),
                'preco': Decimal(str(pr))
            }
        )
        print(f"   {'✨' if created else '✓'} {lt}x{la}cm - R${pr}")

    # Resumo final
    print("\n🎉 CADASTRO CONCLUÍDO!")
    print("=" * 50)
    modulos = Modulo.objects.filter(item=big_boss)
    print(f"📦 Total de módulos: {modulos.count()}")
    
    for modulo in modulos:
        count = TamanhosModulosDetalhado.objects.filter(id_modulo=modulo).count()
        print(f"   • {modulo.nome}: {count} variações")
    
    total_tamanhos = TamanhosModulosDetalhado.objects.filter(id_modulo__item=big_boss).count()
    print(f"📏 Total de variações: {total_tamanhos}")

if __name__ == '__main__':
    main()
