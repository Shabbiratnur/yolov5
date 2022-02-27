import cv2
import numpy as np
from glob import glob
import shutil
import json

# Import ground truth json files 

jsons = glob("paste json path here ")

def coordinateCvt2YOLO(size, box):
    
    dw = 1. / size[0]
    dh = 1. / size[1]
    
    # (xmin + xmax / 2)
    x = (box[0] + box[2]) / 2.0
    # (ymin + ymax / 2)
    y = (box[1] + box[3]) / 2.0

    # (xmax - xmin) = w
    w = box[2] - box[0]
    # (ymax - ymin) = h
    h = box[3] - box[1]

    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return [round(x, 3), round(y, 3), round(w, 3), round(h, 3)]

for js in jsons:
    print(js)
    image_name  = js.split('/')[-1].split('_')[0]
    image_name = image_name + '_leftImg8bit'
    im = cv2.imread("paste images path here "+image_name+".png") 
    # create filename
    yolo_gt_file= open("paste folder path for saving generate ground truth in .txt format "+image_name+".txt",'w+')
    json_file= open(js)
    # Load json file
    data = json.load(json_file)
    # Get image width and height
    size_yolo = [im.shape[1],im.shape[0]]
    for doc in data['objects']:
        # Get polygon from json file
        poly=doc['polygon']
        # Get classes from json file
        class_names = np.unique(doc['label'])    
        # convert polygon to minAreaRect    
        poly = np.array(poly,np.int32)
        # convert polygons to minAreaRect    
        rotrect = cv2.minAreaRect(poly)
        box = cv2.boxPoints(rotrect)
        box = np.int0(box)
        y,h,x,w =int(min(box[:, 1])),int(max(box[:, 1])), int(min(box[:, 0])),int(max(box[:, 0]))
        # Define id for each class
        if 'car' in class_names:
            cls = 0    
        elif 'traffic sign' in class_names:
            cls = 1   
        elif 'motorcycle' in class_names:
            cls = 2    
        elif 'pole' in class_names:
            cls = 3
        elif 'autorickshaw' in class_names:
            cls = 4
        elif 'person' in class_names:
            cls=5

        # Ingnore other classes here  
        else:
            continue
    
        x_min,y_min =  x,y

        x_max, y_max = w,h

        class_ids =cls
        bbox_Yolo = [float(x_min) ,float(y_min),float(x_max),float(y_max)]
        bbox = coordinateCvt2YOLO(size_yolo, bbox_Yolo)
        # Write label file
        yolo_gt_file.write('{} {} {} {} {}\n'.format(int(class_ids), bbox[0], bbox[1], bbox[2],bbox[3]))
        