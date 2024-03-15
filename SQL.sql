select * from conta
select * from cliente
select * from HistoricoTransacoes

create database Banco

use banco

CREATE TABLE Cliente (
    id INT PRIMARY KEY IDENTITY(1,1),
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) unique,
    cpf VARCHAR(14) unique
);

CREATE TABLE Conta (
    id INT PRIMARY KEY IDENTITY(1,1),
    cliente_id INT,
    saldo DECIMAL(18, 2) NOT NULL,
    saldoDolar DECIMAL(18, 2) NOT NULL,
    saldoEuro DECIMAL(18, 2) NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES Cliente(id)
);

CREATE TABLE historicoTransacoes (
    id INT PRIMARY KEY IDENTITY(1,1),
    codigoConta INT,
    Cliente VARCHAR(255),
    Valor DECIMAL(18, 2),
    TipoOperacao VARCHAR(30),
    dataTransacao DATETIME DEFAULT GETDATE()
);


drop table HistoricoTransacoes
drop table Conta
drop table Cliente