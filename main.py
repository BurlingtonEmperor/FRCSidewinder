import cv2;
import numpy as np;
import os;

TEMPLATE_DIR = 'models'
THRESHOLD = 0.8

templates = []

def load_templates (directory):
  for filename in os.listdir(directory):
    if (filename.endswith(('.png', '.jpg', '.jpeg'))):
      path = os.path.join(directory, filename)
      template_img = cv2.imread(path, 0)

      if (template_img is not None):
        width, height = template_img.shape[::-1]
        templates.append({
          'name' : filename.split('.')[0],
          'template' : template_img,
          'w' : width,
          'h' : height,
          'color' : tuple(np.random.randint(0, 255, 3).tolist())
        })
      else:
        print("Could not load template image at {filename}")
  
  if not templates:
    print("There are no templates loaded. Check the 'models' directory.")
    exit()