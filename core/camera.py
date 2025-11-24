import cv2
import numpy as np
import os
from django.conf import settings
from datetime import datetime
from .models import Evidencia

class VideoCamera(object):
    def __init__(self):
        # Seu IP do cabo USB (Mantenha o que estava funcionando)
        self.video = cv2.VideoCapture("http://10.93.175.172:8080/video?dummy=param.mjpg")
        
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.peso_ruido = 0.3

    def __del__(self):
        self.video.release()

    def get_frame(self):
        """Função para o Monitor (Ao Vivo)"""
        success, image = self.video.read()
        if not success: return None
        
        # 1. GIRA A IMAGEM (Ajuste conforme necessário: CLOCKWISE ou COUNTERCLOCKWISE)
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

        # 2. Redimensiona para caber no painel
        image = cv2.resize(image, (640, 480))
        
        # 3. Converte para JPG (ESSA PARTE É CRUCIAL, SE FALTAR A IMAGEM SOME)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def processar_anomalia_unica(self, audio_level=0, mag_level=0):
        """Função do Gatilho (Salvar Evidência)"""
        success, image = self.video.read()
        if not success: return {'sucesso': False}
        
        # 1. GIRA A IMAGEM AQUI TAMBÉM (Para salvar em pé)
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        
        image = cv2.resize(image, (640, 480))

        # Ruído Digital
        h, w, c = image.shape
        ruido = np.random.randint(0, 256, (h, w, 3), dtype=np.uint8)
        frame_caotico = cv2.addWeighted(image, 1 - self.peso_ruido, ruido, self.peso_ruido, 0)

        # Detecção
        gray = cv2.cvtColor(frame_caotico, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))

        detectou = len(faces) > 0 or float(audio_level) > 1.5
        
        if detectou:
            for (x, y, w_box, h_box) in faces:
                cv2.rectangle(frame_caotico, (x, y), (x+w_box, y+h_box), (0, 0, 255), 2)

            score = 1
            if float(audio_level) > 2.0: score += 1
            if float(mag_level) > 5: score += 1

            # Salvar Arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ANOMALIA_{timestamp}.jpg"
            path = os.path.join(settings.MEDIA_ROOT, 'evidencias')
            if not os.path.exists(path): os.makedirs(path)
            
            full_path = os.path.join(path, filename)
            cv2.imwrite(full_path, frame_caotico)
            
            url_final = f"/media/evidencias/{filename}"

            # Salvar Banco
            Evidencia.objects.create(
                imagem_url=url_final,
                nivel_audio_db=audio_level,
                variacao_magnetica=mag_level,
                score_coincidencia=score
            )
            return {'sucesso': True, 'url': url_final}
        
        return {'sucesso': False}