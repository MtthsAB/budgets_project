"""
Nova view de edição de sofás usando formsets hierárquicos.
"""

import logging
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from produtos.models import Produto, TipoItem, Modulo, TamanhosModulosDetalhado
from produtos.forms import SofaForm, ModuloFormSet, TamanhoFormSet
from authentication.decorators import produtos_access_required
from sistema_produtos.mixins import track_user_changes

logger = logging.getLogger(__name__)


@produtos_access_required
def sofa_editar_formset_view(request, sofa_id):
    """
    Nova view para edição de sofás usando formsets hierárquicos.
    
    Esta view substitui a anterior que deletava todos os módulos,
    implementando edição com upsert correto usando formsets do Django.
    """
    sofa = get_object_or_404(Produto, id=sofa_id, id_tipo_produto__nome__icontains='sofá')
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # 1. Formulário principal do sofá
                sofa_form = SofaForm(request.POST, request.FILES, instance=sofa)
                
                # 2. Formset de módulos
                modulo_formset = ModuloFormSet(request.POST, request.FILES, instance=sofa)
                
                # 3. Coletar formsets de tamanhos para cada módulo
                tamanho_formsets = []
                modulos_data = []
                
                # Processar dados dos módulos para preparar formsets de tamanhos
                management_form = modulo_formset.management_form
                total_forms = int(management_form.cleaned_data['TOTAL_FORMS'])
                
                logger.info(f"=== PROCESSANDO EDIÇÃO DO SOFÁ {sofa_id} ===")
                logger.info(f"Total de forms de módulos: {total_forms}")
                
                for i in range(total_forms):
                    prefix = f'{modulo_formset.prefix}-{i}'
                    
                    # Verificar se este form deve ser deletado
                    delete_field = f'{prefix}-DELETE'
                    if request.POST.get(delete_field) == 'on':
                        logger.info(f"Módulo {i} marcado para deleção")
                        continue
                    
                    # Verificar se tem ID (módulo existente)
                    modulo_id_field = f'{prefix}-id'
                    modulo_id = request.POST.get(modulo_id_field)
                    
                    if modulo_id:
                        # Módulo existente
                        try:
                            modulo = Modulo.objects.get(id=modulo_id, produto=sofa)
                            logger.info(f"Módulo existente encontrado: {modulo.nome} (ID: {modulo_id})")
                        except Modulo.DoesNotExist:
                            logger.warning(f"Módulo ID {modulo_id} não encontrado, será tratado como novo")
                            modulo = None
                    else:
                        # Módulo novo
                        modulo = None
                        logger.info(f"Novo módulo detectado no índice {i}")
                    
                    # Criar formset de tamanhos para este módulo
                    tamanho_prefix = f'modulo-{i}-tamanho'
                    tamanho_formset = TamanhoFormSet(
                        request.POST, 
                        instance=modulo,
                        prefix=tamanho_prefix
                    )
                    
                    tamanho_formsets.append(tamanho_formset)
                    modulos_data.append({
                        'index': i,
                        'modulo': modulo,
                        'prefix': prefix,
                        'tamanho_formset': tamanho_formset,
                        'tamanho_prefix': tamanho_prefix
                    })
                
                # 4. Validar todos os formulários
                sofa_valid = sofa_form.is_valid()
                modulo_valid = modulo_formset.is_valid()
                tamanhos_valid = all(tf.is_valid() for tf in tamanho_formsets)
                
                logger.info(f"Validações: Sofá={sofa_valid}, Módulos={modulo_valid}, Tamanhos={tamanhos_valid}")
                
                if sofa_valid and modulo_valid and tamanhos_valid:
                    # 5. Salvar sofá
                    sofa = sofa_form.save(commit=False)
                    track_user_changes(sofa, request.user)
                    sofa.save()
                    logger.info(f"✅ Sofá atualizado: {sofa.ref_produto}")
                    
                    # 6. Salvar módulos (formset já faz upsert automático)
                    modulos_salvos = modulo_formset.save(commit=False)
                    
                    # Adicionar tracking para módulos novos
                    for modulo in modulos_salvos:
                        if not modulo.pk:  # Novo módulo
                            track_user_changes(modulo, request.user)
                        else:  # Módulo existente
                            track_user_changes(modulo, request.user)
                        modulo.save()
                    
                    # Processar deleções de módulos
                    for modulo_deletado in modulo_formset.deleted_objects:
                        logger.info(f"🗑️ Deletando módulo: {modulo_deletado.nome}")
                        modulo_deletado.delete()
                    
                    logger.info(f"✅ {len(modulos_salvos)} módulos processados")
                    
                    # 7. Salvar tamanhos para cada módulo
                    for i, data in enumerate(modulos_data):
                        tamanho_formset = data['tamanho_formset']
                        modulo = data['modulo']
                        
                        # Se o módulo é novo, precisamos associar aos tamanhos
                        if not modulo and i < len(modulos_salvos):
                            modulo = modulos_salvos[i]
                            tamanho_formset.instance = modulo
                        
                        if modulo:
                            tamanhos_salvos = tamanho_formset.save(commit=False)
                            
                            for tamanho in tamanhos_salvos:
                                if not tamanho.pk:  # Novo tamanho
                                    track_user_changes(tamanho, request.user)
                                else:  # Tamanho existente
                                    track_user_changes(tamanho, request.user)
                                tamanho.id_modulo = modulo
                                tamanho.save()
                            
                            # Processar deleções de tamanhos
                            for tamanho_deletado in tamanho_formset.deleted_objects:
                                logger.info(f"🗑️ Deletando tamanho: {tamanho_deletado}")
                                tamanho_deletado.delete()
                            
                            logger.info(f"✅ {len(tamanhos_salvos)} tamanhos processados para módulo {modulo.nome}")
                    
                    messages.success(request, f'Sofá "{sofa.ref_produto} - {sofa.nome_produto}" atualizado com sucesso!')
                    return redirect('sofa_detalhes', sofa_id=sofa.id)
                
                else:
                    # Exibir erros
                    if not sofa_valid:
                        logger.error(f"Erros no formulário do sofá: {sofa_form.errors}")
                        for field, errors in sofa_form.errors.items():
                            for error in errors:
                                messages.error(request, f"Erro no campo {field}: {error}")
                    
                    if not modulo_valid:
                        logger.error(f"Erros no formset de módulos: {modulo_formset.errors}")
                        messages.error(request, f"Erro nos módulos: {modulo_formset.non_form_errors()}")
                    
                    if not tamanhos_valid:
                        for i, tf in enumerate(tamanho_formsets):
                            if tf.errors:
                                logger.error(f"Erros no formset de tamanhos {i}: {tf.errors}")
                                messages.error(request, f"Erro nos tamanhos do módulo {i+1}: {tf.non_form_errors()}")
        
        except Exception as e:
            logger.error(f"Erro na edição do sofá {sofa_id}: {str(e)}", exc_info=True)
            messages.error(request, f'Erro ao editar sofá: {str(e)}')
    
    # GET - Preparar formulários
    sofa_form = SofaForm(instance=sofa)
    modulo_formset = ModuloFormSet(instance=sofa)
    
    # Preparar formsets de tamanhos para módulos existentes
    tamanho_formsets_data = []
    for i, modulo in enumerate(sofa.modulos.all()):
        tamanho_formset = TamanhoFormSet(
            instance=modulo,
            prefix=f'modulo-{i}-tamanho'
        )
        tamanho_formsets_data.append({
            'modulo': modulo,
            'formset': tamanho_formset,
            'index': i
        })
    
    context = {
        'sofa': sofa,
        'sofa_form': sofa_form,
        'modulo_formset': modulo_formset,
        'tamanho_formsets_data': tamanho_formsets_data,
        'tipos': TipoItem.objects.all(),
        'eh_edicao': True,
        'produto_id': sofa.id,
        'timestamp': int(time.time())  # Cache busting para Edge
    }
    
    return render(request, 'produtos/sofas/editar_formsets.html', context)
