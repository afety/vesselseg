#coding:utf8
'''计算连通区域， 并根据条件筛选合适的连通区'''
import Image


class ConnectionRegion:
    def __init__(self, binaryimg):
        if not isinstance(binaryimg, Image.Image):
            print 'ConnectionRegion init must be a binary image'
            exit(-1)
        self.img = binaryimg

        # 图片像素
        self.pixels = self.img.load()
        # 图片尺寸
        self.size = self.img.size

        # 采用矩形结构元
        self.struw = 1
        self.struh = 1

    # 膨胀操作
    def dilation(self, img):

        size = img.size
        pixels = img.load()

        pix = []
        for y in xrange(size[1]):
            temp = []
            for x in xrange(size[0]):
                points = 0
                for m in xrange(x - self.struw, x + self.struw + 1):
                    for n in xrange(y - self.struh, y + self.struh + 1):
                        if (m >= 0 and m <= size[0]-1) and (n >= 0 and n <= size[1]-1) and (m != x and n != y):
                            if pixels[m, n] == 255:
                                points += 1
                if points == 0:
                    temp.append(0)
                else:
                    temp.append(1)
            pix.append(temp)

        resultimg = img.copy()
        for y in xrange(len(pix)):
            for x in xrange(len(pix[0])):
                if pix[y][x] == 1:
                    (resultimg.load())[x, y] = 255
                else:
                    (resultimg.load())[x, y] = 0
        return resultimg

    # 图片求交集
    def intersectionimgs(self, img1, img2):
        resultimg = img2.copy()

        for y in xrange(self.size[1]):
            for x in xrange(self.size[0]):
                if (img1.load())[x, y] == (img2.load())[x, y] == 255:
                    (resultimg.load())[x, y] = 255
                else:
                    (resultimg.load())[x, y] = 0

        print 'Intersection'
        return resultimg

    # 图片相同比对
    def __isequal(self, img1, img2):
        points = 0
        for y in xrange(self.size[1]):
            for x in xrange(self.size[0]):
                if (img1.load())[x, y] != (img2.load())[x, y]:
                    points += 1
        print 'points：', points
        return points == 0

    # 连通区域计算单元
    def __unit(self, img):
        dimg = self.dilation(img)
        A = self.img.copy()
        return self.intersectionimgs(dimg, A)

    # 连通区域计算
    def connectionregion(self):
        img = self.img.copy()
        ass = False
        for y in xrange(self.size[1]):
            for x in xrange(self.size[0]):
                if (img.load())[x, y] == 255 and not ass:
                    (img.load())[x, y] = 255
                    ass = True
                else:
                    (img.load())[x, y] = 0
        k = 0
        while True:
            tempimg = self.__unit(img)
            if self.__isequal(tempimg, img):
                print 'Equal and Exit'
                return tempimg
            img = tempimg
            k += 1
            print '循环次数:', k