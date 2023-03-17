# Import do modulo uic para leitura do arquivo formulario.ui
# Import do modulo QtWidgetspara montar os elementos na tela
# Import do modulo sys para execitar o exit 
from PyQt5 import uic,QtWidgets
import sys


# Função principal que será disparada pelo acionamento do botão "Gravar"
def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    print("Codigo:", linha1)
    print("Descrição:", linha2)
    print("Preço:", linha3)

# Função criada para encerrar o programa disparada pelo acionamento do botão "Sair"
def encerrar_programa():
    sys.exit()

# Objeto App utilizando a classe QtWidgets para criar a aplicação
app=QtWidgets.QApplication([])

# Criação do objeto formulario que utiliza o uic para carregar/importar o arquivo "formulario.ui" 
formulario=uic.loadUi("formulario.ui")

# Objeto de ação do botão que chama a função principal do sistema
formulario.pushButton.clicked.connect(funcao_principal)

# Objeto de ação do botão que chama a função "encerrar_programa"
formulario.pushButton_3.clicked.connect(encerrar_programa)


formulario.show()
app.exec()