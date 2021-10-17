# This is a sample Python script.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys, os, shutil, hashlib
from pathlib import Path
from PySide6 import QtWidgets, QtCore, QtGui
from ui_main import Ui_MainWindow


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

  def file_remove_same(self, textbrowser, work='C:/Users/Jon/Downloads', pattern='*.mp4'):
    output = []
    finger_print_set = set()
    tmpdir = Path(work, 'tmp')
    tmpdir.mkdir(parents=True, exist_ok=True)
    for item in Path(work).rglob(pattern):
      if item.parent == tmpdir:
        continue
      # print(item)
      textbrowser.append(str(item))
      output.append(str(item))
      finger_print = self.gen_md5(item)
      if finger_print in finger_print_set:
        # os.remove(item)
        # print('moving to tmp dir...')
        textbrowser.append('--- ---> moving to tmp dir...')
        output.append('--- ---> moving to tmp dir...')
        shutil.move(item, tmpdir)
      else:
        finger_print_set.add(finger_print)
    return output


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

  def open_file_action(self):
    dir = QtWidgets.QFileDialog.getExistingDirectory(self, caption='Open Directory', dir='.', options=QtWidgets.QFileDialog.ShowDirsOnly)
    self.ui.lineEdit.setText(dir)

  def click_button_action(self):
    rmd = RmDuplicate()
    rmd.file_remove_same(self.ui.textBrowser, work=self.ui.lineEdit.text(), pattern='*.mp4')


if __name__ == '__main__':
  app = QtWidgets.QApplication([])
  mainw = MainWindow()
  mainw.show()
  sys.exit(app.exec())
