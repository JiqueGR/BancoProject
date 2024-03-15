import pyodbc
from models.cotacao import Cotacao

class Database:
    server = 'JIQUE\SQLEXPRESS'
    database = 'Banco'
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    @staticmethod
    def inserir(cliente, conta):
        sql_insert_cliente = "INSERT INTO Cliente (nome, email, cpf) VALUES (?, ?, ?)"
        Database.cursor.execute(sql_insert_cliente, cliente.nome, cliente.email, cliente.cpf)
        Database.conn.commit()

        while True:
            try:
                sql_insert_conta = "INSERT INTO Conta (cliente_id, saldo, saldoDolar, saldoEuro) VALUES (?, ?, ?, ?)"
                data = Cotacao.getCotacao(base='USD', symbols=['EUR'])
                cotacaoDolar = data['USDBRL']['high']
                cotacaoEuro = data['EURBRL']['high']
                Database.cursor.execute(sql_insert_conta, cliente.id, conta.saldo, float(conta.saldo) / float(cotacaoDolar),
                                        float(conta.saldo) / float(cotacaoEuro))
                Database.conn.commit()
                break
            except:
                cliente.id = int(cliente.id) + 1

    @staticmethod
    def alterarSaldo(operacao, valor, saldo, codigo, transferencia=False):
        sql_update = f"UPDATE conta SET saldo = ?, saldoDolar = ?, saldoEuro = ? WHERE id = ?"
        data = Cotacao.getCotacao(base='USD', symbols=['EUR'])
        cotacaoDolar = data['USDBRL']['high']
        cotacaoEuro = data['EURBRL']['high']
        saldo = float(saldo)
        if operacao == 1:
            saldo -= valor
            if transferencia:
                Database.inserirTransacao(codigo, valor, "Saque", transferencia)
            else:
                Database.inserirTransacao(codigo, valor, "Saque")
        elif operacao == 2:
            saldo += valor
            if transferencia:
                Database.inserirTransacao(codigo, valor, "Depósito", transferencia)
            else:
                Database.inserirTransacao(codigo, valor, "Depósito")

        Database.cursor.execute(sql_update, saldo, float(saldo) / float(cotacaoDolar),
                                float(saldo) / float(cotacaoEuro), codigo)
        Database.conn.commit()

    @staticmethod
    def inicializar():
        Database.cursor.execute('SELECT MAX(id) FROM Cliente')
        return Database.cursor.fetchone()[0]

    @staticmethod
    def getClientes():
        Database.cursor.execute("SELECT id, nome, email, cpf FROM Cliente")
        clientes = Database.cursor.fetchall()
        return clientes

    @staticmethod
    def getContas():
        Database.cursor.execute("SELECT * FROM Conta")
        contas = Database.cursor.fetchall()
        return contas

    @staticmethod
    def buscarConta(id):
        Database.cursor.execute('SELECT id, saldo FROM Conta WHERE id = ?', id)
        conta = Database.cursor.fetchall()
        return conta

    @staticmethod
    def getNomeCliente(id):
        Database.cursor.execute('SELECT nome FROM Cliente WHERE id = ?', id)
        nome = Database.cursor.fetchall()
        nomeCliente = nome[0][0]
        return nomeCliente

    @staticmethod
    def historicoTransacoes(transacoes):
        sql = "SELECT TOP {} CodigoConta, Cliente, Valor, TipoOperacao, " \
              "DataTransacao FROM historicoTransacoes".format(transacoes)
        Database.cursor.execute(sql)
        historico = Database.cursor.fetchall()
        historico_convertido = []
        for row in historico:
            historico_convertido.append((
                row[0],
                row[1],
                float(row[2]),
                row[3],
                row[4]
            ))

        return historico_convertido

    @staticmethod
    def inserirTransacao(codigo, valor, operacao, transferencia=False):
        sql_insert_transacao = "INSERT INTO HistoricoTransacoes (CodigoConta, Cliente, Valor, TipoOperacao)" \
                               "VALUES (?, ?, ?, ?)"
        nome = Database.getNomeCliente(codigo)

        if transferencia:
            Database.cursor.execute(sql_insert_transacao, codigo, nome, valor, (operacao + "Transfencia"))
        else:
            Database.cursor.execute(sql_insert_transacao, codigo, nome, valor, operacao)
        Database.conn.commit()

    @staticmethod
    def atualizarCotacao(contas, clientes):
        data = Cotacao.getCotacao(base='USD', symbols=['EUR'])
        cotacaoDolar = data['USDBRL']['high']
        cotacaoEuro = data['EURBRL']['high']

        for conta, cliente in zip(contas, clientes):
            sql_update = "UPDATE conta SET saldoDolar = ?, saldoEuro = ? WHERE cliente_id = ?"
            Database.cursor.execute(sql_update, float(conta.saldo) / float(cotacaoDolar), float(conta.saldo) / float(cotacaoEuro),
                                    cliente.id)
            Database.conn.commit()
