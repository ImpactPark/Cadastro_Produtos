""" 
**Requisitos para funcionalidade do programa**
Instalar o Python 3.9.5 (https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe)
Instalar a biblioteca PyQt5: pip install PyQt5
Instalar a biblioteca ReportLab é usada para criar documentos em PDF: pip install reportlab 
via CMD navegar até a pasta do executável cadastro.py e executar o comando: python cadastro.py
"""


# Importa uic e QtWidgets do PyQt5, uma biblioteca para criar interfaces gráficas de usuário (GUI) em Python
from PyQt5 import uic, QtWidgets
import sqlite3  # Importa sqlite3, biblioteca para trabalhar com o SQLite
import re  # Importa re, biblioteca para trabalhar com expressões regulares
# Importa canvas do reportlab.pdfgen, biblioteca para criar documentos em PDF
from reportlab.pdfgen import canvas
# Importa landscape de reportlab.lib.pagesizes, para definir o formato de página paisagem em PDF
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors  # Importa o módulo colors da biblioteca ReportLab


numero_id = 0

# Função criada para autenticar o usuário e chamar o menu principal
""" Esta função é responsável por autenticar o usuário ao tentar fazer login no aplicativo. 
Ela verifica se o nome de usuário e a senha inseridos correspondem aos armazenados no banco 
de dados. Se as credenciais estiverem corretas, a tela de login é fechada e a tela do menu 
principal é mostrada. Se as credenciais estiverem incorretas ou houver algum problema ao 
validar o login, uma mensagem de erro é exibida. """


def chama_menu_principal():
    # Limpa qualquer mensagem de erro na tela de login
    tela_login.label_5.setText("")

    # Obtém o nome de usuário digitado na tela de login
    nome_usuario = tela_login.lineEdit.text()

    # Obtém a senha digitada na tela de login
    senha = tela_login.lineEdit_2.text()

    # Conecta-se ao banco de dados SQLite 'banco_cadastro.db'
    banco = sqlite3.connect('banco_cadastro.db')

    # Cria um objeto cursor para executar consultas SQL no banco de dados
    cursor = banco.cursor()

    try:
        # Consulta a senha do usuário com o nome de usuário fornecido no banco de dados
        cursor.execute(
            "SELECT senha FROM cadastro_usuario WHERE login ='{}'".format(nome_usuario))

        # Armazena o resultado da consulta em senha_bd
        senha_bd = cursor.fetchall()

        # Verifica se a senha digitada corresponde à senha armazenada no banco de dados
        if senha == senha_bd[0][0]:
            # Fecha a tela de login
            tela_login.close()

            # Mostra a tela do menu principal
            menu_principal.show()

            # Limpa o campo de nome de usuário na tela de login
            tela_login.lineEdit.setText("")

            # Limpa o campo de senha na tela de login
            tela_login.lineEdit_2.setText("")
        else:
            # Mostra uma mensagem de erro se a senha estiver incorreta
            tela_login.label_5.setText("Dados de login incorretos!")

        # Fecha a conexão com o banco de dados
        banco.close()
    except:
        # Mostra uma mensagem de erro se houver um problema ao validar o login
        tela_login.label_5.setText("Erro ao validar o login")


# Função para fechar a tela do menu principal e recarregar a tela de login
def sair():
    menu_principal.close()
    tela_login.show()

# Função para fechar a lista de produtos e recarregar o menu principal


def voltar():
    lista_produtos.close()
    menu_principal.show()

# Função para fechar a tela de login e carregar a tela de cadastro de usuário


def abre_tela_cadastro():
    tela_login.close()
    tela_cadastro_usuario.show()

# Função para fechar a tela de cadastro de usuário e carregar a tela de login


def fecha_tela_cadastro():
    tela_cadastro_usuario.close()
    tela_login.show()


# Função criada para cadastrar_usuario
""" Este trecho de código define a função cadastrar_usuario(), que é responsável por cadastrar 
um novo usuário no banco de dados do aplicativo. A função verifica se todos os campos obrigatórios 
estão preenchidos corretamente, se a senha e a confirmação da senha coincidem e se o nome de usuário 
já existe no banco de dados. Se todas as verificações forem bem-sucedidas, o novo usuário será inserido 
no banco de dados e uma mensagem de sucesso será exibida. Se alguma das verificações falhar, 
uma mensagem de erro apropriada será exibida. """


