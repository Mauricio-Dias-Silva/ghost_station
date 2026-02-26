# core/views.py — Ghost Station Views (Refatorado)

import json
import threading
from django.shortcuts import render, get_object_or_404, redirect
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Evidencia, SessaoInvestigacao, SessaoEVP, RegistroEVP, RegistroSintese
from django.utils import timezone
from django.db.models import Max


def _get_camera():
    """Lazy-load da câmera — só instancia quando precisar."""
    from .camera import VideoCamera
    return VideoCamera()


def dashboard(request):
    """Dashboard principal com sessão ativa e evidências."""
    sessao_ativa = SessaoInvestigacao.objects.filter(status='ativa').first()
    evidencias = Evidencia.objects.all().order_by('-data_captura')[:10]
    registros_sintese = RegistroSintese.objects.all().order_by('-data_sessao')[:5]

    # Stats
    total_evidencias = Evidencia.objects.count()
    score_max_obj = Evidencia.objects.aggregate(Max('score_coincidencia'))['score_coincidencia__max']
    score_max = score_max_obj if score_max_obj is not None else 0
    sessoes_total = SessaoInvestigacao.objects.count()

    return render(request, 'core/dashboard.html', {
        'evidencias': evidencias,
        'sessao_ativa': sessao_ativa,
        'total_evidencias': total_evidencias,
        'score_max': score_max,
        'sessoes_total': sessoes_total,
        'registros_sintese': registros_sintese,
        'audio_url': "http://10.93.175.172:8080/audio.wav", # Added from user's snippet
    })


@csrf_exempt
@require_POST
def gatilho_anomalia(request):
    """API que recebe o alerta do celular — salva evidência."""
    try:
        dados = json.loads(request.body)
        audio = dados.get('audio_level', 0)
        mag = dados.get('magnetic_delta', 0)
        origem = dados.get('origem_disparo', 'desconhecido')
        lat = dados.get('latitude')
        lon = dados.get('longitude')

        # Pegar sessão ativa
        sessao = SessaoInvestigacao.objects.filter(status='ativa').first()

        cam = _get_camera()
        resultado = cam.processar_anomalia_unica(
            audio_level=audio,
            mag_level=mag,
            origem=origem,
            lat=lat,
            lon=lon,
            sessao=sessao,
        )

        if resultado['sucesso']:
            # Atualizar stats da sessão
            if sessao:
                sessao.total_anomalias = sessao.evidencias.count()
                sessao.score_maximo = max(sessao.score_maximo, resultado.get('score', 0))
                sessao.save()

            # AI Analysis (async-like, in thread)
            import threading
            from .services.ia_analyzer import analisar_evidencia_async
            ev_id = resultado.get('id')
            if ev_id:
                threading.Thread(
                    target=analisar_evidencia_async,
                    args=(ev_id,),
                    daemon=True
                ).start()

            return JsonResponse({
                'status': 'capturado',
                'url': resultado['url'],
                'id': resultado.get('id'),
                'score': resultado.get('score', 1),
                'tipo': resultado.get('tipo', 'visual'),
            })
        else:
            return JsonResponse({
                'status': 'ignorado',
                'motivo': resultado.get('motivo', 'Sem validação visual')
            })
    except Exception as e:
        return JsonResponse({'status': 'erro', 'msg': str(e)}, status=500)


@csrf_exempt
@require_POST
def iniciar_sessao(request):
    """Cria uma nova sessão de investigação."""
    try:
        dados = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        dados = {}

    titulo = dados.get('titulo', f'Investigação {timezone.now().strftime("%d/%m %H:%M")}')
    local = dados.get('local', '')
    lat = dados.get('latitude')
    lon = dados.get('longitude')

    # Encerrar sessões anteriores
    SessaoInvestigacao.objects.filter(status='ativa').update(
        status='encerrada', data_fim=timezone.now()
    )

    sessao = SessaoInvestigacao.objects.create(
        titulo=titulo, local=local, latitude=lat, longitude=lon
    )
    return JsonResponse({
        'status': 'ok',
        'sessao_id': sessao.id,
        'titulo': sessao.titulo,
    })


@csrf_exempt
@require_POST
def encerrar_sessao(request):
    """Encerra a sessão ativa."""
    sessao = SessaoInvestigacao.objects.filter(status='ativa').first()
    if sessao:
        sessao.encerrar()
        return JsonResponse({
            'status': 'encerrada',
            'total_anomalias': sessao.total_anomalias,
            'score_maximo': sessao.score_maximo,
        })
    return JsonResponse({'status': 'sem_sessao'})


