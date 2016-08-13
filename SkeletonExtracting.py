#coding:utf8
'''骨架提取算法，用于提取图像骨架并最大程度保证连通性'''
from PIL import Image


class SkeletonExtracting:
    '''结构元采用3阶八连通结构元'''
    def __init__(self, binimg):
        if not isinstance(binimg, Image.Image):
            print 'SkeletonExtracting init must be a binary image'
            exit(-1)
        self.img = binimg
        # 图片信息
        self.pixels = self.img.load()
        # 图片尺寸
        self.size = self.img.size

        self.struw = 1
        self.struh = 1


    # 迭代次数计算
    def iterations(self, img):
        k = 0
        while 1:
            if self.isempty(img):
                return k-1
            img = self.erosion(img)
            k += 1

    # 图片为空集判断
    def isempty(self, img):
        bgpoints = 0
        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if (img.load())[x, y] == 0:
                    bgpoints += 1
        print 'isempty.points:', bgpoints
        print 'size:', (img.size[0])*(img.size[1])
        return bgpoints == (img.size[0])*(img.size[1])

    # 图片腐蚀
    def erosion(self, img):
        size = img.size
        pixels = img.load()

        pix = []
        for y in xrange(size[1]):
            temp = []
            for x in xrange(size[0]):
                bgpoints = 0
                for m in xrange(x - self.struw, x + self.struw + 1):
                    for n in xrange(y - self.struh, y + self.struh + 1):
                        if (m >= 0 and m <= size[0]-1) and (n >= 0 and n <= size[1]-1) and (m != x and n != y):
                            if pixels[m, n] == 0:
                                bgpoints += 1
                if bgpoints == 0:
                    temp.append(1)
                else:
                    temp.append(0)
            pix.append(temp)

        resultimg = img.copy()
        for y in xrange(len(pix)):
            for x in xrange(len(pix[0])):
                if pix[y][x] == 1:
                    (resultimg.load())[x, y] = 255
                else:
                    (resultimg.load())[x, y] = 0
        return resultimg

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

    # 图像开操作
    def openoperation(self, img):
        return self.dilation(self.erosion(img))

    # 迭代腐蚀, k表示迭代次数
    def __iterationerosion(self, img, k=1):
        while k >= 1:
            img = self.erosion(img)
            k -= 1

        return img

    # 图片求差集
    def subtract(self, img1, img2):
        pixels1 = img1.load()
        pixels2 = img2.load()

        size = img1.size
        resultimg = img1.copy()
        for y in xrange(size[1]):
            for x in xrange(size[0]):
                if pixels1[x, y] == pixels2[x, y]:
                    (resultimg.load())[x, y] = 0
        return resultimg

    # 图片求并集
    def unionimgs(self, imglist):
        if len(imglist) <= 1:
            return imglist[len(imglist)-1]
        resultimg = self.img.copy()
        for y in xrange(self.size[1]):
            for x in xrange(self.size[0]):
                points = 0
                for count in xrange(len(imglist)):
                    if (imglist[count].load())[x, y] == 255:
                        points += 1
                if points == 0:
                    (resultimg.load())[x, y] = 0
                else:
                    (resultimg.load())[x, y] = 255

        return resultimg

    # 骨架提取
    def skeletonext(self):
        # 获取迭代层数
        k = self.iterations(self.img)
        print 'iterationcount', k
        # 多次迭代腐蚀结果储存
        sks = []
        for k in xrange(1, k+1):
            img1 = self.__iterationerosion(self.img, k)
            img2 = self.openoperation(self.__iterationerosion(self.img, k))
            sub = self.subtract(img1=img1, img2=img2)
            sks.append(sub)
        return self.unionimgs(imglist=sks)