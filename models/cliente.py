class Cliente:
    id = 0
    def __init__(self, nome, email, cpf):
        self.id = Cliente.id
        self.nome = nome
        self.email = email
        self.cpf = cpf
        Cliente.id += 1

    def __str__(self):
        return f'Código: {self.id} \nNome: {self.nome} \nEmail: {self.email} \nCPF: {self.cpf}'

    @staticmethod
    def setId(id):
        if id:
            Cliente.id = id + 1
        else:
            Cliente.id = 1