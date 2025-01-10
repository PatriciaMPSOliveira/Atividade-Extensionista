from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
from conect import conectar

# Conexão com o banco
conexao = conectar()


def salvar_periodo(periodo):
    cpf = periodo.txtCpfPeriodo.text()  # CPF relacionado ao servidor
    data_inicio_input = periodo.txtDataInicio.text()  # Data Início no formato DD/MM/YYYY
    data_final_input = periodo.txtDataFim.text()  # Data Final no formato DD/MM/YYYY

    # Validação e conversão das datas
    try:
        data_inicio = datetime.strptime(data_inicio_input, '%d/%m/%Y').strftime('%Y-%m-%d')
        data_final = datetime.strptime(data_final_input, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        QMessageBox.warning(periodo, 'Erro', 'Formato de data inválido! Use DD/MM/YYYY.')
        return

    # Outros campos
    licenca_mater_pater = periodo.txtMaterPater.text()
    licenca_trat_saude = periodo.txtSaude.text()
    auxilio_doenca = periodo.txtAuxDoenca.text()
    ferias_premio = periodo.txtFerias.text()
    faltas = periodo.txtFaltas.text()
    faltas_abon_anist = periodo.txtAbono.text()
    observacoes = periodo.txtObser.text()

    try:
        cursor = conexao.cursor()
        comando_SQL = '''
        INSERT INTO PERIODO (cpf, data_inicio, data_final, licenca_mater_pater, licenca_trat_saude, auxilio_doenca, ferias_premio, faltas, faltas_abon_anist, observacoes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        dados = (cpf, data_inicio, data_final, licenca_mater_pater, licenca_trat_saude, auxilio_doenca, ferias_premio, faltas, faltas_abon_anist, observacoes)
        cursor.execute(comando_SQL, dados)
        conexao.commit()  # Salva no banco de dados
        QMessageBox.information(periodo, 'Sucesso', 'Período cadastrado com sucesso!')
        limpar_campos(periodo)
    except MySQLdb.Error as e:
        print(f"Erro ao salvar no banco de dados: {e}")  # Imprime erro no console
        QMessageBox.critical(periodo, 'Erro', f'Erro ao salvar no banco de dados: {e}')


def limpar_campos(periodo):
    periodo.txtCpfPeriodo.setText('')
    periodo.txtDataInicio.setText('')
    periodo.txtDataFim.setText('')
    periodo.txtMaterPater.setText('')
    periodo.txtSaude.setText('')
    periodo.txtAuxDoenca.setText('')
    periodo.txtFerias.setText('')
    periodo.txtFaltas.setText('')
    periodo.txtAbono.setText('')
    periodo.txtObser.setText('')
