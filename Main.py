
import numpy as np

from tkinter import *
import os
from tkinter import filedialog
import cv2
import time





def endprogram():
	print ("\nProgram terminated!")
	sys.exit()



def image():
    import_file_path = filedialog.askopenfilename()

    image = cv2.imread(import_file_path)
    print(import_file_path)
    filename = 'Test.jpg'
    cv2.imwrite(filename, image)


    import easyocr
    import cv2 as cv
    reader = easyocr.Reader(['en'])

    import win32com.client as wincl
    speak = wincl.Dispatch("SAPI.SpVoice")


    img = cv.imread('Test.jpg')
    result = reader.readtext(img)
    print(result)




    cv.imshow('frame', img)
    cv.waitKey(0)
    cv.destroyAllWindows()









def main_account_screen():
    global main_screen
    main_screen = Tk()
    width = 600
    height = 600
    screen_width = main_screen.winfo_screenwidth()
    screen_height = main_screen.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    main_screen.geometry("%dx%d+%d+%d" % (width, height, x, y))
    main_screen.resizable(0, 0)
    # main_screen.geometry("300x250")
    main_screen.title(" OCR Detection")

    Label(text="OCR Detection", width="300", height="5", font=("Calibri", 16)).pack()



    Button(text="image", font=(
        'Verdana', 15), height="2", width="30", command=image, highlightcolor="black").pack(side=TOP)

    Label(text="").pack()

    Button(text="OCR", font=(
        'Verdana', 15), height="2", width="30", command=cocr, highlightcolor="black").pack(side=TOP)
    Label(text="").pack()

    main_screen.mainloop()


main_account_screen()

