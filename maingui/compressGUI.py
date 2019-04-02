#!/usr/bin/enc python
# -*- coding: UTF-8 -*-

# @File: compressGUI.py
# @Time: 2019-3-11 9:28

'''
    压缩工具主界面功能实现文件
'''

from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
import os

from resource.compressUtl import Ui_MainWindow


class CompressFiles(QtWidgets.QMainWindow, Ui_MainWindow):
    __slots__ = ('fileUrl', 'dirUrl', 'fileKind')
    def __init__(self, parent=None):
        super(CompressFiles, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle('文件压缩工具')
        self.setFixedSize(1000, 440)

    def choiseFileOrDir(self):
        '''
        选择文件/文件目录按钮事件
        获取相应的文件路径或者文件目录路径
        :return:
        '''

        # 判断待压缩文件类型: jsFileKind->js文件; cssFIleKind->css文件； spriteKind->image文件
        jsFileKind = self.jsRadio.isChecked()
        cssFileKind = self.cssRadio.isChecked()
        spriteKind = self.spriteRadio.isChecked()

        # 判断是压缩单文件还是文件目录（多文件）: true->单文件；false->文件目录（多文件）
        fileOrDir = self.fileRadio.isChecked()

        # 默认路径
        defaultPath = 'C://'

        # 先判断是文件还是文件目录
        if fileOrDir:
            if jsFileKind:
                fileStyle = '*.js'
                self.fileKind = 'js'
            elif cssFileKind:
                fileStyle = '*.css'
                self.fileKind = 'css'
            elif spriteKind:
                fileStyle = '*.png'
                self.fileKind = 'png'
            else:
                fileStyle = '*.html'
                self.fileKind = 'html'
            fileInfo = QFileDialog.getOpenFileUrl(self, 'Open File', defaultPath, fileStyle)
            fileUrl = fileInfo[0].toString()
            if fileUrl == '':
                return
            self.fileUrl = fileUrl.replace('file:///', '')

            self.choiseRstLabel.show()
            self.choiseRstLabel.setText('选择的文件：%s' % self.fileUrl)

            self.outputDirInput.setText(os.path.dirname(self.fileUrl) + '/dist/' + self.fileKind + '/')

        else:
            if self.jsRadio.isChecked():
                self.fileKind = 'js'
            elif self.cssRadio.isChecked():
                self.fileKind = 'css'
            elif self.spriteRadio.isChecked():
                self.fileKind = 'png'
            fileInfo = QFileDialog.getExistingDirectoryUrl(self)
            dirUrl = fileInfo.toString()
            if dirUrl == '':
                return
            self.dirUrl = dirUrl.replace('file:///', '')

            self.choiseRstLabel.show()
            self.choiseRstLabel.setText('选择的文件目录：%s' % self.dirUrl)

            self.outputDirInput.setText(self.dirUrl + '/dist/' + self.fileKind + '/')

    def changeFileKind(self):
        '''
        切换文件类型时，清空相关展示信息
        :return:
        '''
        self.choiseRstLabel.hide()
        self.outputDirInput.setText('')

        if self.jsRadio.isChecked() or self.cssRadio.isChecked():
            self.dirUrl = ''
            self.fileUrl = ''
        if self.spriteRadio.isChecked():
            self.dirUrl = ''
            self.fileUrl = ''
            self.fileRadio.setDisabled(True)
            self.dirRadio.setChecked(True)
            self.dirRadio.setDisabled(True)
        else:
            self.fileRadio.setDisabled(False)
            self.fileRadio.setChecked(True)
            self.dirRadio.setChecked(False)
            self.dirRadio.setDisabled(False)
        if self.fileRadio.isChecked():
            self.dirUrl = ''
        if self.dirRadio.isChecked():
            self.fileUrl = ''

    def choiseOutputDir(self):
        '''
        选择压缩文件生成的存放目录
        :return:
        '''
        dirUrl = QFileDialog.getExistingDirectoryUrl(self)
        outputDirUrl = dirUrl.toString()
        if outputDirUrl == '':
            return
        self.outputDirInput.setText(outputDirUrl.replace('file:///', '') + '/dist/' + self.fileKind + '/')

    def beginCompress(self):
        '''
        开始压缩所选文件
        根据路径输出框填写的信息，将文件生成到指定目录下
        :return:
        '''

        self._componentsDisable(True)

        # 生成地址配置文件
        try:
            with open(r'../fileConfig.json', 'w', encoding='utf-8') as f:
                if self.fileUrl != '':
                    fileCfg =  '{"fileUrl"' + ':"' + self.fileUrl + '", ' + '"outputDir"' + ':"' +  self.outputDirInput.toPlainText() + '"}'
                    f.write(fileCfg)
                elif self.dirUrl != '':
                    dirCfg = '{"dirUrl"' + ':"' + self.dirUrl + '", ' + '"outputDir"' + ':"' + self.outputDirInput.toPlainText() + '"}'
                    f.write(dirCfg)
        except IOError as e:
            print('生成配置文件发生错误：' + e.message)
            self._componentsDisable(False)

        if self.fileKind == 'js':
            if self.fileUrl != '':
                self._compressOrder('gulp prodSingleJs')
            elif self.dirUrl != '':
                self._compressOrder('gulp prodMultyJs')
        elif self.fileKind == 'css':
            if self.fileUrl != '':
                self._compressOrder('gulp prodSingleCss')
            elif self.dirUrl != '':
                self._compressOrder('gulp prodMultyCss')
        elif self.fileKind == 'png':
            if self.dirUrl != '':
                # self._compressOrder('gulp prodPngs')
                self._compressOrder('gulp prodCompressImgs')
    def _compressOrder(self, orderStr):
        '''
        gulp 执行命令封装
        :param orderStr:
        :return:
        '''
        try:
            if orderStr == '' or orderStr == None:
                return
            rst = os.system(orderStr)
            if rst == 0:
                self._componentsDisable(False)
                print('恭喜...执行的操作已完成!!！')
        except Exception as e:
            print('抱歉...执行时发生错误：' + e.message)

    def _componentsDisable(self, isTure):
        '''
        压缩过程中，禁用所有可点击，可输入组件
        :return:
        '''
        self.jsRadio.setDisabled(isTure)
        self.cssRadio.setDisabled(isTure)
        self.spriteRadio.setDisabled(isTure)
        self.fileRadio.setDisabled(isTure)
        self.dirRadio.setDisabled(isTure)
        self.choiseFileDirBtn.setDisabled(isTure)
        self.outputDirInput.setDisabled(isTure)
        self.outputDirBtn.setDisabled(isTure)
        self.compressBtn.setDisabled(isTure)
