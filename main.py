import cv2
import numpy as np
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

if __name__ == '__main__':
    for i in range(0,3):
        #cargar imagen#
        path = r"C:\Users\Brayan Pedraza\Downloads\Imagenes_proyecto_final\Dir%d.png" % (i+1)
        image = cv2.imread(path)

        #binarización imagen#
        I_YCrCb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
        Y, Cr, Cb = cv2.split(I_YCrCb)
        ret, Ibw_Cb = cv2.threshold(Cr, 50, 200, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        Ibw_Cb_mask = cv2.bitwise_not(Ibw_Cb)
        I_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        #hist_h = cv2.calcHist([I_hsv], [0], Ibw_Cb_mask, [180], [0, 180])
        #plt.plot(hist_h, color='green')
        #plt.xlim([0, 180])
        #plt.show()
        #H_max_pos = int(hist_h.argmax())
        Ibw_H_mask = cv2.inRange(I_hsv, (60, 0, 0), (108, 255, 150))
        H, S, V = cv2.split(I_hsv)
        ret, Ibw_S_mask = cv2.threshold(S, 85, 255, cv2.THRESH_BINARY)
        Ibw_mask = cv2.bitwise_and(Ibw_H_mask, Ibw_S_mask)
        ret, Ibw_V_mask = cv2.threshold(V, 50, 255, cv2.THRESH_BINARY)
        Ibw_mask_f = cv2.bitwise_and(Ibw_mask, Ibw_V_mask)
        cv2.imshow("Filtro final V and S and Filtro amarillo", Ibw_mask_f)
        cv2.waitKey(0)

        text = pytesseract.image_to_string(Ibw_mask_f, config='--psm 12')
        nums = re.findall("\d+", text)
        print(text)
        print(f"Calle {nums[0]}")
        print(f"Carrera {nums[1]}")

