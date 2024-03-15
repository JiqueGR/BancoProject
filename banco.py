from time import sleep
from models.cliente import Cliente
from models.conta import Conta
from models.BD import Database
import datetime


def menu():
    Cliente.setId(Database.inicializar())
    print('\nSelecione uma opção no menu: ')
    print('1 - Criar conta')
    print('2 - Efetuar saque')
    print('3 - Efetuar depósito')
    print('4 - Efetuar transferência')
    print('5 - Listar contas')
    print('6 - Histórico de transações')
    print('7 - Sair do sistema')

    opcao = int(input())

    if opcao == 1:
        criar_conta()
    elif opcao == 2:
        efetuar_saque()
    elif opcao == 3:
        efetuar_deposito()
    elif opcao == 4:
        efetuar_transferencia()
    elif opcao == 5:
        listar_contas()
    elif opcao == 6:
        historico_transacoes()
        sleep(2)
        menu()
    elif opcao == 7:
        print('Encerrando o sistema')
        sleep(2)
        exit(0)
    else:
        print('Opção inválida')
        sleep(2)
        menu()

def criar_conta():
    print('Informe os dados do cliente: ')
    nome = str(input("Nome do cliente: "))
    email = str(input("E-mail do cliente: "))
    cpf = str(input("CPF do cliente: "))

    cliente = Cliente(nome, email, cpf)
    conta = Conta(cliente)
    Database.inserir(cliente, conta)
    contas.append(conta)

    print('Conta criada com sucesso.')
    print('Dados da conta: ')
    print(conta)
    sleep(2)
    menu()

def efetuar_saque():
    if len(contas) > 0:
        numero = int(input("Informe o número da sua conta: "))
        contaBD = Database.buscarConta(numero)
        if contaBD:
            for conta in contaBD:
                if conta[0] == numero:
                    saque = int(input("Informe o valor do saque: "))
                    if saque < conta[1]:
                        print("Saque realizado " + str(Database.getNomeCliente(contaBD[0][0])))
                        Database.alterarSaldo(1, saque, conta[1], conta[0])
                    else:
                        print("Saque maior do que o saldo")
        else:
            print("Conta não encontrada")
    else:
        print("Ainda não existem contas cadastradas")


    sleep(2)
    menu()

def efetuar_deposito():
    if len(contas) > 0:
        numero = int(input("Informe o número da sua conta: "))
        contaBD = Database.buscarConta(numero)

        if contaBD:
            for conta in contaBD:
                if conta[0] == numero:
                    deposito = int(input("Informe o valor do depósito: "))
                    print("Depósito realizado " + str(Database.getNomeCliente(contaBD[0][0])))
                    Database.alterarSaldo(2, deposito, conta[1], conta[0])
        else:
            print("Conta não encontrada")
    else:
        print("Ainda não existem contas cadastradas")
    sleep(2)
    menu()

def efetuar_transferencia():
    if len(contas) > 0:
        numeroTransferencia = int(input("Informe o número da sua conta: "))
        contaTransferencia = Database.buscarConta(numeroTransferencia)

        if contaTransferencia:
            numeroDestino = int(input("Informe o número da conta destino: "))
            contaDestino = Database.buscarConta(numeroDestino)

            if contaDestino:
                valor = float(input("Informe o valor da transferência: "))
                for contaT in contaTransferencia:
                    Database.alterarSaldo(1, valor, contaT[1], contaT[0], transferencia=True)
                for contaD in contaDestino:
                    Database.alterarSaldo(2, valor, contaD[1], contaD[0], transferencia=True)

                print("Transferência realizada de {} para {}".format(Database.getNomeCliente(numeroTransferencia),
                                                                     Database.getNomeCliente(numeroDestino)))

            else:
                print("A conta destino com número", numeroDestino, "não foi encontrada")
        else:
            print("A sua conta com número", numeroTransferencia, "não foi encontrada")
    else:
        print("Ainda não existem contas cadastradas")


    sleep(2)
    menu()

def listar_contas():
    global contas, clientes
    contas = Database.getContas()
    clientes = Database.getClientes()
    if len(contas) > 0:
        print("Listagem de contas")

        for cliente, conta in zip(clientes, contas):
            print("Código:", cliente[0], "\nCliente:", cliente[1], "\nSaldo: ", conta[2]
                  , "\nSaldo Dolar: ", conta[3], "\nSaldo Euro: ", conta[4])
            print('--------------------')
            sleep(1)
    else:
        print("Não existem contas cadastradas")
    sleep(2)
    menu()

def buscar_conta_por_numero(numero):
    c: Conta = None

    if len(contas) > 0:
        for conta in contas:
            if conta.numero == numero:
                c = conta

    if c:
        return c
    else:
        print("Conta não encontrada")

def historico_transacoes():
    quantidade = int(input("Informe a quantidade de transacoes que deseja buscar:"))
    historico = Database.historicoTransacoes(quantidade)
    if historico:
        for hist in historico:
            data = datetime.datetime(hist[4].year, hist[4].month, hist[4].day)
            data_formatada = data.strftime("%d/%m/%Y")
            lista = list(hist[:-1])
            lista.append(data_formatada)
            print(lista)
    else:
        print("Sem transações")


clientes = Database.getClientes()
contas = Database.getContas()
Database.atualizarCotacao(contas, clientes)
contas = Database.getContas()

menu()

