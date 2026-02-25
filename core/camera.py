"""
Ghost Station — Serviço de Câmera Refatorado.
Lazy-load: a câmera só conecta quando alguém pedir.
IP configurável via settings.
"""
import cv2
import numpy as np
import os
import threading
from django.conf import settings
from datetime import datetime
from .models import Evidencia


class VideoCamera:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Singleton — evita múltiplas conexões com a câmera."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.video = None
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.peso_ruido = 0.3
        self._connected = False
        self.last_gray = None # Para calcular Motion Score ITC

    def _connect(self):
        """Conecta à câmera sob demanda (lazy-load)."""
        if self._connected and self.video and self.video.isOpened():
            return True
        cam_url = getattr(settings, 'GHOST_CAMERA_URL', 'http://10.93.175.172:8080/video?dummy=param.mjpg')
        try:
            self.video = cv2.VideoCapture(cam_url)
            self._connected = self.video.isOpened()
            if self._connected:
                print(f"📷 Câmera conectada: {cam_url}")
            else:
                print(f"⚠️ Falha ao conectar câmera: {cam_url}")
        except Exception as e:
            print(f"❌ Erro na câmera: {e}")
            self._connected = False
        return self._connected

    @property
    def is_connected(self):
        return self._connected and self.video and self.video.isOpened()

    def disconnect(self):
        if self.video:
            self.video.release()
        self._connected = False

    def get_frame(self):
        """Frame para monitor ao vivo."""
        if not self._connect():
            return self._frame_offline()
        success, image = self.video.read()
        if not success:
            return self._frame_offline()
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        image = cv2.resize(image, (640, 480))
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def _frame_offline(self):
        """Frame placeholder quando a câmera não está conectada."""
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(img, 'SEM SINAL', (180, 220), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 65), 2)
        cv2.putText(img, 'Conecte a camera IP', (150, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 1)
        cv2.putText(img, f'URL: {getattr(settings, "GHOST_CAMERA_URL", "N/A")}',
                    (80, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (80, 80, 80), 1)
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()

    def get_itc_frame(self):
        """
        Frame especializado para o ITC Visual (Telefone do Além).
        Aplica filtros de alto contraste (CLAHE), detecção de bordas (Canny) 
        e mesclagem para realçar padrões anômalos. Calcula o 'Motion Score'.
        Retorna: (jpeg_bytes, motion_score)
        """
        if not self._connect():
            return self._frame_offline(), 0

        success, image = self.video.read()
        if not success:
            return self._frame_offline(), 0

        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        image = cv2.resize(image, (640, 480))

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # MOTION SCORE (Diferença absoluta para detectar vultos/movimentos)
        motion_score = 0
        if self.last_gray is not None:
            diff = cv2.absdiff(self.last_gray, gray)
            # Acima de um threshold para ignorar ruído normal
            _, thresh_diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
            motion_score = int(np.sum(thresh_diff) / 255) # Conta pixels alterados
        self.last_gray = gray.copy()

        # APERFEIÇOAMENTO PARANORMAL (FILTROS)
        # 1. CLAHE (Contrast Limited Adaptive Histogram Equalization) para realçar variações térmicas/sombras
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        contrast_gray = clahe.apply(gray)

        # 2. Canny Edge Detection (Linhas estruturais)
        edges = cv2.Canny(contrast_gray, 50, 150)

        # 3. Mesclagem Térmica Falsa (Mapa de calor em vermelho para Ghost Hunting)
        # Transforma o gray em mapa de cor quente (Autumn/Inferno/Jet - vamos usar Autumn para vermelho/amarelo)
        heatmap = cv2.applyColorMap(contrast_gray, cv2.COLORMAP_AUTUMN)

        # 4. Sobrepor as bordas no mapa de calor em verde ciano forte
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        edges_bgr[np.where((edges_bgr == [255, 255, 255]).all(axis=2))] = [255, 255, 0] # Ciano/Amarelo nas bordas

        # Mix: Heatmap escurecido + Bordas brilhantes
        final_itc = cv2.addWeighted(heatmap, 0.4, edges_bgr, 0.8, 0)

        # HUD Overlay
        cv2.putText(final_itc, f'ITC ACTIVE // MOTION: {motion_score}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        ret, jpeg = cv2.imencode('.jpg', final_itc)
        return jpeg.tobytes(), motion_score

    def processar_anomalia_unica(self, audio_level=0, mag_level=0, origem='desconhecido',
                                  lat=None, lon=None, sessao=None):
        """Gatilho: captura frame, detecta anomalia, salva evidência."""
        if not self._connect():
            return {'sucesso': False, 'motivo': 'Camera offline'}

        success, image = self.video.read()
        if not success:
            return {'sucesso': False, 'motivo': 'Falha leitura frame'}

        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        image = cv2.resize(image, (640, 480))

        # ==========================================
        # EFEITO NIGHT VISION (Ghost Hunting UI)
        # ==========================================
        # 1. Converter para escala de cinza
        gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 2. Aplicar mapa de cores (LUT) Verde
        # Criando um mapa de cores customizado (Preto para Verde Claro)
        lut = np.zeros((256, 1, 3), dtype=np.uint8)
        lut[:, 0, 0] = 0           # Blue (0)
        lut[:, 0, 1] = np.arange(256) # Green (0 a 255)
        lut[:, 0, 2] = 0           # Red (0)
        
        night_vision = cv2.LUT(gray_frame, lut)
        
        # 3. Adicionar Ruído Granulado (ISO alto simulado)
        h, w, c = night_vision.shape
        ruido = np.random.randint(0, 50, (h, w, 3), dtype=np.uint8)
        frame_caotico = cv2.addWeighted(night_vision, 1.0, ruido, self.peso_ruido, 0)
        
        # 4. Adicionar Vinheta (Bordas escuras)
        X_kernel = cv2.getGaussianKernel(w, w/2)
        Y_kernel = cv2.getGaussianKernel(h, h/2)
        kernel = Y_kernel * X_kernel.T
        mask = 255 * kernel / np.linalg.norm(kernel)
        mask = cv2.resize(mask, (w, h))
        vignette = np.zeros_like(frame_caotico, dtype=np.float32)
        for i in range(3):
            vignette[:,:,i] = frame_caotico[:,:,i] * mask
        frame_caotico = np.clip(vignette, 0, 255).astype(np.uint8)
        # ==========================================

        # Detecção de rostos
        gray = cv2.cvtColor(frame_caotico, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))

        has_face = len(faces) > 0
        has_audio = float(audio_level) > 1.5
        has_mag = float(mag_level) > 5

        detectou = has_face or has_audio

        if detectou:
            for (x, y, w_box, h_box) in faces:
                cv2.rectangle(frame_caotico, (x, y), (x + w_box, y + h_box), (0, 0, 255), 2)
                cv2.putText(frame_caotico, 'ANOMALIA', (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            # Score de coincidência
            score = 1
            if has_audio:
                score += 1
            if has_mag:
                score += 1
            if has_face:
                score += 1

            # Determinar tipo
            if has_face and has_audio:
                tipo = 'multipla'
            elif has_face:
                tipo = 'visual'
            elif has_audio:
                tipo = 'sonora'
            else:
                tipo = 'magnetica'

            # Timestamp HUD no frame
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame_caotico, f'GS // {ts} // SCORE:{score}',
                        (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 65), 1)

            # Salvar Arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ANOMALIA_{timestamp}.jpg"
            path = os.path.join(settings.MEDIA_ROOT, 'evidencias')
            if not os.path.exists(path):
                os.makedirs(path)

            full_path = os.path.join(path, filename)
            cv2.imwrite(full_path, frame_caotico)

            url_final = f"/media/evidencias/{filename}"

            # Salvar no Banco
            evidencia = Evidencia.objects.create(
                sessao=sessao,
                imagem_url=url_final,
                tipo=tipo,
                nivel_audio_db=audio_level,
                variacao_magnetica=mag_level,
                score_coincidencia=score,
                origem_disparo=origem,
                latitude=lat,
                longitude=lon,
            )
            return {
                'sucesso': True,
                'url': url_final,
                'id': evidencia.id,
                'score': score,
                'tipo': tipo,
            }

        return {'sucesso': False, 'motivo': 'Sem validação visual'}