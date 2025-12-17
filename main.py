import os;
import pytesseract;
import time;
# import threading;

from PIL import Image;
from nava import play, stop;

current_working_directory = os.path.dirname(os.path.abspath(__file__))
current_sound = 0
interval_time = 0.6

is_sound_playing = 0
match_time = 150
keyboard_interrupt = 0

#"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def analyze_img_text (): #vague 
  global is_sound_playing

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

    if (total_accuracy < 80 and total_accuracy > 20):
      if (is_sound_playing == 0):
        current_sound = play(current_working_directory + "\\search.wav", async_mode=True, loop=True)
        is_sound_playing = 1
      else:
        if (is_sound_playing == 2):
          current_sound = play(current_working_directory + "\\search.wav", async_mode=True, loop=True)
    if (total_accuracy >= 80):
      if (is_sound_playing == 0):
        current_sound = play(current_working_directory + "\\lock.wav", async_mode=True, loop=True)
        is_sound_playing = 2
      else:
        if (is_sound_playing == 1):
          current_sound = play(current_working_directory + "\\lock.wav", async_mode=True, loop=True)
    if (total_accuracy < 80 and total_accuracy < 20):
      if (is_sound_playing == 1 or is_sound_playing == 2):
        current_sound = play(current_working_directory + "\\zero.wav")
    if (keyboard_interrupt == 1):
      if (is_sound_playing == 1 or is_sound_playing == 2):
        current_sound = play(current_working_directory + "\\zero.wav")

def run_command (command_text):
  command_text = command_text.lower()
  match (command_text):
    case "master_lock_on":
      def lock_loop ():
        analyze_img_text()
        time.sleep(interval_time)
        lock_loop()
      lock_loop()
      return "Lock loop started."
    case "quit":
      exit()
    case "help":
      return """
HELP - returns a list of commands
MASTER_LOCK_ON - begins search and lock sequence
CTRL + C - ends search and lock sequence
QUIT - quits the program
      """
    case _:
      return "No such command exists."

def interface_cmd ():
  global is_sound_playing
  global current_sound

  print("Type HELP for a list of commands.")
  cmd = input("Command: ")
  try:
    print(str(run_command(cmd)))
  except KeyboardInterrupt as e:
    if (is_sound_playing == 1 or is_sound_playing == 2):
      try:
        stop(current_sound)
        current_sound = 0
      except Exception as e:
        is_sound_playing = 0
        current_sound = 0
      is_sound_playing = 0
      current_sound = play(current_working_directory + "\\zero.wav")
    print("Loop sequence interrupted.")
  interface_cmd()

interface_cmd()