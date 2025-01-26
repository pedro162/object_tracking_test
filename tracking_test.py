import cv2

# Verifique a versão do OpenCV
print(cv2.__version__)

# Inicialize o rastreador CSRT
tracker = cv2.legacy.TrackerCSRT_create()

# Caminho do vídeo
file_path = './resources/videos/street.mp4'

# Abra o vídeo
video = cv2.VideoCapture(file_path)

# Leia o primeiro quadro
ok, frame = video.read()

if not ok:
    print("Erro ao ler o vídeo")
    exit()

# Exiba o primeiro quadro e permita que o usuário selecione a ROI
bbox = cv2.selectROI(frame)
print("Caixa delimitadora selecionada:", bbox)

# Inicialize o rastreador com o primeiro quadro e a ROI
ok = tracker.init(frame, bbox)

while True:
    # Leia o próximo quadro do vídeo
    ok, frame = video.read()
    
    if not ok:
        print("Fim do vídeo")
        break

    # Atualize a posição da caixa delimitadora
    ok, bbox = tracker.update(frame)
    
    # Se o rastreamento for bem-sucedido, desenhe a caixa delimitadora no quadro
    if ok:
        (x, y, w, h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)
    else:
        # Se o rastreamento falhar, exiba uma mensagem
        cv2.putText(frame, "Tracking failure", (100, 80), cv2.FONT_HERSHEY_COMPLEX, .75, (0, 0, 255), 2)

    # Exiba o quadro com a caixa delimitadora
    cv2.imshow('Tracking', frame)

    # Interrompa o loop se a tecla 'ESC' for pressionada
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Libere o vídeo e feche as janelas
video.release()
cv2.destroyAllWindows()
