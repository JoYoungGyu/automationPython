import pyautogui
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import mainWindow

# "MR4" = "[M:move or S:Skill][Input Value:실제 눌러야하는 키보드 키(M:상하좌우=UDLR)][Conunt:반복 횟수]"
pattern1 = ["MU1","SZ1"] # for test
teleportKey = "ctrl"

class Worker(QThread):
    # timeout = pyqtSignal(int)    # 사용자 정의 시그널

    def __init__(self):
        super().__init__()
        self.running = False             # 초깃값 설정
        self.pattern = pattern1
        self.idx = 0
        self.maxIdx = len(pattern1)
        self.tele = teleportKey


    def run(self):
        while self.running:
            # self.timeout.emit(self.num)     # 방출
            if (self.pattern[self.idx][0] == "M"):
                for i in range(0, int(self.pattern[self.idx][2:])):
                    match self.pattern[self.idx][1]:
                        case "U": self.mvUD("up")
                        case "D": self.mvUD("down")
                        case "L": pyautogui.press("left")
                        case "R": pyautogui.press("right")
                        

            elif (self.pattern[self.idx][0] == "S"):
                for i in range(0, int(self.pattern[self.idx][2:])):
                    pyautogui.press(self.pattern[self.idx][1])

            else:
                print("Error!!")


            self.idx+=1
            if (self.idx >= self.maxIdx): self.idx = 0
            self.sleep(1)

    def excute(self):
        self.running = True

    def finish(self):
        self.running = False
        self.idx = 0

    def mvUD(self, dir):
        pyautogui.keyDown(dir)
        pyautogui.keyDown(self.tele)
        pyautogui.keyUp(self.tele)
        pyautogui.keyUp(dir)

#화면을 띄우는데 사용되는 Class 선언
# class MyWindow(QMainWindow, mainWindow.Ui_MainWindow):
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker = Worker()
        self.worker.start()

        # UI 선언
        main_ui = mainWindow.Ui_MainWindow()
        # UI 준비
        main_ui.setupUi(self)
        # 화면을 보여준다.
        self.show()

        # 시그널-슬롯 연결하기
        main_ui.goBtn.clicked.connect(self.go)
        main_ui.stopBtn.clicked.connect(self.stop)

    def go(self):
        self.worker.excute()
        self.worker.start()

    def stop(self):
        self.worker.finish()

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = MyWindow() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
