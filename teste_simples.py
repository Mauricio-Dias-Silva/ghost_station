import cv2

# O link com o truque do mjpg
url = "http://10.93.175.172:8080/video?dummy=param.mjpg"

print(f"Conectando em: {url}")
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("ERRO FATAL: O Python não conseguiu abrir o link.")
else:
    print("SUCESSO! Lendo frames... (Aperte 'q' na janela para sair)")
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('TESTE CAM', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Falha ao ler frame.")
            break

cap.release()
cv2.destroyAllWindows()
