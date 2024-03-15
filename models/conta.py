from utils.helper import formata_float_str_moeda

class Conta:
    def __init__(self, cliente):
        self.cliente = cliente
        self.saldo = 0.0

    def __str__(self):
        return f'Número da conta: {self.cliente.id} \nCliente: {self.cliente.nome} ' \
               f'\nSaldo: {formata_float_str_moeda(self.saldo)}'

