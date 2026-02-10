# core/views.py — Ghost Station Views (Refatorado)

import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Evidencia, SessaoInvestigacao
from django.utils import timezone


def _get_camera():
    """Lazy-load da câmera — só instancia quando precisar."""
    from .camera import VideoCamera
    return VideoCamera()


def dashboard(request):
    """Dashboard principal com sessão ativa e evidências."""
    sessao_ativa = SessaoInvestigacao.objects.filter(status='ativa').first()
    evidencias = Evidencia.objects.all().order_by('-data_captura')[:10]

    # Stats
    total_evidencias = Evidencia.objects.count()
    score_max = Evidencia.objects.order_by('-score_coincidencia').first()
    sessoes_total = SessaoInvestigacao.objects.count()

    return render(request, 'core/dashboard.html', {
        'evidencias': evidencias,
        'sessao_ativa': sessao_ativa,
        'total_evidencias': total_evidencias,
        'score_max': score_max.score_coincidencia if score_max else 0,
        'sessoes_total': sessoes_total,
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