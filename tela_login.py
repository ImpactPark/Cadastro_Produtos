from PyQt5 import uic,QtWidgets

def chama_menu_principal():
    tela_login.label_5.setText("")
    nome_usuario = tela_login.lineEdit.text()
    senha = tela_login.lineEdit_2.text()
    if nome_usuario == "admin" and senha ==  "admin":
        tela_login.close()
        menu_principal.show()
    else :
        tela_login.label_5.setText("Dados de login incorretos!")


def logout():
    menu_principal.close()
    tela_login.show()


app=QtWidgets.QApplication([])
tela_login = uic.loadUi("tela_login.ui")
menu_principal = uic.loadUi("menu_principal.ui")
tela_login.pushButton_2.clicked.connect(chama_menu_principal)
menu_principal.pushButton_3.clicked.connect(logout)
tela_login.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)


tela_login.show()
app.exec()

