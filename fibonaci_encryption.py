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
        charList = list()
        primes = list()
        encryptedMessage = ""

        # FIND ASCII VALUE FOR EACH CHARACTER
        charList = self.findAscii(message)

        # GENERATE KEY FOR ENCRYPTION
        numericalKey = self.generateKey()

        # GET FIBONACCI PRIMES
        primes = self.fibPrimes(len(charList))

        #LOOP TO GENERATE FIRST KEY CIPHER
        for i in range(0, len(charList)):
            charList[i] = (numericalKey + primes[i] + charList[i])

        #GENERATES SECOND KEY CIPHER
        charList = self.secondKeyCipher(charList)

        #FIRST KEY TAG
        charList.append(chr(numericalKey))

        #UPDATES OUTPUT LABEL
        
        self.output_label.setText(encryptedMessage.join(charList))

    def decrypt(self):
        pass

    def generateKey(self):
        return random.randint(0, 255)
    
    def secondKeyCipher(self, arr):
        returnList = list()
        for i in range(0,len(arr)):
            item = str(arr[i])
            returnList.append(chr(int(item[0])+30))
            returnList.append(chr(int(item[1])+30))
            returnList.append(chr(int(item[2])+30))
        return returnList

    def findAscii(self, charArr):
        asciiList = list()
        for x in range(0,len(charArr)):
            asciiList.append(ord(charArr[x]))
        return asciiList
    
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