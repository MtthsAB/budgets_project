from django.db import models
from django.conf import settings

class UserTrackingMixin:
    """
    Mixin para automaticamente rastrear usuários em criação e edição
    """
    
    def save_with_user(self, user=None, *args, **kwargs):
        """
        Salva o objeto definindo automaticamente created_by e updated_by
        """
        if user and hasattr(user, 'id') and user.id:
            if not self.pk:  # Novo objeto
                self.created_by = user
            self.updated_by = user
        elif not user or user.is_anonymous:
            # Para usuários anônimos ou None, usar "Sistema"
            if not self.pk:
                self.created_by = None
            self.updated_by = None
        
        return self.save(*args, **kwargs)

    def get_created_by_display(self):
        """Retorna nome amigável do criador"""
        if self.created_by:
            return self.created_by.get_full_name() or self.created_by.email
        return "Sistema"
    
    def get_updated_by_display(self):
        """Retorna nome amigável do último editor"""
        if self.updated_by:
            return self.updated_by.get_full_name() or self.updated_by.email
        return "Sistema"


class BootstrapValidationMixin:
    """
    Mixin para formulários Django que adiciona automaticamente a classe 'is-invalid' 
    do Bootstrap 5 aos campos com erros de validação.
    
    Uso:
        class MeuForm(BootstrapValidationMixin, forms.ModelForm):
            ...
            
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                # Seu código aqui (opcional)
                self.add_invalid_classes()  # Chamar no final do __init__
    """
    
    def add_invalid_classes(self):
        """Adiciona classe is-invalid aos campos com erro"""
        if self.errors:
            for field_name in self.errors:
                if field_name in self.fields:
                    existing_classes = self.fields[field_name].widget.attrs.get('class', '')
                    if 'is-invalid' not in existing_classes:
                        self.fields[field_name].widget.attrs['class'] = f'{existing_classes} is-invalid'.strip()


# Mixin para modelos que já herdam de BaseModel
def track_user_changes(model_instance, user):
    """
    Função utilitária para definir campos de usuário em qualquer modelo
    que tenha created_by e updated_by
    """
    if hasattr(model_instance, 'created_by') and hasattr(model_instance, 'updated_by'):
        if user and hasattr(user, 'id') and user.id and not user.is_anonymous:
            if not model_instance.pk:  # Novo objeto
                model_instance.created_by = user
            model_instance.updated_by = user
        else:
            # Para casos onde não há usuário válido
            if not model_instance.pk:
                model_instance.created_by = None
            model_instance.updated_by = None
    return model_instance
