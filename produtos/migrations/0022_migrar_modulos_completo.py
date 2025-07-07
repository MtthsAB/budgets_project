# Generated manually on 2025-07-07

from django.db import migrations, models
import django.db.models.deletion


def migrar_modulos_referencias(apps, schema_editor):
    """
    Migra as referências dos módulos de Item para Produto
    """
    # Usar raw SQL para evitar problemas de constraints
    with schema_editor.connection.cursor() as cursor:
        print("=== MIGRANDO REFERÊNCIAS DOS MÓDULOS ===")
        
        # Verificar dados antes da migração
        cursor.execute("SELECT COUNT(*) FROM produtos_modulo WHERE item_id = 14")
        modulos_para_migrar = cursor.fetchone()[0]
        print(f"Módulos a migrar: {modulos_para_migrar}")
        
        if modulos_para_migrar > 0:
            # Remover constraint temporariamente
            try:
                cursor.execute("ALTER TABLE produtos_modulo DROP CONSTRAINT IF EXISTS produtos_modulo_item_id_ad6e73a6_fk_produtos_item_id")
                print("✓ Constraint removida temporariamente")
            except Exception as e:
                print(f"Constraint não encontrada ou já removida: {e}")
            
            # Atualizar referências
            cursor.execute("UPDATE produtos_modulo SET item_id = 7 WHERE item_id = 14")
            print(f"✓ {cursor.rowcount} módulos atualizados")
            
            # Verificar resultado
            cursor.execute("SELECT COUNT(*) FROM produtos_modulo WHERE item_id = 7")
            modulos_migrados = cursor.fetchone()[0]
            print(f"✓ Total de módulos após migração: {modulos_migrados}")


def reverter_migracao(apps, schema_editor):
    """Reverter não é seguro"""
    print("Reversão não implementada - dados já foram migrados")


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0021_add_produto_model'),
    ]

    operations = [
        # Primeiro executar a migração de dados
        migrations.RunPython(migrar_modulos_referencias, reverter_migracao),
        
        # Depois alterar o campo com a nova referência
        migrations.AlterField(
            model_name='modulo',
            name='item',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, 
                related_name='modulos', 
                to='produtos.produto', 
                verbose_name='Produto'
            ),
        ),
    ]