def cadastrar_usuario():
    # Obtém o nome digitado no campo lineEdit
    nome = tela_cadastro_usuario.lineEdit.text()
    # Obtém o login digitado no campo lineEdit_2
    login = tela_cadastro_usuario.lineEdit_2.text()
    # Obtém a senha digitada no campo lineEdit_3
    senha = tela_cadastro_usuario.lineEdit_3.text()
    # Obtém a confirmação da senha digitada no campo lineEdit_4
    confirma_senha = tela_cadastro_usuario.lineEdit_4.text()

    # Verifica se os campos nome, login e senha estão preenchidos
    if not nome or not login or not senha:
        # Exibe uma mensagem de erro caso os campos não estejam preenchidos corretamente
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Preencha os campos corretamente")
        msg.setWindowTitle("Erro no cadastro")
        msg.exec_()
        return

    # Verifica se a senha e a confirmação da senha são iguais
    if senha != confirma_senha:
        # Exibe uma mensagem de erro caso as senhas não coincidam
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("As senhas não coincidem")
        msg.setWindowTitle("Erro no cadastro")
        msg.exec_()
        return

    # Conecta-se ao banco de dados banco_cadastro.db
    with sqlite3.connect('banco_cadastro.db') as banco:
        # Cria um cursor para executar comandos SQL
        cursor = banco.cursor()
        # Cria a tabela cadastro_usuario caso ela não exista
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS cadastro_usuario(nome text, login text, senha text)")

        # Verifica se já existe um usuário com o mesmo login
        cursor.execute(
            "SELECT * FROM cadastro_usuario WHERE login = ?", (login,))
        existing_user = cursor.fetchone()

        # Caso o usuário já exista, exibe uma mensagem de erro
        if existing_user:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("O nome de login já está em uso")
            msg.setWindowTitle("Erro no cadastro")
            msg.exec_()
            return

        # Insere o novo usuário na tabela cadastro_usuario
        try:
            cursor.execute(
                "INSERT INTO cadastro_usuario (nome, login, senha) VALUES (?, ?, ?)", (nome, login, senha))
            # Confirma as alterações no banco de dados
            banco.commit()
            # Limpa os campos do formulário após serem enviados
            tela_cadastro_usuario.lineEdit.setText("")
            tela_cadastro_usuario.lineEdit_2.setText("")
            tela_cadastro_usuario.lineEdit_3.setText("")
            tela_cadastro_usuario.lineEdit_4.setText("")
            # Exibe uma mensagem de sucesso em caso de sucesso no cadastro
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Usuário cadastrado com sucesso!")
            msg.setWindowTitle("Cadastro realizado")
            msg.exec_()
        # Caso ocorra um erro ao cadastrar o usuário no banco
        except sqlite3.Error as erro:
            # Imprime o erro no console
            print("Erro ao cadastrar usuário: ", erro)
            # Exibe uma mensagem de erro no label_2
            tela_cadastro_usuario.label_2.setText("Erro ao cadastrar usuário")


# Função principal do programa
""" Este trecho de código é responsável por cadastrar um produto em um banco de dados com base nas 
informações inseridas pelo usuário no menu principal. Ele verifica se os dados inseridos 
estão no formato correto, se o código do produto já existe e qual categoria foi selecionada 
antes de inserir o produto no banco de dados. Se tudo estiver correto, ele limpa os campos. """


