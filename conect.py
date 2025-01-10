import MySQLdb


def conectar():
    return MySQLdb.connect(
        host='localhost',
        user='dev',
        passwd='123456',
        db='certidao_contagem_tempo',
        port=3306
    )
