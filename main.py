import cv2;
import numpy;
import os;
import base64;
import io;

from typing import List, Dict, Tuple;
from PIL import Image;
from nava import play, stop;

THRESHOLD = 0.8 # for lock.
SEARCH_THRESHOLD = 0.4 # for search.

current_working_directory = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = current_working_directory + '\\radar.txt'
DAR_PATH = current_working_directory + '\\lock\\source.png'
TEMPLATE_DIR = current_working_directory + '\\models'

sound_is_playing = 0
current_sound = 0

def lock_target ():
  global sound_is_playing
  global current_sound

  t_img_load = ''
  print(SRC_PATH)
  try:
    t_img_load = open(SRC_PATH)
    t_img_load = t_img_load.read()
  except Exception as e:
    print(f"Error: {e}")
    return str(e)

  image_f = io.BytesIO(base64.b64decode(t_img_load))
  pilimage = Image.open(image_f)
  src_img_color = cv2.imread(DAR_PATH)

  if (src_img_color is None):
    print(f"No source image detected at {SRC_PATH}")
    return None

  src_img_gray = cv2.cvtColor(src_img_color, cv2.COLOR_BGR2GRAY)
  templates: List[Dict] = []

  for filename in os.listdir(TEMPLATE_DIR):
    if (filename.endswith(('.png', '.jpg', '.jpeg'))):
      fpath = os.path.join(TEMPLATE_DIR, filename)
      timg = cv2.imread(fpath, 0)

      if (timg is not None):
        width, height = timg.shape[::-1]
        templates.append({
          'name' : filename.split('.')[0],
          'template' : timg,
          'w' : width,
          'h' : height,
          'color' : tuple(numpy.random.randint(0, 255, 3).tolist())
        })
  
  if not templates:
    print(f"No templates loaded from {TEMPLATE_DIR}.")
    return src_img_color
  
  print(f"LOAD SUCCESS! {len(templates)} templates loaded.")

  total_matches = 0
  one_cond_met = 0

  for item in templates:
    template = item['template']
    width, height = item['w'], item['h']
    name = item['name']
    color = item['color']

    result = cv2.matchTemplate(src_img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc_search = numpy.where(result >= SEARCH_THRESHOLD) #search
    loc_lock = numpy.where(result >= THRESHOLD)

    lcc_search = len(loc_search[0])
    lcc_lock = len(loc_lock[0])

    if (lcc_search > 0 and lcc_lock < 1):
      if (one_cond_met == 1):
        current_sound.stop()
        sound_is_playing = 0
      if (sound_is_playing == 0):
        current_sound = play("search.mp3", async_mode=True, loop=True)
        sound_is_playing = 1
        one_cond_met = 1
    
    if (lcc_lock > 0):
      if (one_cond_met == 1):
        current_sound.stop()
        sound_is_playing = 0
      if (sound_is_playing == 0):
        current_sound = play("lock.mp3", async_mode=True, loop=True)
        sound_is_playing = 1
        one_cond_met = 1
    
    if (lcc_lock < 1 and lcc_search < 1):
      if (sound_is_playing == 1):
        stop(current_sound)
      sound_is_playing = 0
  
    for pt in zip(*loc_lock[::-1]):
      bottom_right = (pt[0] + width, pt[1] + h)
      cv2.rectangle(src_img_color, pt, bottom_right, color, 2)
      cv2.putText(src_img_color, name, (pt[0], pt[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
      total_matches += 1

  print("PROS 1")

lock_target()