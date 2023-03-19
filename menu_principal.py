# Import do modulo uic para leitura do arquivo formulario.ui
# Import do modulo QtWidgetspara montar os elementos na tela
# Import do modulo sys para execitar o exit 
from PyQt5 import uic,QtWidgets
import sys


# Função principal que será disparada pelo acionamento do botão "Gravar"
def funcao_principal():
    linha1 = menu_principal.lineEdit.text()
    linha2 = menu_principal.lineEdit_2.text()
    linha3 = menu_principal.lineEdit_3.text()
    print("Codigo:", linha1)
    print("Descrição:", linha2)
    print("Preço:", linha3)

# Função criada para encerrar o programa disparada pelo acionamento do botão "Sair"
def sair():
    #tela_login.show()
    menu_principal.close()
    

# Objeto App utilizando a classe QtWidgets para criar a aplicação
app=QtWidgets.QApplication([])

# Criação do objeto formulario que utiliza o uic para carregar/importar o arquivo "menu_principal.ui" 
menu_principal=uic.loadUi("menu_principal.ui")

# Criação do objeto formulario que utiliza o uic para carregar/importar o arquivo "tela_login.ui" 
tela_login=uic.loadUi("tela_login.ui")

# Objeto de ação do botão que chama a função principal do sistema
menu_principal.pushButton.clicked.connect(funcao_principal)



# Objeto de ação do botão que chama a função "encerrar_programa"
menu_principal.pushButton_3.clicked.connect(sair)


menu_principal.show()
app.exec()