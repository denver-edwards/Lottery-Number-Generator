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

        outer_layout = QVBoxLayout(self)
        layout = QHBoxLayout(self)
        button_layout = QHBoxLayout(self)
        layout3 = QHBoxLayout(self)

        self.lotteryNum_label = QLabel("How many tickets do you want?")
        self.sp = QSpinBox()
        self.sp.setMinimum(1)
        self.sp.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(self.lotteryNum_label)
        layout.addWidget(self.sp)

        radio_button = [QRadioButton("Cash 4 Life"), QRadioButton("Mega Millions"),
                        QRadioButton("Powerball"), QRadioButton("Numbers Eve (3)")]
        radio_button[0].setChecked(True)

        self.button_group = QButtonGroup()

        for i in range(len(radio_button)):
            button_layout.addWidget(radio_button[i])
            self.button_group.addButton(radio_button[i], i)

        self.submit_button = QPushButton("Generate", self)
        self.submit_button.clicked.connect(self.start_picking)
        layout3.addWidget(self.submit_button)

        outer_layout.addLayout(layout)
        outer_layout.addLayout(button_layout)
        outer_layout.addLayout(layout3)

        self.dialog = QDialog()
        self.dialog_layout = QVBoxLayout(self.dialog)

        self.setLayout(outer_layout)
        self.init_ui()

    def init_ui(self):
        self.resize(400, 350)
        self.setWindowTitle("Lottery Number Generator")

    def show_modal(self):
        self.dialog.setWindowTitle(f"{self.button_group.checkedButton().text()} - Ticket Number ({self.sp.value()})")
        self.dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.dialog.resize(300, 300)
        self.dialog.setLayout(self.dialog_layout)
        self.dialog.exec()

    def start_picking(self):
        prompt_user_num_ticket = self.sp.value()
        prompt_user_ticket_type = self.button_group.checkedButton().text()

        curr_date_time = datetime.datetime.now()
        date_n_time = datetime.datetime.strftime(curr_date_time, "%B %d, %Y | %I:%M %p")

        with open("previous_generated.txt", "a") as file:
            file.write("\n" + date_n_time + " || " + prompt_user_ticket_type + "\n")

        for _ in range(prompt_user_num_ticket):
            self.make_num(prompt_user_ticket_type)

        self.show_modal()

        with open("previous_generated.txt", "a") as file:
            file.write("\n")

        ticket_container = self.dialog_layout

        for i in reversed(range(ticket_container.count())):
            ticket_container.itemAt(i).widget().deleteLater()

    def make_num(self, ticket_type):
        list_num = []

        num_of_positions = 5

        num_start = 1
        num_end = 0

        rand_powerball = 0

        cash_powerball = 4
        cash_num = 60
        mm_powerball = 25
        mm_num = 70
        power_powerball = 26
        power_num = 69

        daily_game_num = 9

        has_powerball = True

        if ticket_type == "Cash 4 Life":
            rand_powerball = system_random.randint(1, cash_powerball)
            num_end = cash_num
        elif ticket_type == "Mega Millions":
            rand_powerball = system_random.randint(1, mm_powerball)
            num_end = mm_num
        elif ticket_type == "Powerball":
            rand_powerball = system_random.randint(1, power_powerball)
            num_end = power_num
        elif ticket_type == "Numbers Eve (3)":
            rand_powerball = system_random.randint(0, daily_game_num)
            num_end = daily_game_num
            num_of_positions = 3
            num_start = 0
            has_powerball = False

        for _ in range(num_of_positions):
            rand_num = system_random.randint(num_start, num_end)

            while rand_num in list_num:
                rand_num = system_random.randint(num_start, num_end)

            list_num.append(rand_num)
        list_num.sort()

        if has_powerball:
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
        # self.dialog_layout.removeWidget(d2)

        self.dialog_layout.addWidget(d2)
        return


def main():
    app = QApplication(sys.argv)
    widget = WindowWidget()
    widget.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
