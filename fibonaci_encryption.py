import sys
import random
from sympy import isprime
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Message Encryption and Decryption Application')

        self.layout_container = QVBoxLayout()

        self.title = QLabel('Enter message to encrypt or decrypt: ')
        self.encrypt_btn = QPushButton('Encrypt')
        self.decrypt_btn = QPushButton('Decrypt')
        self.output_label = QLabel('Output:')
        self.output = QLabel('')

        self.message_to_encrypt = QLineEdit()
        self.message_to_decrypt = QLineEdit()

        self.encrypt_btn.clicked.connect(self.encrypt)
        self.decrypt_btn.clicked.connect(self.decrypt)
        self.output.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse) # ALLOWS ENCRYPTED / DECRYPTED TEXT OUTPUT TO BE HIGHLIGHTABLE FOR ABILITY TO COPY

        self.layout_container.addWidget(self.title)
        self.layout_container.addWidget(self.message_to_encrypt)
        self.layout_container.addWidget(self.encrypt_btn)
        self.layout_container.addWidget(self.message_to_decrypt)
        self.layout_container.addWidget(self.decrypt_btn)
        self.layout_container.addWidget(self.output_label)
        self.layout_container.addWidget(self.output)

        widget = QWidget()
        widget.setLayout(self.layout_container)
        self.setCentralWidget(widget)

    def encrypt(self): # FUNCITON ENCRYPTS USING CAESAR CIPHER AND FIBONACI METHOD FOR EXTRA LAYER OF PROTECTION
        message = self.message_to_encrypt.text()
        print('Original message: ', message)
        message = self.findAscii(message)
        print('Message in ascii form: ', message)
        firstKey = self.generateKey()
        print('First key value: ', firstKey)
        primes = self.fibPrimes(len(message))
        print('Fibbonaci Primes: ', primes)

        # PUT IN FUNCTION
        i = 0
        while i <= len(primes)-1:
            primes[i] = (firstKey + primes[i]) % 256
            i += 1
        print('Fibbonaci Primes With First Key: ', primes)

        # PUT IN FUNCTION
        i = 0
        while i <= len(primes)-1:
            message[i] = message[i] + primes[i]
            i += 1
        print('Ascii vals after primes + message values: ', message)

        message.append(firstKey)
        print("With first key tag: ", message)

        # PUT INTO FUNCTION
        for i in range(0, len(message)-1):
            tempList = []
            item = str(message[i])
            if len(item) < 3 : item = '0' + item # FOR 2 DIGIT NUMBERS
            for c in range(0, 3):
                tempList.append(int(item[c]) + 30)
            message[i] = tempList
        del tempList
        print('Equivilent int unicode values: ', message)

        # PUT INTO FUNCTION
        for i in range(0, len(message) - 1):
            message[i][0] = chr(message[i][0])
            message[i][1] = chr(message[i][1])
            message[i][2] = chr(message[i][2])
        message[-1] = chr(message[-1])
        print('Encrypted character list with first key tag: ', message)

        # PUT INTO A FUNCTION
        temp = ''
        for i in range(0, len(message)-1):
            for c in range(0, 3):
                temp = temp + str(message[i][c])
        message = temp
        del temp
        print('Final encrypted message: ', message)

    def decrypt(self):
        message = self.message_to_decrypt.text()

    def findAscii(self, charArr):
        charArr = list(charArr) #TURNS STRING TO CHARACTER LIST
        i = 0
        while i <= len(charArr)-1:
            charArr[i] = ord(charArr[i])
            i += 1
        return charArr

    def generateKey(self):
        return random.randint(0, 255)
    
    def fibPrimes(self, message_length):
        primes = list()
        a = 0
        b = 1
        while len(primes) < message_length:
            c = a + b
            a = b
            b = c
            if isprime(b) : primes.append(b)
        return primes

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()