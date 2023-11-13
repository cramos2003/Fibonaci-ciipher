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
        message = self.findAscii(message)
        firstKey = self.generateKey()
        primes = self.fibPrimes(len(message))
        message = self.fkCipher(firstKey, primes, message)

        message.append(firstKey)

        message = self.convertToUni(message)
        message = self.encryptedMessage(message)

        self.message_to_encrypt.setText('')
        self.output.setText(message)

    def decrypt(self):
        message = self.message_to_decrypt.text()
        message = self.findAscii(message)
        message = self.uniToAscii(message)
        primes = self.fibPrimes(len(message)-1)
        
        for x in range(0, len(primes)):
            primes[x] = primes[x] - primes[x] * 2

        message = self.fkCipherReversed (message[-1]*(-1), primes, message)
        message = self.decryptedMessage(message)
        
        self.message_to_decrypt.setText('')
        self.output.setText(message)

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

    def fkCipher(self, fk, p, m):
        i = 0
        while i <= len(p)-1:
            p[i] = (fk + p[i]) % 256
            i += 1
        print('Fibbonaci Primes With First Key: ', p)
        i = 0
        while i <= len(p)-1:
            m[i] = m[i] + p[i]
            i += 1
        print('Ascii vals after primes + message values: ', m)
        return m

    def fkCipherReversed(self, fk, p, m):
        for i in range(0, len(m) - 1):
            m[i] = (m[i] + p[i] + fk) % 256
            if m[i] < 0: m[i] = 0
            m[i] = chr(m[i])
        m.pop(-1)
        return m

    def convertToUni(self, m):
        for i in range(0, len(m)-1):
            tempList = []
            item = str(m[i])
            if len(item) < 3 : item = '0' + item # FOR 2 DIGIT NUMBERS
            for c in range(0, 3):
                tempList.append(int(item[c]) + 30)
            m[i] = tempList
        del tempList
        print('Equivilent int unicode values: ', m)
        return m

    def encryptedMessage(self, m):
        for i in range(0, len(m) - 1):
            for c in range(0, 3):
                m[i][c] = chr(m[i][c])
        print('Encrypted character list with first key tag: ', m)

        temp = ''
        tagHolder = m[-1]
        for i in range(0, len(m)-1):
            for c in range(0, 3):
                temp = temp + str(m[i][c])
        m = temp
        m = str(m) + str(chr(tagHolder))
        del temp
        del tagHolder
        print('Final encrypted message: ', m)
        return m

    def decryptedMessage(self, m):
        temp = ''
        for i in range(0, len(m)):
            temp = temp + m[i]
        m = temp
        del temp
        return m

    def uniToAscii(self, m):
        firstKeyHolder = m[-1]

        for i in range(0, len(m)-1):
            m[i] = m[i] - 30
        print('Ascii equivilent values: ', m)

        # COMBINE EVERY 3 NUMBERS WITHIN LIST EXCEPT LAST ITEM
        for i in range(0, int((len(m) - 1) / 3)):
            groupIndex = i * 3 # GROUPS EVERY 3 ITEMS FOR INDEX PORPOSES
            temp = ''
            c = 0
            while c < 3:
                temp = temp + str(m[groupIndex + c])
                c += 1
            m[groupIndex] = int(temp)
        del temp
        m = [x for x in m if x > 9]
        if firstKeyHolder < 10: m.append(firstKeyHolder)
        del firstKeyHolder
        print('Combine integer values: ', m)
        return m

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()