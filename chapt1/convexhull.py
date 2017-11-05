#! /usr/bin/env python
# -*- coding: utf-8 -*-



from __future__ import division

import sys, random
sys.path.append('/mypath/scriptlib')
from  coordWidget import CoordWidget
from PyQt4.Qt import Qt
from PyQt4.QtGui import QApplication, QWidget
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QPointF, QLine, QLineF
from PyQt4.QtGui import QColor, QMatrix, QTransform, QPolygonF
import numpy as np
from PIL import Image
import StringIO

# return QPolygonF
def makeConvexHull(vertexs):
    poly = QPolygonF()

    return poly



class ConvexHull(CoordWidget):
    def __init__(self):
        super(ConvexHull, self).__init__()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Mkake Polygon ')
        self.vertexs = []   #world  pos
        self.points = []    # screen pos
        self.polygon = QPolygonF()
        self.images = []

    def mouseMoveEvent(self, e):
        newPos = e.pos()
        if (self.lastPos - newPos).manhattanLength() < 1:
            self.lastPos = newPos
            return
        if e.buttons() & Qt.RightButton :
            translation = self.screenToWorld(newPos) - self.screenToWorld(self.lastPos)
            self.scene_translation_ = self.scene_translation_ + translation
        elif e.buttons() & Qt.LeftButton:
            pass
        self.lastPos = e.pos()
        self.update()

    def mousePressEvent(self, qMousePressEvent):
        e = qMousePressEvent
        if e.buttons() & Qt.LeftButton :
            vertex = self.screenToWorld( e.pos())  # QPointF
            self.vertexs.append(vertex)
            self.points.append(e.pos())
            self.take_screenshot()
        self.lastPos = e.pos()
        self.update()

    # save QImage to PIL image
    def take_screenshot(self):
        qPixmap = QtGui.QPixmap.grabWindow(self.winId())
        qImage = qPixmap.toImage()
        qBuffer = QtCore.QBuffer()
        qBuffer.open(QtCore.QIODevice.ReadWrite)
        qImage.save(qBuffer, "PNG")
        strio = StringIO.StringIO()
        strio.write(qBuffer.data())
        qBuffer.close()
        strio.seek(0)
        pil_im = Image.open(strio)
        self.images.append(pil_im)


    def saveGIF(self):
        img = self.images[0]
        img.save("aaaaaaaaaaaaaa.gif", save_all=True, append_images=self.images)

    def keyPressEvent(self, keyEvent):
        e = keyEvent
        if e.key() == Qt.Key_C:
            self.polygon = makeConvexHull(self.vertexs)
        # elif e.key() == Qt.Key_P:
        #     self.take_screenshot()
        elif e.key() == Qt.Key_S:
            self.saveGIF()

    def drawInWorld(self, qPainter):
        pen = qPainter.pen()
        pen.setColor(QColor.fromRgb(255, 0, 0))
        # pen.setWidth(3)
        qPainter.setPen(pen)
        # draw  polyline
        # poly = QPolygonF()
        # for v  in self.vertexs:
        #     poly.append(v)
        # qPainter.drawPolyline(poly)

        # draw convex hull
        qPainter.drawPolyline(self.polygon)

        pen.setColor(QColor.fromRgb(0, 0, 255))
        qPainter.setPen(pen)
        # qPainter.drawConvexPolygon(self.qPolygon3)

        # draw in screen
        old_transform = qPainter.worldTransform()
        pen.setWidth(5)
        pen.setColor(QColor.fromRgb(0, 0, 0))
        qPainter.setPen(pen)
        qPainter.resetTransform()
        # draw selected points in screen
        for v in self.points:
            qPainter.drawPoint (v)
        qPainter.setWorldTransform(old_transform)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = ConvexHull()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()