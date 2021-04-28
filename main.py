import cv2
import numpy as np
import pytesseract
import os
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/<int:n>')
def armstrong(n):
    s = 0
    order = len(str(n))
    copy_n = n
    while(n>0):
        digit = n%10
        s += digit **order
        n = n//10
    
    if(s == copy_n):
        print(f"{copy_n} is armstrong number")
        result = {
            "Number" : copy_n,
            "Armstrong" : True,
            "Server IP" : "123.154.1234.00"
        }
    else:
        print(f"{copy_n} is not armstrong number")
        result = {
            "Number" : copy_n,
            "Armstrong" : False,
            "Server IP" : "123.154.1234.00"
        }
    
    return jsonify(result)

@app.route('/new')
def textRecog():
        roi = [[(354, 214), (848, 248), 'text', ' Name'], 
            [(353, 321), (851, 359), 'text', ' Name2'], 
            [(352, 433), (848, 472), 'text', ' Email'], 
            [(356, 543), (844, 581), 'text', ' Position']]

        pytesseract.pytesseract.tesseract_cmd = r'D:\\Web Development\\node\\flaskApi\\Tesseract-OCR\\tesseract.exe'

        imQ = cv2.imread('query.png')
        h,w,c= imQ.shape
        #imQ = cv2.resize(imQ,(w//2, h//2))
        orb = cv2.ORB_create(1000)
        kp1, des1 = orb.detectAndCompute(imQ,None)
        #impkp1 = cv2.drawKeypoints(imQ,kp1,None)

    

        img = cv2.imread('test3.jpg')

        #img = cv2.resize(img, (w // 2, h // 2))
        #cv2.imshow(y, img)
        kp2, des2 = orb.detectAndCompute(img, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.match(des2, des1)
        matches.sort(key=lambda x: x.distance)
        good = matches[:100]
        imgMatch = cv2.drawMatches(img,kp2,imQ,kp1,good[:100],None,flags=2)

        # cv2.imshow(y, imgMatch)

        srcPoints = np.float32([kp2[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        dstPoints = np.float32([kp1[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, _ = cv2.findHomography(srcPoints,dstPoints,cv2.RANSAC,5.0)
        imgScan = cv2.warpPerspective(img,M,(w,h))
        # cv2.imshow(y, imgScan)

        imgShow = imgScan.copy()
        imgMask = np.zeros_like(imgShow)

        myData = []

        for x,r in enumerate(roi):

            cv2.rectangle(imgMask, ((r[0][0]), r[0][1]),((r[1][0]), r[1][1]),(255,0,0), cv2.FILLED)
            imgShow = cv2.addWeighted(imgShow, 0.99, imgMask, 0.1, 0)

            imgCrop = imgScan[r[0][1]:r[1][1], r[0][0]:r[1][0]]
            # cv2.imshow(str(x), imgCrop)

            if r[2] == 'text':
                print(f'{r[3]} :{pytesseract.image_to_string(imgCrop)}')
                myData.append(pytesseract.image_to_string(imgCrop))
        
        # with open() as f:
        #     for data in myData:
        #         f.write((str(data)+ ','))
        #     f.write('\n')

        # imgShow = cv2.resize(imgShow, (w // 2, h // 2))
        print(myData)

        return jsonify(myData)

if __name__ == "__main__":
    app.run(debug=True)