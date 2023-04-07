# Import do modulo uic para leitura do arquivo formulario.ui
# Import do modulo QtWidgetspara montar os elementos na tela
from PyQt5 import uic,QtWidgets
# Import do banco sqlite3
import sqlite3

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

    if menu_principal.radioButton.isChecked(): # If para verificar se o radioButton foi clicado, retorna true ou false
        categoria = "Categoria Informática"
    elif menu_principal.radioButton_2.isChecked(): 
        categoria = "Categoria Alimentos"
    else:
        categoria = "Categoria Eletrônicos"

    # Insere os dados na tabela produtos
    cursor.execute('''
    INSERT INTO produtos (codigo, descricao, preco, categoria)
    VALUES (?, ?, ?, ?)
    ''', (linha1, linha2, linha3, categoria))

    # Salva a transação no banco de dados
    banco.commit()

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