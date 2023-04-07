# Import do modulo uic para leitura do arquivo formulario.ui
# Import do modulo QtWidgetspara montar os elementos na tela
from PyQt5 import uic,QtWidgets
# Import do banco sqlite3
import sqlite3
# Import do módulo re para trabalhar com expressões regulares
import re

# Cria a conexão com o banco de dados
banco = sqlite3.connect('banco_cadastro.db')

# Define o cursor para executar os comandos SQL
cursor = banco.cursor()

# Cria a tabela 'produtos' se ela ainda não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   codigo INTEGER,
   descricao VARCHAR(50),
   preco DOUBLE,
   categoria VARCHAR(20)
);
''')

# Função principal que será disparada pelo acionamento do botão "Gravar"
def funcao_principal():
    linha1 = menu_principal.lineEdit.text()
    linha2 = menu_principal.lineEdit_2.text()
    linha3 = menu_principal.lineEdit_3.text()

    # Validação das entradas do usuário
    if not (re.fullmatch(r'\d+', linha1) and re.fullmatch(r'[A-Za-z0-9\s]+', linha2) and re.fullmatch(r'\d+(\.\d{1,2})?', linha3)):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Dados incorretos para cadastro")
        msg.setWindowTitle("Erro no cadastro")
        msg.exec_()
        return

    # Verifica se o código já existe no banco de dados
    cursor.execute("SELECT * FROM produtos WHERE codigo = ?", (linha1,))
    resultado = cursor.fetchone()

    if resultado:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Código já existente")
        msg.setWindowTitle("Erro no cadastro")
        msg.exec_()
        return

    if menu_principal.radioButton.isChecked():  # If para verificar se o radioButton foi clicado, retorna true ou false
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
    
#    # If para verificar se o radioButton foi clicado, retorna true ou false
#    if menu_principal.radioButton.isChecked(): 
#        categoria = "Informática"
#    elif menu_principal.radioButton_2.isChecked(): 
#        categoria = "Alimentos"
#    else:
#        categoria = "Eletrônicos"

    # Insere os dados na tabela produtos
    cursor.execute('''
    INSERT INTO produtos (codigo, descricao, preco, categoria)
    VALUES (?, ?, ?, ?)
    ''', (linha1, linha2, linha3, categoria))

    # Salva a transação no banco de dados
    banco.commit()

    # Exibe mensagem de sucesso em um pop-up
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText("Produto cadastrado com sucesso!")
    msg.setWindowTitle("Cadastro de Produto")
    msg.exec_()

    print("Dados inseridos com sucesso!")
    print("Codigo:", linha1)
    print("Descrição:", linha2)
    print("Preço:", linha3)    

# Função criada para encerrar o menu principal disparada pelo 
# acionamento do botão "Sair" e voltar para a tela de login 
def sair():
    menu_principal.close()
    tela_login.show()

# Objeto app que utiliza a classe QtWidgets para criar a aplicação
app=QtWidgets.QApplication([])

# Criação do objeto formulario que utiliza o uic para carregar/importar o arquivo "menu_principal.ui" 
menu_principal=uic.loadUi("menu_principal.ui")

# Criação do objeto formulario que utiliza o uic para carregar/importar o arquivo "tela_login.ui" 
tela_login=uic.loadUi("tela_login.ui")

# Objeto de ação do botão que chama a função principal do sistema
menu_principal.pushButton.clicked.connect(funcao_principal)

# Objeto de ação do botão que chama a função "sair" retornando para a tela de login
menu_principal.pushButton_3.clicked.connect(sair)

menu_principal.show()
app.exec()

# Fecha a conexão com o banco de dados
banco.close()