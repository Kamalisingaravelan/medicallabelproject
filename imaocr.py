import easyocr
import cv2 as cv
from gtts import gTTS
import os
import time
from googletrans import Translator


file_path = "tamil_voice.mp3"

# Try to close and wait before deleting
'''try:
    os.remove(file_path)
except PermissionError:
    print("File is in use, waiting...")
    time.sleep(5)  # Wait 5 seconds
    os.remove(file_path)  # Try again'''

# Tamil text to convert

reader = easyocr.Reader(['en'])
img = cv.imread('sign.png')
result = reader.readtext(img)
print(result)
#for detection in result:
    #text = detection[1]
    #print(text)

final_text = " ".join([detection[1] for detection in result])

translator = Translator()
translated_text = translator.translate(final_text, src='en', dest="ta")
print(translated_text)
tamil_text = translated_text.text
tts = gTTS(text=tamil_text, lang='ta')
tts.save("tamil_voice.mp3")
os.system("start tamil_voice.mp3")


