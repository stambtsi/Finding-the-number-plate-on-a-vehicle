import cv2


class PyImageSearchANPR:
    def __init__(self, minAR=2.1, maxAR=4, debug=False):
        self.minAR = minAR
        self.maxAR = maxAR
        self.debug = debug

    def debug_imshow(self, title, image, waitKey=False):
        if self.debug:
            cv2.imshow(title, image)

            if waitKey:
                cv2.waitKey(0)

    def locate_license_plate_candidates(self, gray, keep=5):
        rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 9))
        min_rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        mask = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)[1]
        self.debug_imshow("TMP", mask)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, rect_kern)
        self.debug_imshow("Mask", mask)

        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        grad_x = cv2.Sobel(blur, ddepth=cv2.CV_16S, dx=1, dy=0)
        grad_y = cv2.Sobel(blur, ddepth=cv2.CV_16S, dx=0, dy=1)

        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)

        grad = cv2.bitwise_or(abs_grad_x, abs_grad_y)
        # grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        self.debug_imshow("Grad", grad)

        grad = cv2.morphologyEx(grad, cv2.MORPH_OPEN, min_rect_kern)
        grad = cv2.dilate(grad, rect_kern, iterations=2)
        grad = cv2.erode(grad, rect_kern, iterations=2)
        self.debug_imshow("MORPH_CLOSE", grad)

        thresh = cv2.threshold(grad, 27, 255, cv2.THRESH_BINARY_INV)[1]
        self.debug_imshow("Grad Thresh", thresh)

        thresh1 = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, min_rect_kern)
        self.debug_imshow("Thresh Opened", thresh1)

        masked = cv2.bitwise_and(thresh1, thresh1, mask=mask)
        self.debug_imshow("Masked", masked)

        edged = cv2.Canny(masked, 30, 200)

        contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)


        # Draw all contours
        cv2.drawContours(gray, contours, -1, (0, 255, 0), 3)
        self.debug_imshow('Contours Gray', gray)

        return contours

    def locate_license_plate(self, image, candidates):
        success = False
        for c in candidates:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)

            if self.debug:
                print('x : ', x, 'y : ', y)
                print('ar : ', ar)

            if self.minAR <= ar <= self.maxAR and x > 415 and y > 250:
                success = True
                cv2.rectangle(image, (x - 5, y - 5), (x + w + 5, y + h), (0, 255, 0), 2)
                break

        return success

    def find(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        candidates = self.locate_license_plate_candidates(gray)
        if not self.locate_license_plate(image, candidates):
            print("Cannot find the location of number plate.")


anpr = PyImageSearchANPR(debug=False)
# img = cv2.imread(f'images/62.jpg')
# anpr.find(img)
# cv2.imshow('Final', img)
# cv2.waitKey(0)

# for i in range(0, 100):
#     img = cv2.imread(f'images/{i}.jpg')
#     anpr.find(img)
#     cv2.imwrite(f'images_out/{i}.jpg', img)

