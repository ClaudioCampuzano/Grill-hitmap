import cv2
from matplotlib import pyplot as plt
from time import time



ZONES = []
# para resolucion 1280x720, el grid puede tener tamaños 80, 40, 20, 16, 10, 8, 5,4, 2 ,1
GRID_SIZE = 80
BBOX_COORD = {'left': 321, 'top': 447, 'width': 250, 'height': 173}


def main():
    img = cv2.imread('./car.jpg')
    drawGrid(img, GRID_SIZE)
    drawNumber(img, GRID_SIZE)
    drawBbox(img, BBOX_COORD)
    start_time = time()
    zone_toPint = bboxToZone(BBOX_COORD, GRID_SIZE)
    elapsed_time = (time() - start_time)
    print("Elapsed time: %.10f seconds." % elapsed_time)

    for i in zone_toPint:
        for j in ZONES:
            if i == j[0]:
                coord = j[1]
                blurZone(img, {'left': coord[0][0], 'top': coord[1][0], 'width': GRID_SIZE, 'height': GRID_SIZE})
                break
    
    plt.figure(1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()


def drawGrid(img, step):
    x = step
    y = step
    while x < img.shape[1]:
        cv2.line(img, (x, 0), (x, img.shape[0]), color=(
            255, 0, 255), thickness=1)
        x += step

    while y < img.shape[0]:
        cv2.line(img, (0, y), (img.shape[1], y),
                 color=(255, 0, 255), thickness=1)
        y += step


def drawBbox(img, bbox):
    left = int(bbox['left'])
    top = int(bbox['top'])
    right = int(bbox['left']) + int(bbox['width'])
    bottom = int(bbox['top']) + int(bbox['height'])
    imgHeight, imgWidth, _ = img.shape
    thick = int((imgHeight + imgWidth) // 900)
    cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), thick)


def blurZone(img, bbox):
    left = int(bbox['left'])
    top = int(bbox['top'])
    right = int(bbox['left']) + int(bbox['width'])
    bottom = int(bbox['top']) + int(bbox['height'])

    ROI = img[top:top+int(bbox['height']), left:left+int(bbox['width'])]
    blur = cv2.GaussianBlur(ROI, (51, 51), 0)
    img[top:top+int(bbox['height']), left:left+int(bbox['width'])] = blur


def drawNumber(img, gridSize):
    numerador = 0
    cnt_width = 0
    cnt_height = 0
    imgHeight, imgWidth, _ = img.shape
    for i in range(0, img.shape[1], gridSize):
        for j in range(0, img.shape[0], gridSize):
            left = round((imgHeight/(imgHeight/gridSize))*cnt_height)
            top = round((imgWidth/(imgWidth/gridSize))*cnt_width)
            img = cv2.putText(img, str(numerador), (15+left, 25+top),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
            sup = (left,left+gridSize)
            Inf = (top,top+ gridSize)
            ZONES.append([numerador, (sup,Inf)])
            numerador += 1
            cnt_width += 1
        cnt_width = 0
        cnt_height += 1


def bboxToZone(bbox, gridSize):
    
    right = int(bbox['left']) + int(bbox['width'])
    bottom = int(bbox['top']) + int(bbox['height'])

    bbox_left = range(int(bbox['left']),right+1)
    bbox_top = range(int(bbox['top']),bottom+1)

    zonas_heatmap = []
    for i in ZONES:
        sup_ = i[1][0]
        inf_ = i[1][1]

        grill_left =  set(range(int(i[1][0][0]),int(i[1][0][1])+1))
        grill_top =  set(range(int(i[1][1][0]),int(i[1][1][1])+1))

        porcentaje_left = round(len(grill_left.intersection(bbox_left))/(sup_[1]-sup_[0]+1)*100,1)
        porcentaje_top = round(len(grill_top.intersection(bbox_top))/(inf_[1]-inf_[0]+1)*100,1)

        if porcentaje_left > 40.0 and porcentaje_top >40.0:
            zonas_heatmap.append(i[0])
            #print(i[0], porcentaje_left, porcentaje_top)
    return zonas_heatmap

if __name__ == '__main__':
    main()
