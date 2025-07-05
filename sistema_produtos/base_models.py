from django.db import models

class BaseModel(models.Model):
    """
    Modelo base que inclui campos de auditoria.
    Todos os modelos devem herdar desta classe.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )

    class Meta:
        abstract = True