def funcao_principal():
    # Obtém o texto das três primeiras linhas editáveis do menu principal
    linha1 = menu_principal.lineEdit.text()
    linha2 = menu_principal.lineEdit_2.text()
    linha3 = menu_principal.lineEdit_3.text()

    # Verifica se os campos inseridos estão no formato correto de acordo com o que foi solicitado
    if not (re.fullmatch(r'\d+', linha1) and re.fullmatch(r'[A-Za-z0-9\s]+', linha2) and re.fullmatch(r'\d{1,3}(\.\d{3})*(,\d{2})?', linha3)):
        # Se não estiverem corretos, exibe uma mensagem de erro
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Dados incorretos para cadastro")
        msg.setWindowTitle("Erro no cadastro")
        msg.exec_()
        return

    # Converte o formato do preço para um número decimal
    linha3 = linha3.replace(".", "").replace(",", ".")
    preco = float(linha3)

    # Verifica se o código do produto já existe no banco de dados
    cursor.execute("SELECT * FROM produtos WHERE codigo = ?", (linha1,))
    resultado = cursor.fetchone()

    # Se o código já existir, o progeama exibe uma mensagem de erro
    if resultado:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Código já existente")
        msg.setWindowTitle("Erro no cadastro")
        msg.exec_()
        return

    # Verifica qual categoria foi selecionada na tela de cadastro
    if menu_principal.radioButton.isChecked():
        categoria = "Informática"
    elif menu_principal.radioButton_2.isChecked():
        categoria = "Alimentos"
    elif menu_principal.radioButton_3.isChecked():
        categoria = "Eletrônicos"
    else:
        # Se nenhuma categoria for selecionada, exibe uma mensagem de erro
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Selecione a categoria")
        msg.setWindowTitle("Erro no cadastro")
        msg.exec_()
        return

    # Insere um produto novo no banco de dados
    try:
        cursor.execute("INSERT INTO produtos (codigo, descricao, preco, categoria) VALUES (?,?,?,?)",
                       (linha1, linha2, preco, categoria))
        banco.commit()
        # Limpa os campos de entrada após os dados serem enviados ao banco
        menu_principal.lineEdit.setText("")
        menu_principal.lineEdit_2.setText("")
        menu_principal.lineEdit_3.setText("")
        # Exibe uma mensagem de sucesso ao cadastrar o produto
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Produto cadastrado com sucesso!")
        msg.setWindowTitle("Cadastro realizado")
        msg.exec_()
    except sqlite3.Error as erro:
        # Se ocorrer um erro durante o cadastro, será aberto um pop-up exibindo uma mensagem de erro
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Erro ao cadastrar o produto")
        msg.setWindowTitle("Erro no cadastro")
        msg.exec_()
        print("Erro ao cadastrar produto: ", erro)


# Função criada para chamar a lista de produtos
""" Este trecho de código define a função chama_lista_produtos, que é responsável por exibir uma lista de 
produtos em uma tabela. A função fecha o menu principal, exibe a lista de produtos, consulta o 
banco de dados para obter todos os registros da tabela de produtos e, em seguida, preenche a tabela 
com os dados retornados. A coluna "PREÇO" é formatada com duas casas decimais e inclui o símbolo "R$". """


def chama_lista_produtos():
    # Fecha o menu principal e carrega a lista de produtos
    menu_principal.close()
    lista_produtos.show()

    # Cria um cursor para interagir com o banco de dados
    cursor = banco.cursor()
    # Seleciona todos os registros da tabela de produtos para ser mostrado na lista
    cursor.execute("SELECT * FROM produtos")
    # Armazena todos os registros retornados pela consulta
    dados_lidos = cursor.fetchall()

    # Define o número de linhas e colunas da tabela de acordo com os dados lidos
    lista_produtos.tableWidget.setRowCount(len(dados_lidos))
    lista_produtos.tableWidget.setColumnCount(5)

    # Preenche a tabela com os dados lidos
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            # Se a coluna atual for a coluna "PREÇO", formata o valor com duas casas decimais e inclui o símbolo "R$"
            if j == 3:
                lista_produtos.tableWidget.setItem(
                    i, j, QtWidgets.QTableWidgetItem("R$ {:.2f}".format(dados_lidos[i][j])))
            else:
                # Para outras colunas, simplesmente insere o valor na célula correspondente
                lista_produtos.tableWidget.setItem(
                    i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


# Função criada para edição dos dados da lista
""" Este trecho de código define a função editar_dados, que é responsável por permitir ao usuário editar 
os dados de um produto selecionado na tabela de produtos. A função obtém a linha selecionada, 
recupera o ID do produto correspondente e consulta o banco de dados para obter os detalhes do 
produto. Em seguida, fecha a tela de lista de produtos, exibe a tela de edição e preenche os 
campos da tela de edição com os dados do produto selecionado. """


def editar_dados():
    # Define a variável global numero_id
    global numero_id

    # Obtém a linha selecionada na tabela de produtos
    linha = lista_produtos.tableWidget.currentRow()

    # Cria um cursor para interagir com o banco de dados
    cursor = banco.cursor()

    # Seleciona todos os IDs dos produtos
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()

    # Obtém o ID do produto na linha selecionada
    valor_id = dados_lidos[linha][0]

    # Seleciona o registro do produto com o ID obtido
    cursor.execute("SELECT * FROM produtos WHERE id=" + str(valor_id))
    produto = cursor.fetchall()

    # Fecha a tela de lista de produtos e carrega a tela de edição
    lista_produtos.close()
    tela_editar.show()

    # Armazena o ID do produto na variável global numero_id
    numero_id = valor_id

    # Preenche os campos da tela de edição com os dados do produto selecionado
    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))


