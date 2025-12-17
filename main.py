import os;
import pytesseract;
import time;

from PIL import Image;
from nava import play, stop;

current_working_directory = os.path.dirname(os.path.abspath(__file__))
current_sound = 0

#"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def analyze_img_text (): #vague 
  img_text_data = pytesseract.image_to_data(Image.open(str(current_working_directory) + "\\img_src\\source.jpg"), output_type = pytesseract.Output.DICT)
  accuracy_list = []
  
  for i in range (len(img_text_data['text'])):
    accuracy = int(img_text_data['conf'][i])
  
    if accuracy != -1:
      accuracy_list.append(accuracy)
    else:
      print("No text detected.")

  if (len(accuracy_list) < 1):
    print("No target.")
  else:
    total_accuracy = 0
    for num in accuracy_list:
      total_accuracy += num
    
    total_accuracy = total_accuracy / (len(accuracy_list))

    if (total_accuracy < 80 and total_accuracy > 10):
      current_sound = play(current_working_directory + "\\search.wav", async_mode=True, loop=True)
      time.sleep(30)
    if (total_accuracy >= 80):
      current_sound = play(current_working_directory + "\\lock.wav", async_mode=True, loop=True)
      time.sleep(10)

analyze_img_text()