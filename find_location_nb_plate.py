import numpy as np
import cv2


class PyImageSearchANPR:
    def __init__(self, minAR=2.1, maxAR=4, debug=False):
        # minAR and maxAR define the range within which the ratio of width to height
        # of the number plate will be
        self.minAR = minAR
        self.maxAR = maxAR

        self.debug = debug

    def debug_imshow(self, title: str, image: np.ndarray, waitKey=False):
        if self.debug:
            cv2.imshow(title, image)
            if waitKey:
                cv2.waitKey(0)

    # Create an image to initially separate white objects, to be used later as a mask.
    # Especially useful when processing non-white cars.
    def highlight_white_objects(self, gray: np.ndarray, rect_kern: np.ndarray) -> np.ndarray:
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        mask = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)[1]
        self.debug_imshow("TMP", mask)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, rect_kern)
        self.debug_imshow("Mask", mask)
        return mask

    # Use the gradient and morphology to separate flat objects (without any curves).
    def highlight_flat_objects(self, gray: np.ndarray, rect_kern: np.ndarray) -> np.ndarray:
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        grad_x = cv2.Sobel(blur, ddepth=cv2.CV_16S, dx=1, dy=0)
        grad_y = cv2.Sobel(blur, ddepth=cv2.CV_16S, dx=0, dy=1)

        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)

        grad = cv2.bitwise_or(abs_grad_x, abs_grad_y)
        self.debug_imshow("Grad", grad)

        grad = cv2.morphologyEx(grad, cv2.MORPH_OPEN, rect_kern[:3, :3])
        grad = cv2.dilate(grad, rect_kern, iterations=2)
        grad = cv2.erode(grad, rect_kern, iterations=2)
        self.debug_imshow("MORPH_CLOSE", grad)

        thresh = cv2.threshold(grad, 27, 255, cv2.THRESH_BINARY_INV)[1]
        self.debug_imshow("Grad Thresh", thresh)

        thresh1 = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, rect_kern[:3, :3])
        self.debug_imshow("Thresh Opened", thresh1)
        return thresh1

    def contours_number_plate_candidates(self, gray: np.ndarray) -> list:
        rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 9))

        mask = self.highlight_white_objects(gray, rect_kern)

        flat_obj = self.highlight_flat_objects(gray, rect_kern)

        # After pre-processing the image, apply a mask and search for contours from the resulting image.
        masked = cv2.bitwise_and(flat_obj, flat_obj, mask=mask)
        self.debug_imshow("Masked", masked)

        edged = cv2.Canny(masked, 30, 200)

        contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Draw all contours
        cv2.drawContours(gray, contours, -1, (0, 255, 0), 3)
        self.debug_imshow('Contours Gray', gray)

        return contours

    def highlight_number_plate(self, image: np.ndarray, candidates: list) -> bool:
        success = False
        for c in candidates:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)

            if self.debug:
                print('x : ', x, 'y : ', y)
                print('ar : ', ar)

            # There is a check for the correct ratio rectangle and
            # also a check that the number is in the bottom right corner of the image
            if self.minAR <= ar <= self.maxAR and x > 415 and y > 250:
                success = True
                cv2.rectangle(image, (x - 5, y - 5), (x + w + 5, y + h), (0, 255, 0), 2)
                break

        return success

    def find(self, image: np.ndarray):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        candidates = self.contours_number_plate_candidates(gray)
        if not self.highlight_number_plate(image, candidates):
            print("Cannot find the location of number plate.")


def main(number_images: int):
    print('\nImage processing has begun')
    anpr = PyImageSearchANPR()

    for i in range(0, number_images):
        img = cv2.imread(f'images/{i}.jpg')
        anpr.find(img)
        cv2.imwrite(f'images/{i}.jpg', img)
        if i % 50 == 0:
            print(i, "images have been processed.")
    print('Finally,', number_images, 'images were processed.')
    print('Processing successfully ended!')
