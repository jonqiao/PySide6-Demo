# This is a sample Python script.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys, os, shutil, hashlib
from pathlib import Path
from threading import Thread

from PySide6 import QtWidgets, QtCore, QtGui
from main_ui import Ui_MainWindow


class RmDuplicate:
  def gen_md5(self, datafile):
    with open(datafile, 'rb') as f:
      md5 = hashlib.md5()
      buffer = 8192
      while True:
        chunk = f.read(buffer)
        if not chunk:
          break
        md5.update(chunk)
      return md5.hexdigest()

  def file_remove_same(self, signal_cust, work='C:/Users/Jon/Downloads', pattern='*.mp4'):
    output = []
    finger_print_dict = dict()
    tmpdir = Path(work, 'tmp')
    tmpdir.mkdir(parents=True, exist_ok=True)
    for item in Path(work).rglob(pattern):
      if item.parent == tmpdir:
        continue
      # print(item)
      output.append(str(item))
      signal_cust.signal_str.emit(str(item))
      finger_print = self.gen_md5(item)
      if finger_print_dict.get(finger_print):
        output.append('---> moving to tmp dir...')
        signal_cust.signal_str.emit('---> moving to tmp dir...')
        shutil.move(item, tmpdir)
      else:
        finger_print_dict.setdefault(finger_print, str(item))
    return output


class MySignals(QtCore.QObject):
  # text_print = QtCore.Signal(QtWidgets.QTextBrowser, str)  # not working???
  signal_str = QtCore.Signal(str)


class MainWindow(QtWidgets.QMainWindow):
  def __init__(self):
    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.ui.actionOpenFile.triggered.connect(self.open_file_action)
    self.ui.lineEdit.returnPressed.connect(self.open_file_action)
    self.lienEditAction = QtGui.QAction(self, 'Open Directory')
    self.lienEditAction.triggered.connect(self.open_file_action)
    self.ui.lineEdit.addAction(self.lienEditAction, QtWidgets.QLineEdit.TrailingPosition)
    self.ui.pushButton.clicked.connect(self.click_button_action)
    self.global_ms = MySignals()
    # self.global_ms.text_print.connect(self.printToGui)
    self.global_ms.signal_str.connect(self.append_signal_str)

  @QtCore.Slot()
  def printToGui(self, fb, text):
    print('-------printToGui-------')
    print(text)
    fb.append(str(text))
    fb.ensureCursorVisible()

  @QtCore.Slot()
  def append_signal_str(self, text):
    print('-------append_signal_str-------')
    print(text)
    self.ui.textBrowser.append(text)
    self.ui.textBrowser.ensureCursorVisible()

  @QtCore.Slot()
  def open_file_action(self):
    dir = QtWidgets.QFileDialog.getExistingDirectory(self, caption='Open Directory', dir='.', options=QtWidgets.QFileDialog.ShowDirsOnly)
    self.ui.lineEdit.setText(dir)

  @QtCore.Slot()
  def click_button_action(self):
    thread = Thread(target=self.rmduplicate)
    thread.start()

  def rmduplicate(self):
    self.global_ms.signal_str.emit('<--- Start ... --->')
    rmd = RmDuplicate()
    output = rmd.file_remove_same(self.global_ms, work=self.ui.lineEdit.text(), pattern=self.ui.comboBox.currentText())
    self.global_ms.signal_str.emit('<--- ... End --->')


if __name__ == '__main__':
  app = QtWidgets.QApplication([])
  mainw = MainWindow()
  mainw.show()
  sys.exit(app.exec())
