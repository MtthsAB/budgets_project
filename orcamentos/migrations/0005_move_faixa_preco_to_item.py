from django.db import migrations, models
import django.db.models.deletion


def copiar_faixa_preco_para_itens(apps, schema_editor):
    Orcamento = apps.get_model('orcamentos', 'Orcamento')
    OrcamentoItem = apps.get_model('orcamentos', 'OrcamentoItem')

    itens = OrcamentoItem.objects.filter(
        faixa_preco__isnull=True,
        orcamento__faixa_preco__isnull=False
    ).select_related('orcamento')

    for item in itens.iterator():
        item.faixa_preco_id = item.orcamento.faixa_preco_id
        item.save(update_fields=['faixa_preco'])


def reverter_copia_faixa_preco(apps, schema_editor):
    OrcamentoItem = apps.get_model('orcamentos', 'OrcamentoItem')
    OrcamentoItem.objects.update(faixa_preco=None)


class Migration(migrations.Migration):

    dependencies = [
        ('orcamentos', '0004_add_modulo_improvements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orcamento',
            name='faixa_preco',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='orcamentos.faixapreco',
                verbose_name='Faixa de Preço'
            ),
        ),
        migrations.AddField(
            model_name='orcamentoitem',
            name='faixa_preco',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='orcamentos.faixapreco',
                verbose_name='Faixa de Preço'
            ),
        ),
        migrations.RunPython(copiar_faixa_preco_para_itens, reverter_copia_faixa_preco),
    ]
