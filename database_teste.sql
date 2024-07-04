CREATE DATABASE database_teste;
\c database_teste;

CREATE TABLE cadastro_clientes (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL,
    date DATE NOT NULL,
    telefone TEXT NOT NULL
);

INSERT INTO cadastro_clientes (nome, cpf, date, telefone) VALUES ('Maria Fulana da Silva', '999.888.888.88', '1999-01-01', '(84)99999-9999');
INSERT INTO cadastro_clientes (nome, cpf, date, telefone) VALUES ('Jonas Sicrano Oliveira', '999.888.777.77', '1995-03-11', '(84)92424-2424');
INSERT INTO cadastro_clientes (nome, cpf, date, telefone) VALUES ('Renata Fulana da Silva', '999.888.777.66', '1999-10-15', '(84)91111-1111');
