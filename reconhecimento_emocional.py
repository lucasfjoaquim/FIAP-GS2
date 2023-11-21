from fer import FER
import cv2

def escanear_imagem(path):
    img = cv2.imread(path)
    detector = FER()
    return detector.detect_emotions(img)