# Função criada para salvar os dados editados
""" Este trecho de código define a função salvar_dados_editados, que é responsável por salvar 
as alterações feitas pelo usuário na tela de edição de produtos. A função obtém os valores 
digitados nos campos da tela de edição, atualiza o registro do produto no banco de dados com 
os novos valores e fecha as janelas de edição e lista de produtos. Em seguida, a função chama 
chama_lista_produtos() para atualizar a lista de produtos e exibi-la novamente, e salva as 
alterações no banco de dados usando banco.commit(). """


def salvar_dados_editados():
    # Acessa a variável global numero_id
    global numero_id

    # Obtém os valores digitados nos campos da tela de edição
    codigo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()

    # Cria um cursor para interagir com o banco de dados
    cursor = banco.cursor()

    # Atualiza o registro do produto no banco de dados com os valores editados
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria = '{}' WHERE id = '{}'".format(
        codigo, descricao, preco, categoria, numero_id))

    # Fecha a tela de edição e a lista de produtos
    tela_editar.close()
    lista_produtos.close()

    # Atualiza a lista de produtos e a exibe novamente
    chama_lista_produtos()

    # Salva as alterações no banco de dados
    banco.commit()


# Função criada para excluir dados do banco
""" Este trecho define a função excluir_dados, que é responsável por excluir um produto selecionado 
na tabela de produtos. A função obtém a linha selecionada, remove-a da tabela e recupera o ID do 
produto correspondente. Em seguida, a função exclui o registro do produto no banco de dados com 
o ID obtido e salva as alterações usando banco.commit(). """


def excluir_dados():
    # Obtém a linha selecionada na tabela de produtos
    linha = lista_produtos.tableWidget.currentRow()

    # Remove a linha selecionada da tabela de produtos
    lista_produtos.tableWidget.removeRow(linha)

    # Cria um cursor para interagir com o banco de dados
    cursor = banco.cursor()

    # Seleciona todos os IDs dos produtos
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()

    # Obtém o ID do produto na linha selecionada
    valor_id = dados_lidos[linha][0]

    # Exclui o registro do produto com o ID obtido do banco de dados
    cursor.execute("DELETE FROM produtos WHERE id=" + str(valor_id))

    # Salva as alterações no banco de dados
    banco.commit()


# Função criada para gerar o PDF
""" Este trecho de código define a função gerar_pdf, que é responsável por criar um arquivo PDF com a lista de 
produtos cadastrados. A função consulta o banco de dados para obter todos os produtos, cria um objeto 
de PDF, define o estilo de fonte e cor para o cabeçalho e os títulos das colunas, e desenha os dados 
dos produtos no PDF. Ao final, a função salva o PDF e exibe uma mensagem de sucesso. """


