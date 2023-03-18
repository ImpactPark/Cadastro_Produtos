from PyQt5 import uic,QtWidgets

def chama_segunda_tela():
    tela_login.label_4.setText("")
    nome_usuario = tela_login.lineEdit.text()
    senha = tela_login.lineEdit_2.text()
    if nome_usuario == "admin" and senha ==  "admin":
        tela_login.close()
        menu_principal.show()