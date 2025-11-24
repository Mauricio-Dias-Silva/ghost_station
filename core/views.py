import json
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .camera import VideoCamera
from .models import Evidencia

cam = VideoCamera()

def dashboard(request):
    # Mostra as últimas 5 capturas
    evidencias = Evidencia.objects.all().order_by('-data_captura')[:5]
    return render(request, 'core/dashboard.html', {'evidencias': evidencias})

@csrf_exempt
def gatilho_anomalia(request):
    """API que recebe o alerta do celular"""
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            audio = dados.get('audio_level', 0)
            mag = dados.get('magnetic_delta', 0)
            origem = dados.get('origem_disparo', 'desconhecido')
            
            print(f"⚠️ GATILHO RECEBIDO ({origem}) | Audio: {audio} | Mag: {mag}")
            
            resultado = cam.processar_anomalia_unica(audio, mag)
            
            if resultado['sucesso']:
                return JsonResponse({'status': 'capturado', 'url': resultado['url']})
            else:
                return JsonResponse({'status': 'ignorado', 'motivo': 'Sem validação visual'})
        except Exception as e:
            return JsonResponse({'status': 'erro', 'msg': str(e)}, status=500)
    return JsonResponse({'status': 'erro'}, status=400)

# Feed de Vídeo (Opcional, apenas para setup)
def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen(cam), content_type='multipart/x-mixed-replace; boundary=frame')