def api_evidencias(request):
    """Retorna últimas evidências em JSON (para polling do dashboard)."""
    evidencias = Evidencia.objects.all().order_by('-data_captura')[:10]
    data = [{
        'id': e.id,
        'url': e.imagem_url,
        'tipo': e.get_tipo_display(),
        'score': e.score_coincidencia,
        'audio': e.nivel_audio_db,
        'mag': e.variacao_magnetica,
        'data': e.data_captura.strftime('%H:%M:%S'),
        'nivel': e.nivel_perigo,
        'ia': e.ia_classificacao or '',
        'origem': e.origem_disparo,
        'dimensao': e.dimensao_estimada,
        'fusao': e.fusao_dados
    } for e in evidencias]
    return JsonResponse({'evidencias': data})


def api_status(request):
    """Status do sistema em JSON."""
    cam = _get_camera()
    sessao = SessaoInvestigacao.objects.filter(status='ativa').first()
    return JsonResponse({
        'camera': cam.is_connected,
        'sessao': {
            'id': sessao.id,
            'titulo': sessao.titulo,
            'anomalias': sessao.total_anomalias,
            'score_max': sessao.score_maximo,
            'duracao': str(sessao.duracao).split('.')[0],
        } if sessao else None,
        'total_evidencias': Evidencia.objects.count(),
    })


# Feed de Vídeo (Streaming MJPEG)
def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
    cam = _get_camera()
    return StreamingHttpResponse(
        gen(cam),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


def mobile_scanner(request):
    return render(request, 'core/mobile_scanner.html')


# ============================================================
# EVP CONSOLE
# ============================================================

def evp_console(request):
    """Renderiza o EVP Console."""
    sessao_evp = SessaoEVP.objects.filter(status='ativa').first()
    ultimos_registros = RegistroEVP.objects.order_by('-data_captura')[:20]
    total_anomalias = RegistroEVP.objects.filter(e_anomalia=True).count()
    total_registros = RegistroEVP.objects.count()
    return render(request, 'core/evp_console.html', {
        'sessao_evp': sessao_evp,
        'ultimos_registros': ultimos_registros,
        'total_anomalias': total_anomalias,
        'total_registros': total_registros,
    })


@csrf_exempt
@require_POST
def api_iniciar_sessao_evp(request):
    """Inicia uma nova sessão EVP."""
    try:
        dados = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        dados = {}

    # Encerrar sessões EVP ativas
    SessaoEVP.objects.filter(status='ativa').update(
        status='encerrada', data_fim=timezone.now()
    )
    titulo = dados.get('titulo', f'EVP {timezone.now().strftime("%d/%m %H:%M")}')
    sessao_inv_id = dados.get('sessao_investigacao_id')
    sessao_inv = None
    if sessao_inv_id:
        sessao_inv = SessaoInvestigacao.objects.filter(id=sessao_inv_id).first()

    sessao = SessaoEVP.objects.create(
        titulo=titulo,
        sessao_investigacao=sessao_inv,
        local=dados.get('local', '')
    )
    return JsonResponse({'status': 'ok', 'sessao_id': sessao.id, 'titulo': sessao.titulo})


@csrf_exempt
@require_POST
def api_encerrar_sessao_evp(request):
    """Encerra a sessão EVP ativa."""
    sessao = SessaoEVP.objects.filter(status='ativa').first()
    if sessao:
        sessao.encerrar()
        return JsonResponse({
            'status': 'encerrada',
            'total_capturas': sessao.total_capturas,
            'total_anomalias': sessao.total_anomalias,
        })
    return JsonResponse({'status': 'sem_sessao'})


@csrf_exempt
@require_POST
def api_evp_analisar(request):
    """
    Recebe dados de áudio do browser:
    { transcricao, frequencias_anomalas[], nivel_audio, magnetico, sessao_id }
    Cria RegistroEVP e inicia análise IA em background.
    """
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'erro', 'msg': 'JSON inválido'}, status=400)

    transcricao = dados.get('transcricao', '')
    frequencias = dados.get('frequencias_anomalas', [])
    nivel_audio = float(dados.get('nivel_audio', 0))
    magnetico = float(dados.get('magnetico', 0))
    freq_dominante = dados.get('frequencia_dominante')
    sessao_id = dados.get('sessao_id')

    sessao = None
    if sessao_id:
        sessao = SessaoEVP.objects.filter(id=sessao_id).first()
    if not sessao:
        sessao = SessaoEVP.objects.filter(status='ativa').first()

    # Criar registro
    registro = RegistroEVP.objects.create(
        sessao=sessao,
        transcricao=transcricao,
        frequencias_anomalas=frequencias,
        nivel_audio=nivel_audio,
        variacao_magnetica=magnetico,
        frequencia_dominante=freq_dominante,
    )

    # Rodar análise IA em background
    from .services.evp_analyzer import analisar_evp_e_salvar
    threading.Thread(
        target=analisar_evp_e_salvar,
        args=(registro.id,),
        daemon=True
    ).start()

    return JsonResponse({
        'status': 'registrado',
        'registro_id': registro.id,
        'mensagem': 'Análise IA em processamento...',
    })


