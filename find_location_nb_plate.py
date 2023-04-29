import cv2


class PyImageSearchANPR:
    def __init__(self, minAR=2.7, maxAR=3.5, debug=False):
        self.minAR = minAR
        self.maxAR = maxAR
        self.debug = debug

    def debug_imshow(self, title, image, waitKey=False):
        if self.debug:
            cv2.imshow(title, image)

            if waitKey:
                cv2.waitKey(0)

    def locate_license_plate_candidates(self, gray, keep=5):
        rectKern = cv2.getStructuringElement(cv2.MORPH_RECT, (19, 9))

        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        mask = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        self.debug_imshow("TMP", mask)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, rectKern)
        self.debug_imshow("Mask", mask)

        # gradX = cv2.Sobel(thresh, ddepth=cv2.CV_16S, dx=1, dy=0)
        # gradY = cv2.Sobel(thresh, ddepth=cv2.CV_16S, dx=0, dy=1)
        #
        # abs_grad_x = cv2.convertScaleAbs(gradX)
        # abs_grad_y = cv2.convertScaleAbs(gradY)
        #
        # grad = cv2.bitwise_or(abs_grad_x, abs_grad_y)
        # self.debug_imshow("Grad tmp", grad)
        # grad = cv2.GaussianBlur(grad, (5, 5), 0)
        # grad = cv2.dilate(grad, rectKern, iterations=2)
        # grad = cv2.erode(grad, rectKern, iterations=2)
        # self.debug_imshow("MORPH_CLOSE tMP", grad)

        # ---------------------------------------------------------------------------------

        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        gradX = cv2.Sobel(blur, ddepth=cv2.CV_16S, dx=1, dy=0)
        gradY = cv2.Sobel(blur, ddepth=cv2.CV_16S, dx=0, dy=1)

        abs_grad_x = cv2.convertScaleAbs(gradX)
        abs_grad_y = cv2.convertScaleAbs(gradY)

        grad = cv2.bitwise_or(abs_grad_x, abs_grad_y)
        # grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        self.debug_imshow("Grad", grad)

        # grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, rectKern)
        grad = cv2.dilate(grad, rectKern, iterations=2)
        grad = cv2.erode(grad, rectKern, iterations=2)
        self.debug_imshow("MORPH_CLOSE", grad)
        # thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        thresh = cv2.threshold(grad, 20, 255, cv2.THRESH_BINARY_INV)[1]
        self.debug_imshow("Grad Thresh", thresh)

        # thresh = cv2.threshold(blur, 210, 255, cv2.THRESH_OTSU )[1]
        # self.debug_imshow("Thresh", thresh)

        min_rectKern = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 5))
        thresh1 = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, min_rectKern)
        # thresh1 = cv2.dilate(thresh, rectKern, iterations=1)
        # thresh1 = cv2.erode(thresh1, rectKern, iterations=1)
        # thresh1 = cv2.erode(thresh1, rectKern, iterations=2)
        # thresh1 = cv2.dilate(thresh1, rectKern, iterations=2)
        self.debug_imshow("Thresh Opened", thresh1)

        masked = cv2.bitwise_and(thresh1, thresh1, mask=mask)
        self.debug_imshow("Masked", masked)

        edged = cv2.Canny(masked, 30, 200)
        # self.debug_imshow("Edged", edged)

        contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        print("Number of Contours found = " + str(len(contours)))
        # print(contours)

        # Draw all contours
        # tmp_cont = []
        # for i in contours:
        #     if len(i) < 10:
        #         tmp_cont.append(i)
        # print(type(contours[0]))
        # print(type(tmp_cont[0]))
        cv2.drawContours(gray, contours, -1, (0, 255, 0), 3)
        self.debug_imshow('Contours Gray', gray)

        return contours

    def locate_license_plate(self, image, candidates):
        success = False
        for c in candidates:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            print('x : ', x, 'y : ', y)
            print('ar : ', ar)
            if self.minAR <= ar <= self.maxAR:
                success = True
                cv2.rectangle(image, (x - 5, y - 5), (x + w + 5, y + h), (0, 255, 0), 2)
                cv2.imshow('Contours', image)
                break
        cv2.waitKey(0)

        return success

    def find(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        candidates = self.locate_license_plate_candidates(gray)
        print('WTF')
        if not self.locate_license_plate(image, candidates):
            print("Cannot find the location of number plate.")


anpr = PyImageSearchANPR(debug=False)

img = cv2.imread('images/5.jpg')
anpr.find(img)
