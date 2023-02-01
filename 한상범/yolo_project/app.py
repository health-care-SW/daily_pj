import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom
# Images
img = 'yolov5\data\images\down.jpg'  # or file, Path, PIL, OpenCV, numpy, list
# Inference
results = model(img)

# Results
results.save()  # or .show(), .save(), .crop(), .pandas(), etc.