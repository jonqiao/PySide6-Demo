# https://stackoverflow.com/questions/67231753/signals-in-pyside6
class Account(QtCore.QThread):
  textUpdate = QtCore.Signal(str)

  def run(self):
    print("thread is work")
    self.textUpdate.emit("Connect to device\n")


if __name__ == "__main__":
    app = QApplication()

    main = MainWindow()
    acc_instance = Account()

    acc_instance.textUpdate.connect(main.update_text)
    main.ui.pushButton.clicked.connect(acc_instance.start)

    main.show()

    sys.exit(app.exec_())