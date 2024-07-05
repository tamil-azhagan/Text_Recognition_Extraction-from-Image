import easyocr
import numpy as np

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.constants import *
from PIL import Image, ImageEnhance

reader = easyocr.Reader(['en'])

# Image fetching and text extraction
def ocr_image(image_path):
    try:
        image = Image.open(image_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)  
        image_np = np.array(image)

        result = reader.readtext(image_np)
        text = ' '.join([item[1] for item in result])
        return text

    except Exception as e:
        print(f"Error during OCR: {str(e)}")
        return None

def main(image_path):
    try:
        # Perform OCR to get the text
        recognized_text = ocr_image(image_path)
        if recognized_text:
            return recognized_text
        else:
            return "Nothing Recognized"
            

    except Exception as e:
        print(f"Error during main execution: {str(e)}")
        return "Error Occurred"



# GUI
root = Tk()
root.title("TextRecognizer")
root.geometry('500x500')

title = Label(root, text="Extract Text from Image", font=("Helvetica", 20, "bold"))
title.grid(row=0, column=0, columnspan=2)

# label_path = Label(root, text='Image Path:')
# label_path.pack(side=LEFT, padx)

label_path=Label(root, text="Image Path:", font=("Times",10))
label_path.grid(row=1, column=0, padx=5, pady=20, sticky='W')

label_img=Label(root, text="None selected", font=("Times",10,"bold"), foreground='red')
label_img.grid(row=1, column=1, padx=5, pady=20, sticky='W')

def browse_action():
    global filename
    filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

    if filename:
        label_img.config(text = filename, fg='green')
        btn_extract['state'] = 'active'

def extract_action():
    result = main(label_img.cget("text"))
    label_result_txt.config(text=result, fg='red')
    

btn_browse = Button(root, text="Browse", command=browse_action)
btn_browse.grid(row=1, column=2, padx=50, pady=20, sticky='W')

btn_extract = Button(root, text="Extract Text", state='disabled', command=extract_action)
btn_extract.grid(row=2, column=2, padx=50, pady=40, sticky='W')

label_result = Label(root, text="Recognized Text: ", font=("Times",10))
label_result.grid(row=2, column=0, pady=40, columnspan=2, sticky='W')

label_result_txt = Label(root, text="", font=("Times",10), wraplength=200)
label_result_txt.grid(row=2, column=1, padx=50, pady=40, columnspan=2, sticky='W')
root.mainloop()