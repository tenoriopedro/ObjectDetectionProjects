import cv2
from database.info_database import get_info
import numpy as np
from PIL import Image, ImageDraw, ImageFont


# Funções primordiais para o funcionamento do codigo


def draw_popup(frame, cap_width, height, class_detected, cursor_over_link01, cursor_over_link02, cursor_overlink03):

    font_size = 15
    font_path = "C:\\Desenvolvimento\\ProjetoYOLOWebcam03\\font\\arial.ttf"
    # Convertendo frame OPENCV para rgb
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame_rgb)

    # Desenhando aba
    popup_x, popup_y, popup_w = 30, 60, cap_width / 2
    draw = ImageDraw.Draw(pil_image)
    draw.rectangle([popup_x, popup_y, popup_x + popup_w, popup_y + height], fill=(255, 255, 255))

    font = ImageFont.truetype(font_path, font_size)

    # Extraindo informações do banco de dados
    list_data = get_info()

    last_popup_y = 0
    positions = []
    link_dict = {}
    image_dict = {}

    # Ligação das informações do banco de dados com as classes(objetos) detectados
    # E tambem colocar informações na tela
    for name in range(len(class_detected)):
        for i in list_data:
            temporary_list = []
            if class_detected[name] in i:
                object, description, link, image = i
                temporary_list.append((f"Objeto detectado: {object}",
                                       f"Descrição: {description}",
                                       f"Link: Clique aqui para saber mais",))
                link_dict[f"{class_detected[name]}"] = link
                # image_dict[f"{class_detected[name]}"] = Image.open(image)

                # Vai revisionar se tem algum texto que ultrapasse a largura da aba
                new_temporary_list = text_review(temporary_list, popup_w, font, draw)

                image_path = image
                img = Image.open(image_path)
                img.thumbnail((50, 50))

                first_line_width = draw.textbbox((0,0), new_temporary_list[0], font=font)[2]

                image_y = popup_y + 5
                image_x = first_line_width + popup_x + 30
                pil_image.paste(img, (image_x, image_y))

                for k,text in enumerate(new_temporary_list):

                    draw.text((popup_x + 10, popup_y + 20 + k * 30), text, font=font, fill=(0, 0, 0))
                    last_popup_y = popup_y + 20 + k * 30

                popup_y = max(last_popup_y, image_y + 50)
                positions.append(last_popup_y)

                # linha divisória
                draw.line([(popup_x + 10, last_popup_y + 40), (popup_x + popup_w - 10, last_popup_y + 40)], fill=(0,0,0), width=3)
                popup_y = last_popup_y + 50


    # Convertendo para o OPENCV
    frame_bgr = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Só aparece a linha quando o cursor passar no local exato do texto
    if cursor_over_link01 and positions:
        cv2.line(frame_bgr,(popup_x + 90, positions[0] + 20), (popup_x + 115, positions[0] + 20), (0,0,0), 2)
    else:
        cv2.line(frame_bgr, (popup_x + 90, positions[0] + 20), (popup_x + 115, positions[0] + 20), (0, 0, 0), 1)

    if cursor_over_link02 and len(positions) >= 2:
        cv2.line(frame_bgr,(popup_x + 90, positions[1] + 20), (popup_x + 115, positions[1] + 20), (0,0,0), 2)
    else:
        if len(positions) >= 2:
            cv2.line(frame_bgr, (popup_x + 90, positions[1] + 20), (popup_x + 115, positions[1] + 20), (0, 0, 0), 1)

    if cursor_overlink03 and len(positions) >= 3:
        cv2.line(frame_bgr,(popup_x + 90, positions[2] + 20), (popup_x + 115, positions[2] + 20), (0,0,0), 2)
    else:
        if len(positions) >= 3:
            cv2.line(frame_bgr, (popup_x + 90, positions[2] + 20), (popup_x + 115, positions[2] + 20), (0, 0, 0), 1)

    click_area = []
    for pos in range(len(positions)):
        x1 = popup_x + 90
        y1 = positions[pos] + 5
        x2 = popup_x + 115
        y2 = positions[pos] + 25
        click_area.append((x1, y1, x2, y2))

    return frame_bgr, click_area, link_dict


def text_review(temporary_list, popup_w, font, draw):


    lines = []
    for data in temporary_list:
        for text in data:
            words = text.split()
            new_line = ""
            for word in words:

                text_width = draw.textbbox((0, 0), new_line + word + ' ', font=font)[2]

                if text_width > popup_w - 60:
                    lines.append(new_line.strip())
                    new_line = word + ' '
                else:
                    new_line += word + ' '

            lines.append(new_line.strip())

    return lines


def draw_image(image_dict,first_line_width, popup_y, popup_x):
    x, y = popup_x + first_line_width, popup_y + 40

    for object, image_path in image_dict.items():
        image = image_path

        image = image.resize((50, 50))

        # Converter para RGB se necessário
        if image.mode != "RGB":
            image = image.convert("RGB")

        image.paste(image, (x, y))

        return image

coco_classes_pt = [
    "pessoa","bicicleta","carro","motocicleta","avião","autocarro","comboio","camião","barco","semáforo",
    "hidrante","sinal de stop","parquímetro","banco","pássaro","gato","cão","cavalo","ovelha","vaca",
    "elefante","urso","zebra","girafa","mochila","guarda-chuva","carteira","gravata","mala","frisbee",
    "esquis","prancha de snowboard","bola desportiva","papagaio","taco de baseball","luva de baseball",
    "skate","prancha de surf","raquete de ténis","garrafa","copo de vinho","chavena","garfo","faca",
    "colher","taça","banana","maçã","sanduiche","laranja","brocolos","cenoura","cachorro quente","pizza",
    "donut","bolo","cadeira","sofa","planta em vaso","cama","mesa de jantar","sanita","televisão",
    "portátil","rato","comando","teclado","telemóvel","microondas","forno","torradeira","lava-loiça",
    "frigorífico","livro","relógio","vaso","tesoura","urso de peluche","secador de cabelo",
    "escova de dentes"
]