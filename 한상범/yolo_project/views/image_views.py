from flask import Blueprint, render_template, request
import torch

bp = Blueprint('image', __name__, url_prefix='/image')

@bp.route('/upload_image/', methods=['POST'])
def upload_image_file():
    if request.method == 'POST':
        file = request.files['uploaded_image'] # 이미지 받기
        if not file: return render_template('image.html', label="No Files")
        label = file.filename
        
        
        file.save('yolo_project/static/'+label) # 그리고 파일을 서버에 저장한다.
        return render_template('index.html', label = label) # 다시 이미지를 출력하기 위해서 파일을 변수로 준다.
    
    
    
@bp.route('/image_preprocess/')
def preprocessing():
    # Model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom
    # Images
    
    img = 'yolo_project/yolov5/data/images/down.jpg'  # or file, Path, PIL, OpenCV, numpy, list
    # Inference
    results = model(img)

    # Results
    results.save()  # or .show(), .save(), .crop(), .pandas(), etc.
    # label = 'yolo_project/runs/detect/exp/down.jpg'

    # 결과 리턴
    return render_template('image.html')