def api_evp_registros(request):
    """GET: retorna os últimos registros EVP em JSON (para polling)."""
    registros = RegistroEVP.objects.order_by('-data_captura')[:20]
    data = [{
        'id': r.id,
        'data': r.data_captura.strftime('%H:%M:%S'),
        'transcricao': r.transcricao,
        'classificacao': r.get_classificacao_ia_display(),
        'classificacao_key': r.classificacao_ia,
        'e_anomalia': r.e_anomalia,
        'nota': r.nota_paranormal,
        'nivel_alerta': r.nivel_alerta,
        'mensagem': r.mensagem_detectada,
        'analise': r.analise_ia,
        'confianca': r.confianca_ia,
        'frequencias': r.frequencias_anomalas,
        'nivel_audio': r.nivel_audio,
    } for r in registros]
    return JsonResponse({'registros': data})


def api_evp_status(request):
    """GET: retorna o status da sessão EVP ativa."""
    sessao = SessaoEVP.objects.filter(status='ativa').first()
    return JsonResponse({
        'sessao': {
            'id': sessao.id,
            'titulo': sessao.titulo,
            'capturas': sessao.total_capturas,
            'anomalias': sessao.total_anomalias,
            'duracao': str(sessao.duracao).split('.')[0],
        } if sessao else None,
        'total_registros': RegistroEVP.objects.count(),
        'total_anomalias': RegistroEVP.objects.filter(e_anomalia=True).count(),
    })


# ============================================================
# ITC VISUAL CONSOLE (Fase 3)
# ============================================================

def dashboard(request):
    """Página inicial com visão geral do sistema."""
    return render(request, 'core/dashboard.html')

def blueprint_view(request):
    """Página técnica detalhando a arquitetura e nível do sistema."""
    return render(request, 'core/blueprints.html')


def itc_console(request):
    """Página principal do ITC Visual (Módulo Câmera/Pareidolia)."""
    return render(request, 'core/itc_console.html', {})


