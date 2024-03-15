from models.cliente import Cliente
from models.conta import Conta

joao = Cliente('Joao', 'joao@gmail.com', '123.456.789-01', '02/09/1987')
maria = Cliente('Maria', 'maria@gmail.com', '234.567.890-02', '08/07/1978')

print(joao)
print(maria)

conta1 = Conta(joao)
conta2 = Conta(maria)

print(conta1)
print(conta2)

