from PyQt5.QtWidgets import QMessageBox
from conect import conectar

# Conexão com o banco
conexao = conectar()


def inserir_dados(cadastro):
    nome = cadastro.txtNome.text()
    cpf = cadastro.txtCpf.text()
    masp = cadastro.txtMasp.text()
    cargo_exercido = cadastro.txtCargo.text()
    adm = cadastro.txtAdm.text()
    situacao_funcional = cadastro.BoxSitFuncional.currentText()
    cargo_funcao_conteudo = cadastro.txtCargoFuncao.text()
    funcao_exercida = cadastro.txtFuncao.text()
    codigo_exercicio = cadastro.txtCodigoExc.text()

    try:
        cursor = conexao.cursor()
        comando_SQL = '''
        INSERT INTO SERVIDORES (nome, cpf, masp, cargo_exercido, adm, situacao_funcional, cargo_funcao_conteudo, funcao_exercida, codigo_exercicio)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        dados = (nome, cpf, masp, cargo_exercido, adm, situacao_funcional, cargo_funcao_conteudo, funcao_exercida, codigo_exercicio)
        cursor.execute(comando_SQL, dados)
        conexao.commit()
        QMessageBox.information(cadastro, 'Sucesso', 'Dados inseridos com sucesso!')
        limpar_campos(cadastro)
    except MySQLdb.Error as e:
        QMessageBox.critical(cadastro, 'Erro', f'Erro ao inserir no banco: {e}')


def limpar_campos(cadastro):
    cadastro.txtNome.setText('')
    cadastro.txtCpf.setText('')
    cadastro.txtMasp.setText('')
    cadastro.txtCargo.setText('')
    cadastro.txtAdm.setText('')
    cadastro.BoxSitFuncional.setCurrentIndex(0)
    cadastro.txtCargoFuncao.setText('')
    cadastro.txtFuncao.setText('')
    cadastro.txtCodigoExc.setText('')
