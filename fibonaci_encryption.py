import sys
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
        encrypted_char_list = list()
        encrypted_message = ''
        message = self.message_to_encrypt.text()

        for x in range(0, len(message)): # CODE BLOCK ENCRYPTS EACH CHARACTER
            encrypted_char_list.append(ord(message[x]) + 3)
            encrypted_char_list[x] = (encrypted_char_list[x]-1 + encrypted_char_list[x] +
                                    encrypted_char_list[x]+1 + ord(message[x]))
            encrypted_message = encrypted_message + chr(encrypted_char_list[x])            
        
        self.message_to_encrypt.setText('') # CLEARS message_to_encrypt TEXTBOX
        self.output.setText(encrypted_message) # UPDATES output LABEL TO HOLD ENCRYPTED MESSAGE
        self.update()

    def decrypt(self): # THIS FUNCTION DECRYPTS MESSAGE - MUST BE SAME ENCRYPTION AS APPLICAITON TO DECRYPT
        decrypted_char_list = list()
        decrypted_message = ''
        message = self.message_to_decrypt.text()

        for x in range(0, len(message)): # CODE BLOCK DECRYPTS EACH MESSAGE CHARACTER
            decrypted_char_list.append(ord(message[x]))
            decrypted_char_list[x] = chr(int(((decrypted_char_list[x] -1) / 4)-2))
            decrypted_message = decrypted_message + decrypted_char_list[x]

        self.message_to_decrypt.setText('') # CLEARS message_to_decrypt TEXTBOX
        self.output.setText(decrypted_message) # UPDATES output LABEL TO HOLD DECRYPTED MESSAGE
        self.update()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()