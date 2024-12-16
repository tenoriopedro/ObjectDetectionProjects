## Se necessário mudar versão do torch e torchvision
## torch==2.3.1 torchvision==0.18.1


from ultralytics import YOLO
from ultralytics.solutions import object_counter
import cv2

model = YOLO("C:\\Desenvolvimento\\ProjetosEstagio\\ProjetoContagemYOLO\\yolov8x.pt")
cap = cv2.VideoCapture("C:\\Desenvolvimento\\ProjetosEstagio\\ProjetoContagemYOLO\\test_files\\track_video_car01.mp4")

w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# classes que serão identificadas(COCO)
class_to_count = [2, 3, 7] #(2: carro, 3:motocicleta, 7:caminhão)

# linha tracker
line_points = [(20, 400), (1500, 400)]

video_writer = cv2.VideoWriter("compiled_files\\object_counting_output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))


# Iniciar Object Counter

counter = object_counter.ObjectCounter(
    names=model.names,
    view_img=True,
    reg_pts=line_points,
    draw_tracks=True
)

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    tracks = model.track(im0, 
                         persist=True, 
                         show=False, classes=class_to_count)
    print('oi')
    im0 = counter.start_counting(im0, tracks)
    video_writer.write(im0)

    if cv2.waitKey(5)&0xFF == ord('q'):
        break

cap.release()
video_writer.release()
cv2.destroyAllWindows()