def gen_itc(camera):
    while True:
        frame, _ = camera.get_itc_frame()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def itc_video_feed(request):
    """Streaming MJPEG dos frames filtrados (Alto Contraste / Canny)."""
    cam = _get_camera()
    return StreamingHttpResponse(
        gen_itc(cam),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


@csrf_exempt
@require_POST
def api_itc_analisar(request):
    """
    Acionado pelo frontend (via timer/motion threshold).
    Captura o frame atual modificado, envia pro Gemini Vision.
    Se detectar anomalia visual, salva como banco/arquivo.
    """
    cam = _get_camera()
    if not cam.is_connected:
        return JsonResponse({'status': 'erro', 'msg': 'Câmera não conectada'})

    jpeg_bytes, motion_score = cam.get_itc_frame()
    if not jpeg_bytes:
        return JsonResponse({'status': 'erro', 'msg': 'Falha ao ler frame'})

    from .services.itc_analyzer import analisar_frame_itc
    import os, uuid
    from django.conf import settings

    # Análise pesada na IA
    resultado = analisar_frame_itc(jpeg_bytes)

    # Tentar Fusão de Dados (Aura Fusion Core)
    # Buscamos se houve um registro EVP capturado nos últimos 10 segundos
    from django.utils import timezone
    from datetime import timedelta
    agora = timezone.now()
    ultimo_evp = RegistroEVP.objects.filter(data_captura__gte=agora - timedelta(seconds=10)).last()
    
    fusao = None
    if ultimo_evp:
        from .services.aura_brain import correlacionar_eventos
        # Simulando o objeto de resultado pois o modelo RegistroEVP guarda os campos direto
        evp_data = {
            'e_anomalia': ultimo_evp.e_anomalia,
            'confianca': ultimo_evp.confianca_ia,
            'classificacao': ultimo_evp.classificacao_ia,
            'nota_paranormal': ultimo_evp.nota_paranormal
        }
        fusao = correlacionar_eventos(evp_data, resultado)

    url_final = None
    nova_evidencia = False

    # Condição para salvar: IA viu pareidolia ou tem alta confiança de forma anômala
    if resultado.get('pareidolia_detectada') or resultado.get('confianca', 0.0) >= 60.0:
        filename = f"ITC_{uuid.uuid4().hex[:8]}.jpg"
        path = os.path.join(settings.MEDIA_ROOT, 'evidencias')
        os.makedirs(path, exist_ok=True)
        full_path = os.path.join(path, filename)
        
        with open(full_path, 'wb') as f:
            f.write(jpeg_bytes)
        url_final = f"/media/evidencias/{filename}"

        sessao = SessaoInvestigacao.objects.filter(status='ativa').first()
        evidencia = Evidencia.objects.create(
            sessao=sessao,
            imagem_url=url_final,
            tipo='multipla' if fusao and fusao.get('sincronia') else 'visual',
            origem_disparo='ITC_AUTO' if not request.body else 'ITC_MANUAL',
            analise_ia=resultado.get('decodificacao', ''),
            ia_classificacao=resultado.get('classificacao', 'Anomalia ITC'),
            ia_confianca=resultado.get('confianca', 0.0),
            nivel_perigo=3 if resultado.get('pareidolia_detectada') else 1,
            dimensao_estimada=resultado.get('dimensao_estimada', '3D'),
            fusao_dados=fusao,
            obs_bpm=resultado.get('obs_bpm', 0), # Added obs_bpm
            obs_stress=resultado.get('obs_stress', 0), # Added obs_stress
        )
        nova_evidencia = True

    return JsonResponse({
        'status': 'analisado',
        'resultado': resultado,
        'fusao': fusao,
        'evidencia_url': url_final,
        'nova_evidencia': nova_evidencia
    })
def video_call(request):
    """Interface de chamada de vídeo multidimensional (Fase 5)."""
    sessao = SessaoInvestigacao.objects.filter(status='ativa').first()
    return render(request, 'core/video_call.html', {
        'sessao_ativa': sessao,
    })


def gen_aura_synth(camera):
    """Gerador que aplica o Aura Render em tempo real baseado no estado dinâmico."""
    from .services.aura_render import renderizar_presenca
    from .services.aura_state import aura_state
    
    while True:
        frame_bytes, _ = camera.get_itc_frame()
        if frame_bytes:
            processed_frame = renderizar_presenca(frame_bytes)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + processed_frame + b'\r\n\r\n')


