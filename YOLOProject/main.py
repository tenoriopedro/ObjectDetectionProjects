import cv2
import math
import webbrowser
from ultralytics import YOLO
from utils.functions import (coco_classes_pt, draw_popup)
from database.data_database import save_in_database

circle_clicked = False
pause_stream = False
popup_opening = False
cursor_over_link01 = False
cursor_over_link02 = False
cursor_over_link03 = False


def mouse_event(event, x, y, flags, params):
    global circle_clicked, popup_opening, popup_height, \
        pause_stream, cursor_over_link01, cursor_over_link02, cursor_over_link03, link_url_dict
    try:
        circle_x1, circle_y1, radius = params[0]
        click_area_list = params[1]

        if event == cv2.EVENT_LBUTTONDOWN:
            if (x - circle_x1) ** 2 + (y - circle_y1) ** 2 <= radius ** 2:
                if not circle_clicked:
                    circle_clicked = True
                    popup_opening = True
                    pause_stream = True

                else:
                    pause_stream = False
                    circle_clicked = False
                    popup_opening = False
        sublistas = {}
        if click_area_list:
            for i, sublista in enumerate(click_area_list):
                sublistas[f"sublista_{i+1}"] = sublista

        if circle_clicked:
            if sublistas:
                x1, y1, x2, y2 = sublistas['sublista_1']
                if x1 <= x <= x2 and y1 <= y <= y2:
                    cursor_over_link01 = True
                    for key, value in link_url_dict.items():
                        if key == class_detected[0]:
                            if event == cv2.EVENT_LBUTTONDOWN:
                                webbrowser.open(value)
                else:
                    cursor_over_link01 = False

            if len(sublistas) >= 2:
                x3, y3, x4, y4 = sublistas['sublista_2']
                if x3 <= x <= x4 and y3 <= y <= y4:
                    cursor_over_link02 = True
                    if len(class_detected) >= 2:
                        for key, value in link_url_dict.items():
                            if key == class_detected[1]:
                                if event == cv2.EVENT_LBUTTONDOWN:
                                    webbrowser.open(value)
                else:
                    cursor_over_link02 = False

            if len(sublistas) >= 3:
                x5, y5, x6, y6 = sublistas['sublista_3']
                if x5 <= x <= x6 and y5 <= y <= y6:
                    cursor_over_link03 = True
                    if len(class_detected) == 3:
                        for key, value in link_url_dict.items():
                            if key == class_detected[2]:
                                if event == cv2.EVENT_LBUTTONDOWN:
                                    webbrowser.open(value)

                else:
                    cursor_over_link03 = False

    except:
        pass



# Selecionando web cam (0=webcam integrada, 3=webcam virtual OBS)
cap = cv2.VideoCapture(0)
cap_width = 640
cap_height = 480
cap.set(3, cap_width)
cap.set(4, cap_height)
# ip = "https://192.168.1.66:8080/video"
# cap.open(ip)

popup_height = 0
max_popup_height = cap_height - 100
min_popup_height = 0
animation_speed = 40

# Model
model = YOLO("YOLOWeights/yolov8n_openvino_model")

# Nome das classes do dataset (COCO)
classNames = coco_classes_pt

# Constante para cores
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_LINE = (255, 255, 255)
COLOR_CIRCLE = (34, 34, 174)
COLOR_LINK = (255, 255, 255)

# Variavel para armazenar ultimo frame
last_frame = None

# variavel para armazenar link
link_url_dict = None

while True:
    if not pause_stream:
        sucess, frame = cap.read()
        if not sucess:
            print("Não foi possivel abrir video")
            break
        last_frame = frame.copy()
    else:
        frame = last_frame.copy()

    # tirar efeito de espelho(se necessário)
    # frame = cv2.flip(frame, 1)

    results = model(frame)

    # Definições do ponto detector
    circle_x1 = 35
    circle_y1 = 25
    radius = 10
    thickness_circle = -1
    circle_positions = []

    class_detected = []
    click_area = []

    for data in results:
        boxes = data.boxes

        for box in boxes:

            # nivel de certeza da imagem(apenas 2 casas decimais)
            conf = math.ceil((box.conf[0] * 100)) / 100

            # ID class
            cls = int(box.cls[0])

            if conf > 0.5 and (classNames[cls] == "telemóvel" or classNames[cls] == "comando" or classNames[cls] == "pessoa"):

                # Desenhar ponto detector
                cv2.circle(frame, (circle_x1, circle_y1), radius, COLOR_CIRCLE, thickness_circle)
                # Area clicavel para o circulo
                circle_positions = [circle_x1, circle_y1, radius]
                # Guardando objetos detectados
                object_detected = classNames[cls]
                class_detected.append(object_detected)

                # Desenha aba de forma gradativa
                if popup_opening and popup_height < max_popup_height:
                    popup_height += animation_speed
                    if popup_height >= max_popup_height:
                        popup_height = max_popup_height

                if not popup_opening and popup_height > min_popup_height:
                    popup_height -= animation_speed
                    if popup_height <= min_popup_height:
                        popup_height = min_popup_height

                if circle_clicked:
                    frame, click_area, link_url_dict = draw_popup(frame,
                                                                  cap_width,
                                                                  popup_height,
                                                                  class_detected,
                                                                  cursor_over_link01,
                                                                  cursor_over_link02,
                                                                  cursor_over_link03)

                # salvando dados a base de dados
                save_in_database(object_detected)


    cv2.imshow("Video Test", frame)
    cv2.setMouseCallback("Video Test", mouse_event, param=(circle_positions, click_area))

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

print("Fim do programa.")