CREATE DATABASE database_teste;
\c database_teste;

CREATE TABLE "cadastro_clientes" (
    "id" SERIAL PRIMARY KEY,
    "nome" TEXT NOT NULL,
    "cpf" TEXT NOT NULL,
    "date" DATE NOT NULL,
    "telefone" TEXT NOT NULL
);

\c database_teste;

INSERT INTO "cadastro_clientes" ("nome", "cpf", "date", "telefone") VALUES ("Maria Fulana da Silva", "999.999.999.99", 1999-01-01, "(84)99999-9999");