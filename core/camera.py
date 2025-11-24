import cv2
import numpy as np
import os
from django.conf import settings
from datetime import datetime
from .models import Evidencia

class VideoCamera(object):
    def __init__(self):
        # Tenta abrir a webcam (0). Se der erro, tente 1.
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.peso_ruido = 0.3 # 30% de ruído digital

    def __del__(self):
        self.video.release()

    def get_frame(self):
        """Apenas para visualização ao vivo no painel (não grava)"""
        success, image = self.video.read()
        if not success: return None
        
        image = cv2.resize(image, (640, 480))
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def processar_anomalia_unica(self, audio_level=0, mag_level=0):
        """
        GATILHO: Chamado apenas quando o sensor de áudio/mag dispara.
        """
        success, image = self.video.read()
        if not success: return {'sucesso': False}
        
        image = cv2.resize(image, (640, 480))

        # 1. Gerar Ruído (Matriz Caótica)
        h, w, c = image.shape
        ruido = np.random.randint(0, 256, (h, w, 3), dtype=np.uint8)
        frame_caotico = cv2.addWeighted(image, 1 - self.peso_ruido, ruido, self.peso_ruido, 0)

        # 2. Detecção de Rosto
        gray = cv2.cvtColor(frame_caotico, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))

        # Lógica de Validação: Salva se tiver rosto OU se o áudio foi muito alto
        tem_rosto = len(faces) > 0
        audio_alto = float(audio_level) > 60 
        
        if tem_rosto or audio_alto:
            # Desenha retângulo se tiver rosto
            for (x, y, w_box, h_box) in faces:
                cv2.rectangle(frame_caotico, (x, y), (x+w_box, y+h_box), (0, 0, 255), 2)

            # Calcula Score
            score = 1
            if audio_alto: score += 1
            if float(mag_level) > 5: score += 1

            # Salva Imagem no Disco
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ANOMALIA_{timestamp}.jpg"
            
            path_dir = os.path.join(settings.MEDIA_ROOT, 'evidencias')
            if not os.path.exists(path_dir): os.makedirs(path_dir)
            
            full_path = os.path.join(path_dir, filename)
            cv2.imwrite(full_path, frame_caotico)
            
            url_final = f"/media/evidencias/{filename}"

            # Salva no Banco
            Evidencia.objects.create(
                imagem_url=url_final,
                nivel_audio_db=audio_level,
                variacao_magnetica=mag_level,
                score_coincidencia=score
            )
            return {'sucesso': True, 'url': url_final}
        
        return {'sucesso': False}