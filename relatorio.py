from PyQt5.QtWidgets import QMessageBox
from fpdf import FPDF
from conect import conectar
import locale
from datetime import datetime

# Conexão com o banco
conexao = conectar()

# Configurar o locale para português do Brasil
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


# Função para formatar a data no formato desejado
def formatar_data():
    data_atual = datetime.now()
    data_formatada = data_atual.strftime("%d, %B, %Y")
    return data_formatada.capitalize()


def calcular_dias_trabalhados(data_inicio, data_final):
    return (data_final - data_inicio).days + 1


def buscar_dados(relatorio):
    try:
        print("Iniciando busca de dados...")

        # Preencher o campo txtDataDia com a data formatada
        relatorio.txtDataDia.setText(formatar_data())  # Adicionando a data atual no formato desejado

        cpf = relatorio.txtCpfRelat.text()
        if not cpf:
            QMessageBox.warning(relatorio, 'Erro', 'Por favor, digite um CPF.')
            return

        cursor = conexao.cursor()
        print("Conexão com banco de dados estabelecida.")

        # Buscar dados do servidor
        cursor.execute('SELECT nome, masp, cargo_exercido, adm FROM SERVIDORES WHERE cpf = %s', (cpf,))
        servidor = cursor.fetchone()

        if servidor:
            nome, masp, cargo_exercido, adm = servidor
            relatorio.txtNome.setText(nome)  # Nome
            relatorio.txtMasp.setText(masp)  # MASP
            relatorio.txtCargo.setText(cargo_exercido)  # Cargo
            relatorio.txtAdm.setText(str(adm))  # ADM convertido para string
        else:
            QMessageBox.warning(relatorio, 'Erro', 'CPF não encontrado na tabela SERVIDORES.')
            return

        # Buscar dados do período
        cursor.execute('SELECT MIN(data_inicio), MAX(data_final) FROM PERIODO WHERE cpf = %s', (cpf,))
        datas = cursor.fetchone()

        if datas and datas[0] and datas[1]:
            data_inicio, data_final = datas
            relatorio.txtDataInicio.setText(data_inicio.strftime('%d/%m/%Y'))
            relatorio.txtDataFim.setText(data_final.strftime('%d/%m/%Y'))
        else:
            relatorio.txtDataInicio.setText('')
            relatorio.txtDataFim.setText('')
            QMessageBox.warning(relatorio, 'Aviso', 'Nenhum período cadastrado para este CPF.')
            return

        dias_totais = calcular_dias_trabalhados(data_inicio, data_final)

        # Somar as licenças, férias e faltas
        cursor.execute(''' 
            SELECT SUM(licenca_mater_pater), SUM(licenca_trat_saude), SUM(auxilio_doenca), 
                   SUM(ferias_premio), SUM(faltas), SUM(faltas_abon_anist)
            FROM PERIODO WHERE cpf = %s
        ''', (cpf,))
        licencas = cursor.fetchone()

        if licencas:
            (mater_pater, trat_saude, aux_doenca, ferias, faltas, faltas_abon) = licencas
            mater_pater = mater_pater or 0
            trat_saude = trat_saude or 0
            aux_doenca = aux_doenca or 0
            ferias = ferias or 0
            faltas = faltas or 0
            faltas_abon = faltas_abon or 0

            dias_trabalhados_uteis = dias_totais - (mater_pater + trat_saude + aux_doenca + ferias + faltas + faltas_abon)
            dias_trabalhados_totais = dias_totais - faltas

            # Preencher os campos na interface
            relatorio.txtDiasAno.setText(str(dias_trabalhados_uteis))
            relatorio.txtDiasMaterPater.setText(str(mater_pater))
            relatorio.txtDiasSaude.setText(str(trat_saude))
            relatorio.txtDiasAuxDoenca.setText(str(aux_doenca))
            relatorio.txtDiasFerias.setText(str(ferias))
            relatorio.txtDiasFaltas.setText(str(faltas))
            relatorio.txtDiasAbono.setText(str(faltas_abon))
            relatorio.txtTotal.setText(str(dias_trabalhados_totais))

        else:
            QMessageBox.warning(relatorio, 'Aviso', 'Nenhuma licença ou falta encontrada para este CPF.')

    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        QMessageBox.critical(relatorio, 'Erro', f'Erro ao buscar dados: {e}')


def gerar_pdf(relatorio):
    try:
        # Criar um objeto FPDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Definir fonte
        pdf.set_font("Arial", style="B", size=12)

        # Título do relatório
        pdf.cell(200, 10, txt="CERTIDÃO DE CONTAGEM DE TEMPO E SERVIÇO", ln=True, align='C')

        # TSubtítulo do relatório
        pdf.cell(200, 10, txt="Unidade: Escola Estadual ABCDEF ABCDEF", ln=True, align='C')

        # Definir fonte
        pdf.set_font("Arial", size=12)

        # Adicionar informações do servidor
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Nome: {relatorio.txtNome.text()}", ln=True)
        pdf.cell(200, 10, txt=f"CPF: {relatorio.txtCpfRelat.text()}", ln=True)
        pdf.cell(200, 10, txt=f"MASP: {relatorio.txtMasp.text()}", ln=True)
        pdf.cell(200, 10, txt=f"Cargo: {relatorio.txtCargo.text()}", ln=True)
        pdf.cell(200, 10, txt=f"ADM: {relatorio.txtAdm.text()}", ln=True)

        # Adicionar período de trabalho
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"No Período de: {relatorio.txtDataInicio.text()} a {relatorio.txtDataFim.text()}, sendo, conforme frenquência e livro de ponto:", ln=True)
        pdf.cell(200, 10, txt=f"{relatorio.txtDiasAno.text()} dia(s) de efetivo exercício;", ln=True)
        pdf.cell(200, 10, txt=f"{relatorio.txtDiasMaterPater.text()} dia(s) de licença Maternidade/Paternidade;", ln=True)
        pdf.cell(200, 10, txt=f"{relatorio.txtDiasSaude.text()} dia(s) de licença para tratamento de saúde;", ln=True)
        pdf.cell(200, 10, txt=f"{relatorio.txtDiasAuxDoenca.text()} dia(s) de auxílio-doença, com vínculo empregatício;", ln=True)
        pdf.cell(200, 10, txt=f"{relatorio.txtDiasFerias.text()} dia(s) de férias prêmio;", ln=True)
        pdf.cell(200, 10, txt=f"{relatorio.txtDiasFaltas.text()} dia(s) de faltas;", ln=True)
        pdf.cell(200, 10, txt=f"{relatorio.txtDiasAbono.text()} dia(s) de faltas abonadas, anistiadas.", ln=True)
        pdf.cell(200, 10, txt=f"Totalizando {relatorio.txtTotal.text()} dia(s) de tempo de serviço.", ln=True)

        # Adicionar a data atual
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Belo Horizonte, {relatorio.txtDataDia.text()}", ln=True, align='C')

        # Assinatura do servidor
        pdf.ln(20)
        pdf.cell(200, 10, txt=f"Ass. Responsável e Masp                           Ass. Diretor(a) e Masp", ln=True, align='C')
        pdf.ln(20)
        pdf.cell(200, 10, txt=f"Ass. Inspetor(a) e Masp", ln=True, align='C')

        # Salvar o PDF
        pdf_output = 'certidao_tempo.pdf'
        pdf.output(pdf_output)

        QMessageBox.information(relatorio, "Sucesso", f"Relatório exportado para {pdf_output} com sucesso!")

    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        QMessageBox.critical(relatorio, 'Erro', f'Erro ao gerar PDF: {e}')