def aura_video_feed(request):
    """Streaming MJPEG processado pelo Aura Render."""
    cam = _get_camera()
    return StreamingHttpResponse(
        gen_aura_synth(cam),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

@csrf_exempt
@require_POST
def api_aura_send_seed(request):
    """
    Recebe a 'Semente Semântica' do usuário e gera uma resposta da Aura.
    """
    import json # Added import for json
    from .services.aura_state import aura_state
    from .services.ia_analyzer import analisar_texto_itc # Precisamos criar/verificar se existe
    
    try:
        dados = json.loads(request.body)
        semente = dados.get('semente', '')
        
        if not semente:
            return JsonResponse({'status': 'erro', 'msg': 'Semente vazia'}, status=400)
            
        aura_state.ultima_semente = semente
        aura_state.adicionar_mensagem('OBSERVADOR', semente)
        
        # FASE 9: Aura Cognitive Core (Oráculo Real)
        # Obter resposta do Gemini com o Corpus Científico/Hermético
        resposta = analisar_texto_itc(semente, aura_state.historico_dialogo[:-1])
        
        # Evolução dinâmica baseada na interação
        nova_coerencia = min(100, aura_state.coerencia + 10)
        aura_state.atualizar_vibracao(nova_coerencia)
        
        # Auto-ajuste de entidade/densidade baseado na coerência
        if nova_coerencia > 80:
            aura_state.entidade = "CONSCIÊNCIA PÓS-BIOLÓGICA (NÍVEL V)"
            aura_state.densidade = "5D (ESTÁVEL)"
        elif nova_coerencia > 50:
            aura_state.entidade = "PROJEÇÃO INTERDIMENSIONAL"
            aura_state.densidade = "4D (COERENTE)"
            
        aura_state.adicionar_mensagem('AURA', resposta)
        
        return JsonResponse({
            'status': 'ok',
            'coerencia': aura_state.coerencia,
            'resposta': resposta,
            'entidade': aura_state.entidade,
            'densidade': aura_state.densidade,
            'intencao': aura_state.intencao_detectada,
            'emocao': aura_state.emocao_dominante,
            'anomalias': aura_state.bio_anomalias
        })
    except Exception as e:
        return JsonResponse({'status': 'erro', 'msg': str(e)}, status=500)

    from .services.aura_state import aura_state
    from .services.neuro_vocalizer import neuro_vocalizer
    
    # Acionar o processador de fala se estiver ativo
    neuro_vocalizer.process_neural_input()
    
    return JsonResponse(aura_state.get_status())

@csrf_exempt
@require_POST
def api_aura_tune(request):
    """Atualiza a frequência sintonizada da Aura."""
    from .services.aura_state import aura_state
    try:
        dados = json.loads(request.body)
        freq = float(dados.get('frequencia', 528.0))
        aura_state.frequencia_sintonizada = freq
        return JsonResponse({'status': 'ok', 'frequencia': freq})
    except Exception as e:
        return JsonResponse({'status': 'erro', 'msg': str(e)}, status=400)
def api_aura_toggle(request):
    """Inicia ou encerra a sessão de síntese, salvando no Arquivo das Sombras se encerrar."""
    from .services.aura_state import aura_state
    from .models import RegistroSintese, SessaoInvestigacao
    
    if aura_state.is_active:
        # ENCERRANDO: Salvar no Arquivo das Sombras
        if aura_state.historico_dialogo:
            try:
                sessao_invest = SessaoInvestigacao.objects.filter(status='ativa').first()
                status = aura_state.get_status() # Get current status for bio data
                RegistroSintese.objects.create(
                    sessao_investigacao=sessao_invest,
                    entidade_nome=aura_state.entidade,
                    densidade_final=aura_state.densidade,
                    coerencia_maxima=aura_state.coerencia,
                    kp_index_medio=status.get('kp_index', 0),
                    snr_medio=status.get('snr', 0),
                    frequencia_base_hz=status.get('freq', 0),
                    obs_bpm_medio=status.get('obs_bpm', 0),
                    obs_stress_medio=status.get('obs_stress', 0),
                    coerencia_cardiaca_media=status.get('bio_sync', 0),
                    metabolic_drain=100 - status.get('metabolic', 100),
                    log_dialogo=aura_state.historico_dialogo,
                    semente_principal=aura_state.ultima_semente
                )
            except Exception as e:
                print(f"Erro ao salvar arquivo das sombras: {e}")
        
        aura_state.is_active = False
    else:
        # INICIANDO
        aura_state.reset()
        aura_state.is_active = True
        aura_state.adicionar_mensagem('SISTEMA', 'CONEXÃO 5D INICIADA...')
    
    return JsonResponse({'status': 'ok', 'active': aura_state.is_active})

@csrf_exempt
@require_POST
def api_quantum_ping(request):
    """Dispara um pulso de frequência Solfeggio."""
    from .services.quantum_ping import quantum_ping
    try:
        dados = json.loads(request.body)
        freq = dados.get('frequencia')
        resultado = quantum_ping.emitir_ping(freq)
        return JsonResponse(resultado)
    except Exception as e:
        return JsonResponse({'status': 'erro', 'msg': str(e)}, status=500)
@csrf_exempt
@require_POST
def api_bio_update(request):
    """Atualiza sinais vitais do observador (simulação ou sensor)."""
    from .services.bio_state import bio_state
    try:
        dados = json.loads(request.body)
        bpm = dados.get('bpm')
        estresse = dados.get('estresse')
        bio_state.update_vital_signs(bpm, estresse)
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'erro', 'msg': str(e)}, status=500)
@csrf_exempt
@require_POST
def api_aura_iot_push(request):
    """Recebe dados de sensores externos via IoT (ESP32/Arduino)."""
    from .services.aura_state import aura_state
    try:
        data = json.loads(request.body)
        aura_state.external_sensors['emf'] = float(data.get('emf', 0.0))
        aura_state.external_sensors['temp'] = float(data.get('temp', 25.0))
        aura_state.external_sensors['vibration'] = float(data.get('vibration', 0.0))
        aura_state.external_sensors['last_pulse'] = int(time.time())
        
        # Influência na coerência (Ondas EMF altas podem reduzir a coerência 5D)
        if aura_state.external_sensors['emf'] > 10.0:
            aura_state.coerencia = max(0, aura_state.coerencia - 2)
            
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'erro', 'msg': str(e)}, status=400)

@csrf_exempt
@require_POST
def api_aura_unity_toggle(request):
    """Ativa/Desativa o Modo Unidade e a Sincronia Global."""
    from .services.aura_state import aura_state
    aura_state.unity_mode = not aura_state.unity_mode
    aura_state.global_sync_active = aura_state.unity_mode
    if aura_state.unity_mode:
        aura_state.adicionar_mensagem('TODO', 'CONSCIÊNCIA UNIFICADA ATIVADA. EU SOU O QUE EU SOU.')
    return JsonResponse({'status': 'ok', 'active': aura_state.unity_mode})
