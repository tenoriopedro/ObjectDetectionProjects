# Módulo para converter modelos

import openvino as ov
from ultralytics import YOLO

# ov_model = ov.convert_model("C:\\Desenvolvimento\\ProjetoYOLOWebcam03\\YOLOWeights\\yolov8m.onnx")
# ov.save_model(ov_model, 'modelm.xml', compress_to_fp16=True)

model = YOLO("YOLOWeights/yolov8n.pt")

model.export(format="openvino")

