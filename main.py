import datetime
import secrets
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QSpinBox, QLabel, QButtonGroup, \
    QRadioButton, QPushButton, QDialog
from PyQt6.QtCore import Qt

system_random = secrets.SystemRandom()


class WindowWidget(QWidget):
    def __init__(self):
        super().__init__()

        outerlayout = QVBoxLayout(self)
        layout = QHBoxLayout(self)
        buttonlayout = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)

        self.lotteryNum_label = QLabel("How many tickets do you want?")
        self.sp = QSpinBox()
        self.sp.setMinimum(1)
        self.sp.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(self.lotteryNum_label)
        layout.addWidget(self.sp)

        radiob = [QRadioButton("Cash 4 Life"), QRadioButton("Mega Millions"), QRadioButton("Powerball")]
        radiob[0].setChecked(True)

        self.button_group = QButtonGroup()
        for i in range(len(radiob)):
            buttonlayout.addWidget(radiob[i])
            self.button_group.addButton(radiob[i], i)

        self.submitbutton = QPushButton("Generate", self)
        self.submitbutton.clicked.connect(self.startpicking)
        layout3.addWidget(self.submitbutton)

        outerlayout.addLayout(layout)
        outerlayout.addLayout(buttonlayout)
        outerlayout.addLayout(layout3)

        self.dialog = QDialog()
        self.dialog_layout = QVBoxLayout(self.dialog)

        self.setLayout(outerlayout)
        self.initUI()

    def initUI(self):
        self.resize(400, 350)
        self.setWindowTitle("Lottery Number Generator")

    def showModal(self):
        self.dialog.setWindowTitle(f"{self.button_group.checkedButton().text()} - Ticket Number ({self.sp.value()})")
        self.dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.dialog.resize(300, 300)

        self.dialog.setLayout(self.dialog_layout)
        self.dialog.exec()

    def startpicking(self):
        prompt_user_num_ticket = self.sp.value()
        prompt_user_ticket_type = self.button_group.checkedButton().text()

        curr_date_time = datetime.datetime.now()
        date_n_time = datetime.datetime.strftime(curr_date_time, "%B %d, %Y | %I:%M %p")

        with open("previous_generated.txt", "a") as file:
            file.write("\n" + date_n_time + " || " + prompt_user_ticket_type + "\n")

        for _ in range(prompt_user_num_ticket):
            self.makenum(prompt_user_ticket_type)

        self.showModal()

        with open("previous_generated.txt", "a") as file:
            file.write("\n")

    def makenum(self, tickettype):
        list_num = []

        num_end = 0
        rand_powerball = 0

        cash_pwrball = 4
        cash_num = 60
        mm_pwrball = 25
        mm_num = 70
        power_pwrball = 26
        power_num = 69

        if tickettype == "Cash 4 Life":
            rand_powerball = system_random.randint(1, cash_pwrball)
            num_end = cash_num
        elif tickettype == "Mega Millions":
            rand_powerball = system_random.randint(1, mm_pwrball)
            num_end = mm_num
        elif tickettype == "Powerball":
            rand_powerball = system_random.randint(1, power_pwrball)
            num_end = power_num

        for _ in range(5):
            rand_num = system_random.randint(1, num_end)

            while rand_num in list_num:
                rand_num = system_random.randint(1, num_end)

            list_num.append(rand_num)

        list_num.sort()
        list_num.append(rand_powerball)

        with open("previous_generated.txt", "a") as file:
            str_list_num = ""

            for a in range(len(list_num)):

                if list_num[a] < 10:
                    list_num[a] = "0" + str(list_num[a])

                str_list_num += str(list_num[a])
                str_list_num += " "
            file.write(str_list_num + "\n")

        d2 = QLabel(str_list_num)
        self.dialog_layout.addWidget(d2)
        return


def main():
    app = QApplication(sys.argv)
    widget = WindowWidget()
    widget.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
