from PyQt5 import uic, QtWidgets
from cadastro import inserir_dados
from periodo import salvar_periodo
from relatorio import buscar_dados, gerar_pdf 


app = QtWidgets.QApplication([])

# Carregar as telas
cadastro = uic.loadUi('cadastro.ui')
periodo = uic.loadUi('Periodo.ui')
relatorio = uic.loadUi('relatorio.ui')

# Configurar ComboBox na tela principal
cadastro.BoxSitFuncional.addItem("Selecione uma opção")
cadastro.BoxSitFuncional.addItems(["Efetivo", "Designado", "Contratado"])

# Conectar os botões às funções
cadastro.btnSalvar.clicked.connect(lambda: inserir_dados(cadastro))
cadastro.btnCadastroPeriodo.clicked.connect(periodo.show)
cadastro.btnRelatorio.clicked.connect(relatorio.show)
periodo.btnSalvarPeriodo.clicked.connect(lambda: salvar_periodo(periodo))
relatorio.txtCpfRelat.returnPressed.connect(lambda: buscar_dados(relatorio))

# Conectar o botão "Exportar" à função de gerar o PDF
relatorio.btnExportar.clicked.connect(lambda: gerar_pdf(relatorio))

# Adicionar comportamento ao botão "Voltar" na tela de período
periodo.btnVoltar.clicked.connect(lambda: (periodo.hide(), cadastro.show()))

# Exibir a tela principal
cadastro.show()
app.exec()