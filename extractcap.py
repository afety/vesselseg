# coding: utf8
from PIL import Image

from otsu import getGray

__author__ = 'tanghan'

''' 微血管提取步骤
    1. (二值图像)形态学腐蚀，消除小血管
    2. 图片异或运算，得小血管坐标
    3. 图片与运算，的的主血管坐标
    4. 小血管角度偏转，或者沿主血管移动
'''

# 腐蚀, 采用矩形结构元
def erosion(binimg, diskradius=1, pointcounts = 6):
    pixels = binimg.load()
    imgsize = binimg.size
    imgpix = []
    for y in xrange(0, imgsize[1]):
        temp = []
        for x in xrange(0, imgsize[0]):
            # 探测的像素点总数
            totalpoints = 0
            # 背景点数
            bgpoints = 0
            for m in xrange(x-diskradius, x+diskradius+1):
                for n in xrange(y-diskradius, y+diskradius+1):
                    if (m >= 0 and m <= imgsize[0]-1) and (n >= 0 and n <= imgsize[1]-1) and (m != x and n != y):
                        totalpoints = totalpoints + 1
                        if pixels[m, n] == 0:
                            bgpoints = bgpoints + 1
            if bgpoints >= pointcounts:
                temp.append(0)
            else:
                temp.append(1)
        imgpix.append(temp)
    tempimg = getGray('template.png').resize((imgsize[0], imgsize[1]))

    pixels = tempimg.load()
    for y in xrange(0, len(imgpix)):
        for x in xrange(0, len(imgpix[0])):
            if imgpix[y][x] == 0:
                pixels[x, y] = 0
            else:
                pixels[x, y] = 255
    return tempimg

# 形态学 膨胀操作
def dilation(binimg, diskradius=1, pointcounts=6):


# 异或运算， 获取小血管坐标
def xor_extractcap(originimg, erosimg):
    originimg.show()
    erosimg.show()
    o_pixels = originimg.load()
    e_pixels = erosimg.load()
    imgsize = originimg.size
    pix = []
    for y in xrange(imgsize[1]):
        temp = []
        for x in xrange(imgsize[0]):
            if e_pixels[x, y] == 255 and o_pixels == 0:
                temp.append(1)
            else:
                temp.append(0)

        pix.append(temp)

    for y in xrange(0, len(pix)):
        for x in xrange(0, len(pix[0])):
            if pix[y][x] == 0:
                e_pixels[x, y] = 0
            else:
                e_pixels[x, y] = 255
    return erosimg

# 去噪点
def removenoise(binaryimg):
    binaryimg.show()
    pixels = binaryimg.load()
    imgsize = binaryimg.size
    radius = 1
    pix = []
    for y in xrange(imgsize[1]):
        temp = []
        for x in xrange(imgsize[0]):
            if pixels[x, y] == 255:
                points = 0
                for m in xrange(x-1, x+2):
                    for n in xrange(y-1, y+2):

                        if (m >= 0 and m <= imgsize[0] -1) and (n >= 0 and n <= imgsize[1]-1) and (m != x and n != y):
                            if (m == x and n == y-1) or () or () or ():
                                if pixels[m, n] == 255:
                                    points += 1
                if points >= 2:
                    temp.append(1)
                else:
                    temp.append(0)
            else:
                temp.append(0)
        pix.append(temp)

    for y in xrange(len(pix)):
        for x in xrange(len(pix[0])):
            if pix[y][x] == 0:
                pixels[x, y] = 0
            else:
                pixels[x, y] = 255

    binaryimg.show()

if __name__ == "__main__":
    bimg = getGray("labels-ah/im0001.ah.ppm")
    # pixels = bimg.load()
    # imgsize = bimg.size
    # t = []
    # for x in xrange(imgsize[0]):
    #     s = []
    #     for y in xrange(imgsize[1]):
    #         if pixels[x, y] == 255:
    #             s.append(0)
    #         else:
    #             s.append(1)
    #     t.append(s)
    # with open('test.txt', 'wb') as txtfile:
    #     for x in xrange(len(t)):
    #         for y in xrange(len(t[0])):
    #             txtfile.write(str(t[x][y]))
    #         txtfile.write('\n')
    erosimg = erosion(bimg, diskradius=2)
    erosimg.show()
    # erosimg = xor_extractcap(bimg, erosimg)
    # erosimg = erosion(erosimg, diskradius=1, pointcounts=2)
    # removenoise(erosimg)

