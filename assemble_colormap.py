import cv2 as cv
import sys
import numpy as np
import colorsys as cs
import os

results = []

pal_num = int(sys.argv[1])

if len(sys.argv) == 3:
    light_exp = float(sys.argv[2])
else:
    light_exp = 1.4

if not os.path.isdir("results"):
    os.mkdir("results")

def selectLight(light):
    smalldist = 1
    selectcol = palette[0][0]
    palcol = [0, 0, 0]
    for x in range(0, palette.shape[0]):
        for y in range(0, palette.shape[1]):
            palcol = palette[x][y]
            palcol = cs.rgb_to_hls(palcol[0] / 255, palcol[1] / 255, palcol[2] / 255)
            dist = abs(light - palcol[1])
            if dist < smalldist:
                smalldist = dist
                selectcol = palette[x][y]
    return selectcol

for color_ramp_id in range(1, pal_num+1):
    ramp = cv.imread("range"+str(color_ramp_id)+"0000.png")
    palette = cv.imread("cmap"+str(color_ramp_id)+"0000.png")

    result = np.zeros((32,ramp.shape[1],3), np.uint8)

    for x in range(0, ramp.shape[1]):
        base = ramp[0][x]
        result[0][x] = base
        for y in range(1, 32):
            amount = y/32
            invamount = 1 - amount

            newcol = [0, 0, 0]

            base_hls = cs.rgb_to_hls(base[0] / 255, base[1] / 255, base[2] / 255)

            light = base_hls[1] * (0-(invamount-2*(pow(invamount, 1/light_exp))))

            newcol = selectLight(light)
            result[y][x] = newcol

    cv.imwrite("results/result"+str(color_ramp_id)+".png", result);
    results.append(result)

cv.imwrite("results/complete.png", cv.hconcat(results))
