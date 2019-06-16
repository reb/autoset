#!/usr/bin/python3

from matplotlib import pyplot as plt
import numpy as np
import argparse
import cv2
import operator


colour_bands = [
    ('r', [200,50,50])
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('images', nargs='+', help='Path to the image')
    args = vars(parser.parse_args())
    for file in args['images']:
        detect(file)


def plot(file, channel_names, image):
    label = ''.join(channel_names)
    plt.figure()
    plt.title(f'{label} Histogram')
    plt.xlabel('Bins')
    plt.ylabel('# of Pixels')

    image_channels = cv2.split(image)
    for (channel, name) in zip(image_channels, channel_names):
        cv2.imwrite(f'{file}.{label}-{name}.png', channel)

    for i, channel in enumerate(channel_names):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, label=channel)
        plt.xlim([0, 256])
    plt.legend()
    plt.savefig(f'{file}.{label}.png')
    plt.close()


def kill_whitey(image):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    # (y, cr, cb) = cv2.split(ycrcb)
    # hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # (h, s, v) = cv2.split(hsv)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    (l, _, _) = cv2.split(lab)
    # ret, thresh = cv2.threshold(y, 200, 255, cv2.THRESH_BINARY)
    _, thresh = cv2.threshold(l, 180, 255, cv2.THRESH_BINARY)
    return thresh

def hue_to_colour(hue):
    if hue < 20:
        return 'R'
    if hue < 100:
        return 'G'
    return 'B'


def detect(file):
    print(file)
    image = cv2.imread(file)
    # cv2.imshow('image', image)

    # plot(file, ('b', 'g', 'r'), image)
    # plot(file, ('h', 's', 'v'), cv2.cvtColor(image, cv2.COLOR_BGR2HSV))
    # plot(file, ('l', 'a', 'b'), cv2.cvtColor(image, cv2.COLOR_BGR2LAB))
    # plot(file, ('Y', 'Cr', 'Cb'), cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb))

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    thresh = kill_whitey(image)
    mask = cv2.bitwise_not(thresh)

    plt.figure()
    plt.title(f'Masked HSV Histogram')
    plt.xlabel('Bins')
    plt.ylabel('# of Pixels')
    for i, channel in enumerate(('h', 's', 'v')):
        hist = cv2.calcHist([hsv], [i], mask, [256], [0, 256])
        plt.plot(hist, label=channel)
        plt.xlim([0, 256])
    plt.legend()
    plt.savefig(f'{file}.masked.plot.png')
    plt.close()
    
    image[thresh == 255] = 0
    cv2.imwrite(file + '.masked.png', image)

    score = {'R': 0, 'G': 0, 'B': 0}
    for (image_row, mask_row) in zip(hsv, mask):
        for (image_px, mask_px) in zip(image_row, mask_row):
            if mask_px:
                colour = hue_to_colour(image_px[0])
                score[colour] += 1

    print(score)
    print(max(score.items(), key=operator.itemgetter(1))[0])


    # print(masked)
    # plot(file + '2', ('h', 's', 'v'), cv2.cvtColor(masked, cv2.COLOR_BGR2HSV))


if __name__ == "__main__":
    main()




# def histo():
#     color = ('b', 'g', 'r')
#     plt.figure()
#     plt.title("Colour Histogram")
#     plt.xlabel("Bins")
#     plt.ylabel("# of Pixels")
#     for i, color in enumerate(color):
#         hist = cv2.calcHist([image], [i], None, [64], [0, 256])
#         plt.plot(hist)
#         plt.xlim([0, 64])
#     plt.show()

# def inrange():
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 
#     lower_red = np.array([200,50,50]) 
#     upper_red = np.array([255,255,255])

#     mask = cv2.inRange(hsv, lower_red, upper_red)
#     res = cv2.bitwise_and(image, image, mask=mask)
#     cv2.imshow('mask', mask)
#     cv2.imshow('res', res)

#     plt.figure()
#     plt.title("HSV Histogram")
#     plt.xlabel("Bins")
#     plt.ylabel("# of Pixels")

#     color = ('h', 's', 'v')
#     for i, color in enumerate(color):
#         hist = cv2.calcHist([hsv], [i], None, [64], [0, 256])
#         plt.plot(hist, label=color)
#         plt.xlim([0, 64])
#     plt.xlim([0, 64])
#     plt.legend()
#     plt.savefig(f'{args["image"]}.plot.png')
#     plt.show()

#     while True:
#         k = cv2.waitKey(0)
#         if k == 27:         # If escape was pressed exit
#             cv2.destroyAllWindows()
#             break



# inrange()
