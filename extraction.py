import urllib.request
import re
import pandas as pd
import pdf2image
from pdf2image import convert_from_path
from PIL import Image
from pytesseract import pytesseract
import cv2
import re
import numpy as np
from datetime import datetime
from multiprocessing import Pool
import os
import requests

path_to_tesseract = r'/usr/bin/test'
pytesseract.tesseract_cmd = path_to_tesseract 

def text_details(link):
    
    tmp = None
    pages = convert_from_path(link)
    image = np.array(pages[0])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Remove horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,1))
    detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (0,0,0), 2)

    # Remove vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,15))
    detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (0,0,0), 3)

    # Dilate to connect text and remove dots
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,1))
    dilate = cv2.dilate(thresh, kernel, iterations=2)
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 500:
            cv2.drawContours(dilate, [c], -1, (0,0,0), -1)

    # Bitwise-and to reconstruct image
    result = cv2.bitwise_and(image, image, mask=dilate)
    result[dilate==0] = (255,255,255)

    # OCR
    data = pytesseract.image_to_string(result, lang='eng',config='--psm 6')
#     print(data)
    
#     Application_number,dob,roll from data
    try: 
        if "Application No. :" in data:
            appno = data.split("Application No. :")[1].split(" IP")[0]
        elif "Application No. " in data:
            appno = data.split("Application No. ")[1].split(" (")[0]
        
        elif "Application No " in data:
            appno = data.split("Application No ")[1].split(" ")[0]
        elif "Appucation No. " in data:
            appno = data.split("Appucation No. ")[1].split(" ")[0]
        elif "Application Number : " in data:
            appno = data.split("Application Number : ")[1].split(" ")[0]
        elif "Application Number " in data:
            appno = data.split("Application Number ")[1].split(" ")[0]
        else:
            appno = None

    except:
        appno = None
        
    try:
        if "Birth) " in data:
            dob = data.split("Birth) ")[1].split(" ")[0]
        elif "Date of " in data:
            dob = data.split("Date of ")[1].split("Birth)")[0]
        elif "Birth " in data:
            dob = data.split("Birth ")[1].split(" ")[0]
        else:
            dob = None
    except:
        dob=None

    try:
        roll = data.split("Roll No. ")[1].split(" ")[0]
    except:
        roll = None

    try:
        candidates_name = data.split("Candidate's Name) ")[1].split(" sae")[0]
    except:
        candidates_name = None

    text_list = [appno, dob, roll,candidates_name]
    return text_list
 
def text_details_jpg(link):
    tmp = None
    # img = Image.open(requests.get(link, stream=True).raw)
    img = Image.open(link)
    data = pytesseract.image_to_string(img)
#     print(data)
    
#     Application_number,dob,roll from data
    try:    
        if "Application No. " in data:
            appno = data.split("Application No. ")[1].split(" (")[0]
        elif "Application No. :" in data:
            appno = data.split("Application No. :")[1].split(" IP")[0]
        elif "Application Number : " in data:
            appno = data.split("Application Number : ")[1].split(" ")[0]
        elif "Application No " in data:
            appno = data.split("Application No ")[1].split(" ")[0]
        elif "Application Number " in data:
            appno = data.split("Application Number ")[1].split(" ")[0]
        else:
            appno = None
    

    except:
        appno = None
        
    try:
        if "Birth) " in data:
            dob = data.split("Birth) ")[1].split(" ")[0]
        elif "Date of " in data:
            dob = data.split("Date of ")[1].split("Birth)")[0]
        elif "Birth " in data:
            dob = data.split("Birth ")[1].split(" ")[0]
        else:
            dob = None
    except:
        dob=None

    try:
        roll = data.split("Roll No. ")[1].split(" ")[0]
    except:
        roll = None

    try:
        candidates_name = data.split("Candidate's Name) ")[1].split(" sae")[0]
    except:
        candidates_name = None

    text_list = [appno, dob, roll,candidates_name]
    return text_list
    
def t_d(file):
    urllib.request.urlretrieve(file[5],file[5].split("/")[4])
    link = file[5].split("/")[4]
    ph_no = file[1]
    
    if link.endswith('.png') :
        
        try:
            output = text_details_jpg(link)
            output.append(ph_no)
            return output
        except:
            return ['img_fail','img_fail','img_fail','img_fail',ph_no] 
    elif link.endswith('.jpg') :
        
        try:
            output = text_details_jpg(link)
            output.append(ph_no)
            return output
        except:
            return ['img_fail','img_fail','img_fail','img_fail',ph_no] 
    elif link.endswith('.jpeg') :
        
        try:
            output = text_details_jpg(link)
            output.append(ph_no)
            return output
        except:
            return ['img_fail','img_fail','img_fail','img_fail',ph_no] 
    if link.endswith('.pdf'):
        try:
            
            output =  text_details(link)
            output.append(ph_no)
            return output
        except:
            return ['pdf_fail','pdf_fail','pdf_fail','pdf_fail',ph_no]
    else:
        
        return ['fail','fail','fail','fail',ph_no]
