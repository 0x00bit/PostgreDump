![pygress](https://github.com/0x00bit/PostgreDump/assets/136848260/3cdbe5e4-c3f6-4858-a682-da3b8c3de2c0)
# Pygress

## Um simples gerenciador de PostgreSQL via terminal interativo :)

![menu](https://github.com/0x00bit/PostgreDump/assets/136848260/bf04ac5f-ec33-4a55-a9da-88ad2ccce432)

**Requisitos**

    Python 3.x
    Docker

**Instalação**

    Clone este repositório:
   ```git clone https://github.com/0x00bit/PostgreDump.git```
   ```cd pygress```

Instale as dependências:
    ```pip install -r requirements.txt```


**Uso**

Para iniciar Pygress, execute o seguinte comando:

```python3 pygress.py```

[1]: Realiza um dump em um contêiner via linha de comando (stdin) e salva o ```backup.sql``` por meio de um pipe, redirecionando o stdout do docker para a máquina local

[2]: Restaura uma base de dados em um contêiner via linha de comando (stdin). É efetuado o login no banco por meio da biblioteca ```psycopg2```e criado uma base de dados por meio de SQL, logo após, o banco é restaurado usando o binário ```pg_restore```. muito similar a primeira opção.

[3]: Checa o status de cada contêiner (listados em um array). Caso o contêiner esteja parado, ele é restartado.

[4]: Fecha o programa

 **Estrutura do código:**
![Apache Tomcat](https://github.com/0x00bit/PostgreDump/assets/136848260/e379fb9a-77a8-46db-9659-d496b1a842b1)