def gerar_pdf():
    # Cria um cursor para interagir com o banco de dados
    cursor = banco.cursor()

    # Seleciona todos os registros da tabela de produtos
    cursor.execute("SELECT * FROM produtos")
    dados_lidos = cursor.fetchall()

    # Inicializa a variável y para controlar o posicionamento vertical dos elementos no PDF
    y = 0

    # Cria um objeto de PDF com tamanho de página paisagem e nome de arquivo "Cadastro_Produtos.pdf"
    pdf = canvas.Canvas("Cadastro_Produtos.pdf",
                        pagesize=landscape((612, 792)))
    pdf.setPageSize(landscape((612, 792)))

    # Define o estilo de fonte e cor para o cabeçalho
    pdf.setFont("Helvetica-Bold", 25)
    pdf.setFillColor(colors.HexColor("#2c2c54"))

    # Desenha o cabeçalho no PDF
    pdf.drawString(250, 550, "Produtos Cadastrados:")

    # Define o estilo de fonte e cor para os títulos das colunas
    pdf.setFont("Helvetica-Bold", 18)

    # Desenha os títulos das colunas no PDF
    pdf.drawString(30, 500, "ID")
    pdf.drawString(100, 500, "CÓDIGO")
    max_product_len = max([len(str(prod[2])) for prod in dados_lidos])
    pdf.drawString(200, 500, "PRODUTO")
    pdf.drawString(200 + max_product_len * 7 + 40, 500, "PREÇO")
    pdf.drawString(300 + max_product_len * 7 + 20, 500, "CATEGORIA")

    # Define o estilo de fonte e cor para os dados dos produtos
    pdf.setFont("Helvetica", 14)
    pdf.setFillColor(colors.HexColor("#40407a"))

    # Itera sobre os produtos e desenha seus dados no PDF
    for i in range(0, len(dados_lidos)):
        y = y + 30
        pdf.drawString(30, 500 - y, str(dados_lidos[i][0]))
        pdf.drawString(100, 500 - y, str(dados_lidos[i][1]))
        pdf.drawString(200, 500 - y, str(dados_lidos[i][2]))
        pdf.drawString(200 + max_product_len * 7 + 30, 500 - y,
                       "R$ {:.2f}".format(dados_lidos[i][3]))
        pdf.drawString(300 + max_product_len * 7 + 20,
                       500 - y, str(dados_lidos[i][4]))

    # Salva o PDF
    pdf.save()

    # Exibe uma mensagem de sucesso
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText("PDF Gerado com sucesso!")
    msg.setWindowTitle("PDF Gerado")
    msg.exec_()


""" Este código define a inicialização e a configuração do aplicativo Qt. Ele carrega as interfaces 
do usuário, conecta os botões às funções apropriadas e configura a exibição da senha. Além disso, 
o código conecta-se ao banco de dados, cria a tabela de produtos se não existir e conecta o botão de 
cadastro de produto à função correspondente. Por fim, o aplicativo é executado e, quando finalizado, 
a conexão com o banco de dados é encerrada. """
# Inicializa o aplicativo Qt
app = QtWidgets.QApplication([])

# Carrega as interfaces do usuário a partir dos arquivos .ui
tela_login = uic.loadUi("tela_login.ui")
menu_principal = uic.loadUi("menu_principal.ui")
tela_cadastro_usuario = uic.loadUi("tela_cadastro_usuario.ui")
lista_produtos = uic.loadUi("lista_produtos.ui")
tela_editar = uic.loadUi("tela_edicao.ui")

# Conecta os botões das interfaces do usuário às respectivas funções
lista_produtos.pushButton_2.clicked.connect(gerar_pdf)
lista_produtos.pushButton_3.clicked.connect(voltar)
lista_produtos.pushButton_4.clicked.connect(excluir_dados)
lista_produtos.pushButton_5.clicked.connect(editar_dados)
tela_login.pushButton_3.clicked.connect(abre_tela_cadastro)
tela_login.pushButton_2.clicked.connect(chama_menu_principal)

# Configura a exibição da senha como asteriscos para que não fique visivel ao ser digitada
tela_login.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

# Conecta mais botões das interfaces do usuário às respectivas funções
menu_principal.pushButton_2.clicked.connect(chama_lista_produtos)
menu_principal.pushButton_3.clicked.connect(sair)
tela_cadastro_usuario.pushButton_2.clicked.connect(cadastrar_usuario)
tela_cadastro_usuario.pushButton_3.clicked.connect(fecha_tela_cadastro)
tela_editar.pushButton_2.clicked.connect(salvar_dados_editados)

# Conecta ao banco de dados e cria um cursor
banco = sqlite3.connect('banco_cadastro.db')
cursor = banco.cursor()

# Cria a tabela de produtos no banco de dados, caso não exista
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   codigo INTEGER,
   descricao VARCHAR(50),
   preco DOUBLE,
   categoria VARCHAR(20)
);
''')

# Conecta o botão de cadastro de produto na tela principal à função principal
menu_principal.pushButton.clicked.connect(funcao_principal)

# Exibe a tela de login e executa o aplicativo
tela_login.show()
app.exec()

# Fecha a conexão com o banco de dados
banco.close()
