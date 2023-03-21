# Import do modulo uic para leitura do arquivo formulario.ui
# Import do modulo QtWidgetspara montar os elementos na tela
from PyQt5 import uic, QtWidgets
import sqlite3


def chama_menu_principal():
    tela_login.label_5.setText("")
    nome_usuario = tela_login.lineEdit.text()
    senha = tela_login.lineEdit_2.text()
    if nome_usuario == "admin" and senha == "admin":
        tela_login.close()
        menu_principal.show()
    else:
        tela_login.label_5.setText("Dados de login incorretos!")


def sair():
    menu_principal.close()
    tela_login.show()


def abre_tela_cadastro():
    tela_cadastro_usuario.show()



def cadastrar_usuario():
    nome = tela_cadastro_usuario.lineEdit.text()
    login = tela_cadastro_usuario.lineEdit_2.text()
    senha = tela_cadastro_usuario.lineEdit_3.text()
    confirma_senha = tela_cadastro_usuario.lineEdit_4.text()


# If criado para verificação da senha de cadastro caso de algum 
# problema foi criado um TRY e um EXCEPT para captura destes erros

    if (senha == confirma_senha):
        try:
            banco = sqlite3.connect('banco_cadastro.db')
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS cadastro_usuario(nome text,login text,senha text)")
            cursor.execute("INSERT INTO cadastro_usuario VALUES ('"+nome+"', '"+login+"', '"+senha+"')")

            banco.commit()
            banco.close()
            tela_cadastro_usuario.label_2.setText("Usuário cadastrado com sucesso!")

        except sqlite3.Error as erro:
            print("Erro ao cadastrar usuário: ", erro)
    else:
        tela_cadastro_usuario.label_2.setText("As senhas não são iguais")





app = QtWidgets.QApplication([])
tela_login = uic.loadUi("tela_login.ui")
menu_principal = uic.loadUi("menu_principal.ui")
tela_cadastro_usuario = uic.loadUi("tela_cadastro_usuario.ui")
tela_login.pushButton_2.clicked.connect(chama_menu_principal)
menu_principal.pushButton_3.clicked.connect(sair)
tela_login.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
tela_login.pushButton_3.clicked.connect(abre_tela_cadastro)
tela_cadastro_usuario.pushButton_2.clicked.connect(cadastrar_usuario)


tela_login.show()
app.exec()
