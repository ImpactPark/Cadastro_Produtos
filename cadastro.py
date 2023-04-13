from PyQt5 import uic, QtWidgets
import sqlite3
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape


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


def voltar():
    lista_produtos.close()
    menu_principal.show()


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
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS cadastro_usuario(nome text, login text, senha text)")

        cursor.execute(
            "SELECT * FROM cadastro_usuario WHERE login = ?", (login,))
        existing_user = cursor.fetchone()

        if existing_user:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("O nome de login já está em uso")
            msg.setWindowTitle("Erro no cadastro")
            msg.exec_()
            return

        try:
            cursor.execute(
                "INSERT INTO cadastro_usuario (nome, login, senha) VALUES (?, ?, ?)", (nome, login, senha))
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
    dados_lidos = cursor.fetchall()

    lista_produtos.tableWidget.setRowCount(len(dados_lidos))
    lista_produtos.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            if j == 3:  # Formata a coluna PREÇO com duas casas decimais e inclui o símbolo "R$"
                lista_produtos.tableWidget.setItem(
                    i, j, QtWidgets.QTableWidgetItem("R$ {:.2f}".format(dados_lidos[i][j])))
            else:
                lista_produtos.tableWidget.setItem(
                    i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


def editar_dados():
    linha = lista_produtos.tableWidget.currentRow()
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id=" + str(valor_id))
    produto = cursor.fetchall()
    lista_produtos.close()
    tela_editar.show()
    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))
    
    #banco.commit()

def excluir_dados():
    linha = lista_produtos.tableWidget.currentRow()
    lista_produtos.tableWidget.removeRow(linha)
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id=" + str(valor_id))
    banco.commit()


def gerar_pdf():
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM produtos")
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("Cadastro_Produtos.pdf", pagesize=landscape(
        (612, 792)))  # Define o formato paisagem
    pdf.setPageSize(landscape((612, 792)))
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(250, 550, "Produtos Cadastrados:")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(30, 500, "ID")
    pdf.drawString(100, 500, "CÓDIGO")
    max_product_len = max([len(str(prod[2])) for prod in dados_lidos])
    pdf.drawString(200, 500, "PRODUTO")
    # Aumenta o espaçamento em 20 pixels
    pdf.drawString(200 + max_product_len * 7 + 40, 500, "PREÇO")
    pdf.drawString(300 + max_product_len * 7 + 20, 500, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y = y + 30
        pdf.drawString(30, 500 - y, str(dados_lidos[i][0]))
        pdf.drawString(100, 500 - y, str(dados_lidos[i][1]))
        pdf.drawString(200, 500 - y, str(dados_lidos[i][2]))
        # Formata a coluna PREÇO com duas casas decimais e inclui o símbolo "R$"
        pdf.drawString(200 + max_product_len * 7 + 30, 500 - y,
                       "R$ {:.2f}".format(dados_lidos[i][3]))
        pdf.drawString(300 + max_product_len * 7 + 20,
                       500 - y, str(dados_lidos[i][4]))

    pdf.save()
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText("PDF Gerado com sucesso!")
    msg.setWindowTitle("PDF Gerado")
    msg.exec_()


app = QtWidgets.QApplication([])
tela_login = uic.loadUi("tela_login.ui")
menu_principal = uic.loadUi("menu_principal.ui")
tela_cadastro_usuario = uic.loadUi("tela_cadastro_usuario.ui")
lista_produtos = uic.loadUi("lista_produtos.ui")
tela_editar = uic.loadUi("tela_edicao.ui")
lista_produtos.pushButton_2.clicked.connect(gerar_pdf)
lista_produtos.pushButton_3.clicked.connect(voltar)
lista_produtos.pushButton_4.clicked.connect(excluir_dados)
lista_produtos.pushButton_5.clicked.connect(editar_dados)
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
