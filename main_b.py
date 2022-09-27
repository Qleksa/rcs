import cv2
import time

def findContours(dilatedFrame):
    contours, hierarchy = cv2.findContours(dilatedFrame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    final_contours = []

    # step 1/4
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.1 * perimeter, True)
        if len(approx) == 4:
            area = cv2.contourArea(contour)
            (x, y, w, h) = cv2.boundingRect(approx)
            ratio = w / float(h)
            print(w, h, ratio, area / (w * h))
            if ratio >= 0.8 and ratio <= 1.2 and w >= 30 and w <= 60 and area / (w * h) > 0.4:
                final_contours.append((x, y, w ,h))
    print('final num', len(final_contours))
    if len(final_contours) < 9:
        return []

    # step 2/4
    found = False
    contour_neighbours = {}
    for index, contour in enumerate(final_contours):
        (x, y, w, h) = contour
        contour_neighbours[index] = []
        center_x = x + w / 2
        center_y = y + h / 2
        radius = 1.5

        neighbour_positions = [
            # top left
            [(center_x - w * radius), (center_y - h * radius)],
            # top middle
            [center_x, (center_y - h * radius)],
            # top right
            [(center_x + w * radius), (center_y - h * radius)],
            # left
            [(center_x - w * radius), center_y],
            # center
            [center_x, center_y],
            # right
            [(center_x + w * radius), center_y],
            # bottom left
            [(center_x - w *radius), (center_y + h * radius)],
            # bottom middle
            [center_x, (center_y + h * radius)],
            # bottom right
            [(center_x + w * radius), (center_y + h * radius)]
        ]

        for neighbour in neighbour_positions:
            (x2, y2, w2, h2) = neighbour
            for (x3, y3) in neighbour_positions:
                if (x2 < x3 and y2 < y3) and (x2 + w2 > x3 and y2 + h2 > y3):
                    contour_neighbours[index].append(neighbour)

    # step 3/4
    for (contour, neighbours) in contour_neighbours.items():
        if len(neighbours) == 9:
            found = True
            final_contours = neighbours
            break

    if not found:
        return []

    # step 4/4
    y_sorted = sorted(final_contours, key=lambda item: item[1])

    top_row = sorted(y_sorted[0:3], key=lambda item: item[0])
    middle_row = sorted(y_sorted[4:6], key=lambda item: item[0])
    bottom_row = sorted(y_sorted[7:9], key=lambda item: item[0])

    sorted_contours = top_row + middle_row + bottom_row
    return sorted_contours

def drawContours(frame, contours):
    for index, (x, y, w, h) in enumerate(contours):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (36, 255, 12), 2)

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    prevTime = 0

    while True:
        time.sleep(0.5)
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow('frame', frame)
        
        key = cv2.waitKey(10) & 0xFF
        # escape
        if key == 27:
            break

        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('gray', grayFrame)
        #blurredFrame = cv2.blur(grayFrame, (5, 5))
        #cv2.imshow('blur', blurredFrame)
        cannyFrame = cv2.Canny(grayFrame, 40, 60, 3)
        cv2.imshow('canny', cannyFrame)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        dilatedFrame = cv2.dilate(cannyFrame, kernel)
        cv2.imshow('dilate', dilatedFrame)

        contours = findContours(dilatedFrame)
        if len(contours) == 9:
            drawContours(frame, contours)

    cam.release()
    cv2.destroyAllWindows()
