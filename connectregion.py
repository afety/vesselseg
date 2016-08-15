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

                        if (m >= 0 and m <= size[0]-1) and (n >= 0 and n <= size[1]-1):
                            if not (m == x and n == y):
                                if pixels[m, n] == 255:
                                    points += 1
                if points == 0:
                    temp.append(0)
                else:
                    temp.append(1)
            pix.append(temp)

        resultimg = img.copy()
        rpixels = resultimg.load()
        for y in xrange(len(pix)):
            for x in xrange(len(pix[0])):
                if pix[y][x] == 1:
                    rpixels[x, y] = 255
                else:
                    rpixels[x, y] = 0
        print '膨胀'
        return resultimg

    # 图片求交集
    def intersectionimgs(self, img1, img2):
        pixels1 = img1.load()
        pixels2 = img2.load()

        for y in xrange(self.size[1]):
            for x in xrange(self.size[0]):
                if pixels1[x, y] != pixels2[x, y]:
                    pixels1[x, y] = 0
        print 'Intersection'
        return img1

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
        return self.intersectionimgs(self.dilation(img), self.img)

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

    # 一遍扫描获取连通区域
    '''储存方式：多维数组，储存连通区域坐标(元组)'''
    def regionext(self):
        result = []
        for y in xrange(self.size[1]):
            for x in xrange(self.size[0]):
                if self.pixels[x, y] == 255:
                    if not self.isin2dlist(result, (x, y)):
                        result.append([(x, y)])
                    index = self.getindex(result, (x, y))
                    for m in xrange(x - self.struw, x + self.struw + 1):
                        for n in xrange(y - self.struh, y + self.struh + 1):
                            if not (m == x and n == y):
                                if self.pixels[m, n] == 255:
                                    if index != -1 and not self.isin2dlist(result, (m, n)):
                                        result[index].append((m, n))
        return result

    # 二维表元素索引
    def getindex(self, list2d, element):
        if list2d == []:
            return 0
        else:
            for m in xrange(len(list2d)):
                for n in xrange(len(list2d[m])):
                    if list2d[m][n] == element:
                        return m
            return -1

    # 二维表中元素检查
    def isin2dlist(self, list2d, element):
        for m in xrange(len(list2d)):
            for n in xrange(len(list2d[m])):
                if list2d[m][n] == element:
                    return True
        return False

# 膨胀测试
if __name__ == "__main__":
    img = Image.open('test.png')
    img.show()
    t = ConnectionRegion(img)
    img = t.dilation(img)
    img.show()