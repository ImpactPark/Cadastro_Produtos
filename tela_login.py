# Import do modulo uic para leitura do arquivo formulario.ui e do modulo QtWidgetspara montar os elementos na tela
from PyQt5 import uic, QtWidgets

# Import do banco sqlite3
import sqlite3

# Função para validar se o usuário e senha estão corretos e chamar o menu primcipal
def chama_menu_principal():
    tela_login.label_5.setText("")
    nome_usuario = tela_login.lineEdit.text()
    senha = tela_login.lineEdit_2.text()
    banco = sqlite3.connect('banco_cadastro.db') #Abertura de coneão com o banco de dados
    cursor = banco.cursor() # Cursor usado para manipulação do banco e criação das querys
    try:
        cursor.execute("SELECT senha FROM cadastro_usuario WHERE login ='{}'".format(nome_usuario)) # Query para pegar a senha na mesma linha que o usuário digitou 
        senha_bd = cursor.fetchall() # Senha recuparada do banco
        if senha == senha_bd[0][0]: #[0][0] primeira posição da lista e primeira posição da tupla para que não traga valores a mais 
            tela_login.close()
            menu_principal.show()
        else:
            tela_login.label_5.setText("Dados de login incorretos!")
        banco.close()
    except:
        tela_login.label_5.setText("Erro ao validar o login")
    

# Função criada para encerrar o menu principal disparada pelo 
# acionamento do botão "Sair" e voltar para a tela de login 
def sair():
    menu_principal.close()
    tela_login.show()

# Função criada para abrir a tela de cadastro quando acionado o botão "cadastrar"
def abre_tela_cadastro():
    tela_login.close()
    tela_cadastro_usuario.show()

def fecha_tela_cadastro():
    tela_cadastro_usuario.close()
    tela_login.show()



# Função responsável por coletar os dados digitados no formuário
def cadastrar_usuario():
    nome = tela_cadastro_usuario.lineEdit.text()
    login = tela_cadastro_usuario.lineEdit_2.text()
    senha = tela_cadastro_usuario.lineEdit_3.text()
    confirma_senha = tela_cadastro_usuario.lineEdit_4.text()

# If criado para verificação da senha de cadastro caso de algum 
# problema foi criado um TRY e um EXCEPT para captura destes erros
    if (senha == confirma_senha):
        try:
            banco = sqlite3.connect('banco_cadastro.db') #Função do sqlite para criação do banco através do connect caso o banco ja exista esta linha não será executada
            cursor = banco.cursor() # Cursor usado para manipulação do banco e criação das querys
            cursor.execute("CREATE TABLE IF NOT EXISTS cadastro_usuario(nome text,login text,senha text)") # Criação da tabela seguido das respectivas colunas para armazenar os dados dos usuários cadastrados 
            cursor.execute("INSERT INTO cadastro_usuario VALUES ('"+nome+"', '"+login+"', '"+senha+"')") # Será inserido no banco o que foi digitado nas variáveis criadas na função cadastrar_usuario
            banco.commit() #Commit para salvar as alteraçõs no banco 
            banco.close() # Fechando a conexão com o banco de dados
            tela_cadastro_usuario.label_2.setText("Usuário cadastrado com sucesso!")

        except sqlite3.Error as erro:
            print("Erro ao cadastrar usuário: ", erro)
    else:
        tela_cadastro_usuario.label_2.setText("As senhas não são iguais")





app = QtWidgets.QApplication([]) # Objeto app que utiliza a classe QtWidgets para criar a aplicação
tela_login = uic.loadUi("tela_login.ui") # Criação do objeto formulario que utiliza o uic para carregar/importar o arquivo "tela_login.ui" 
menu_principal = uic.loadUi("menu_principal.ui") # Criação do objeto formulario que utiliza o uic para carregar/importar o arquivo "menu_principal.ui" 
tela_cadastro_usuario = uic.loadUi("tela_cadastro_usuario.ui")  
tela_login.pushButton_2.clicked.connect(chama_menu_principal) 
menu_principal.pushButton_3.clicked.connect(sair) 
tela_login.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password) # Propriedade setEchoMode utilizada para esconder as senhas digitadas no formulário
tela_login.pushButton_3.clicked.connect(abre_tela_cadastro)
tela_cadastro_usuario.pushButton_2.clicked.connect(cadastrar_usuario)
tela_cadastro_usuario.pushButton_3.clicked.connect(fecha_tela_cadastro) 


tela_login.show()
app.exec()

