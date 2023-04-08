from PyQt5 import uic, QtWidgets
import sqlite3
import re

def chama_menu_principal():
    tela_login.label_5.setText("")
    nome_usuario = tela_login.lineEdit.text()
    senha = tela_login.lineEdit_2.text()
    banco = sqlite3.connect('banco_cadastro.db')
    cursor = banco.cursor()
    try:
        cursor.execute("SELECT senha FROM cadastro_usuario WHERE login ='{}'".format(
            nome_usuario))
        senha_bd = cursor.fetchall() 
        if senha == senha_bd[0][0]:
            tela_login.close()
            menu_principal.show()
            tela_login.lineEdit.setText("")
            tela_login.lineEdit_2.setText("")
        else:
            tela_login.label_5.setText("Dados de login incorretos!")
        banco.close()
    except:
        tela_login.label_5.setText("Erro ao validar o login")


def sair():
    menu_principal.close()
    tela_login.show()

def abre_tela_cadastro():
    tela_login.close()
    tela_cadastro_usuario.show()

def fecha_tela_cadastro():
    tela_cadastro_usuario.close()
    tela_login.show()

def cadastrar_usuario():
    nome = tela_cadastro_usuario.lineEdit.text()
    login = tela_cadastro_usuario.lineEdit_2.text()
    senha = tela_cadastro_usuario.lineEdit_3.text()
    confirma_senha = tela_cadastro_usuario.lineEdit_4.text()

    if senha != confirma_senha:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("As senhas não coincidem")
        msg.setWindowTitle("Erro no cadastro")
        msg.exec_()
        return

    with sqlite3.connect('banco_cadastro.db') as banco:
        cursor = banco.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS cadastro_usuario(nome text, login text, senha text)")
        
        cursor.execute("SELECT * FROM cadastro_usuario WHERE login = ?", (login,))
        existing_user = cursor.fetchone()

        if existing_user:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("O nome de login já está em uso")
            msg.setWindowTitle("Erro no cadastro")
            msg.exec_()
            return

        try:
            cursor.execute("INSERT INTO cadastro_usuario (nome, login, senha) VALUES (?, ?, ?)", (nome, login, senha))
            banco.commit()
            tela_cadastro_usuario.lineEdit.setText("")
            tela_cadastro_usuario.lineEdit_2.setText("")
            tela_cadastro_usuario.lineEdit_3.setText("")
            tela_cadastro_usuario.lineEdit_4.setText("")
            # Mostra pop-up de sucesso
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Usuário cadastrado com sucesso!")
            msg.setWindowTitle("Cadastro realizado")
            msg.exec_()
        except sqlite3.Error as erro:
            print("Erro ao cadastrar usuário: ", erro)
            tela_cadastro_usuario.label_2.setText("Erro ao cadastrar usuário")




def funcao_principal():
    linha1 = menu_principal.lineEdit.text()
    linha2 = menu_principal.lineEdit_2.text()
    linha3 = menu_principal.lineEdit_3.text()

    if not (re.fullmatch(r'\d+', linha1) and re.fullmatch(r'[A-Za-z0-9\s]+', linha2) and re.fullmatch(r'\d+(\.\d{1,2})?', linha3)):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Dados incorretos para cadastro")
        msg.setWindowTitle("Erro no cadastro")
        msg.exec_()
        return
    
    cursor.execute("SELECT * FROM produtos WHERE codigo = ?", (linha1,))
    resultado = cursor.fetchone()

    if resultado:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Código já existente")
        msg.setWindowTitle("Erro no cadastro")
        msg.exec_()
        return

    if menu_principal.radioButton.isChecked():
        categoria = "Informática"
    elif menu_principal.radioButton_2.isChecked():
        categoria = "Alimentos"
    elif menu_principal.radioButton_3.isChecked():
        categoria = "Eletrônicos"
    else:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Selecione a categoria")
        msg.setWindowTitle("Erro no cadastro")
        msg.exec_()
        return

    try:
        cursor.execute("INSERT INTO produtos (codigo, descricao, preco, categoria) VALUES (?,?,?,?)",
                       (linha1, linha2, linha3, categoria))
        banco.commit()
        menu_principal.lineEdit.setText("")
        menu_principal.lineEdit_2.setText("")
        menu_principal.lineEdit_3.setText("")
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Produto cadastrado com sucesso!")
        msg.setWindowTitle("Cadastro realizado")
        msg.exec_()
    except sqlite3.Error as erro:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Erro ao cadastrar o produto")
        msg.setWindowTitle("Erro no cadastro")
        msg.exec_()
        print("Erro ao cadastrar produto: ", erro)

def chama_lista_produtos():
    menu_principal.close()
    lista_produtos.show()

    cursor = banco.cursor()
    cursor.execute("SELECT * FROM produtos")
    dados_lidos=cursor.fetchall()
    print(dados_lidos)

app = QtWidgets.QApplication([])
tela_login = uic.loadUi("tela_login.ui")
menu_principal = uic.loadUi("menu_principal.ui")
tela_cadastro_usuario = uic.loadUi("tela_cadastro_usuario.ui")
lista_produtos = uic.loadUi("lista_produtos.ui")
tela_login.pushButton_3.clicked.connect(abre_tela_cadastro)
tela_login.pushButton_2.clicked.connect(chama_menu_principal)
tela_login.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
menu_principal.pushButton_2.clicked.connect(chama_lista_produtos)
menu_principal.pushButton_3.clicked.connect(sair)
tela_cadastro_usuario.pushButton_2.clicked.connect(cadastrar_usuario)
tela_cadastro_usuario.pushButton_3.clicked.connect(fecha_tela_cadastro)


banco = sqlite3.connect('banco_cadastro.db')
cursor = banco.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   codigo INTEGER,
   descricao VARCHAR(50),
   preco DOUBLE,
   categoria VARCHAR(20)
);
''')

menu_principal.pushButton.clicked.connect(funcao_principal)

tela_login.show()
app.exec()
banco.close()
