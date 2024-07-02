import psycopg2
from psycopg2 import sql
from tabulate import tabulate
import os
import subprocess


class Manager():
    def __init__(self) -> None:
        self.host_address = "172.17.0.1"
        self.port_db = 5432
        # Final path
        self.DUMP_DIR = '.'
        # File name
        self.DUMP_FILE = 'dump_database_teste.sql'
        self.DUMP_PATH = os.path.join(self.DUMP_DIR, self.DUMP_FILE) 

    # Connection with database
    def connect_db(self):
        """This function returns the object of the connection with Postgre """
        try:
            self.conn = psycopg2.connect(database="database_teste",
                                host=self.host_address,
                                user="postgres",
                                password="password",
                                port=self.port_db)
            return self.conn
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    # Dump all data from database
    def dump_database(self):
        """This function make a request to database
        and get all informations from some table"""

        self.connection = self.connect_db()
        self.cursor = self.connection.cursor()
        self.querry = self.cursor.execute("SELECT * FROM cadastro_clientes")
        self.dump = self.cursor.fetchall()
        # Printing a formatted table
        print(tabulate(self.dump, headers=["ID", "NOME", "CPF", "Nascimento",
                                           "Telefone"], tablefmt="grid"))
        self.table_name = 'cadastro_clientes'

        # Creating final absolute path
        output_file = os.path.join(os.getcwd(), 'output_data.csv')
        db = os.path.join(os.getcwd(), 'database.csv')
        
        # Dump table 
        try:
            # Dump of table specified at "table_name"
            with open(db, 'w') as f:
                self.cursor.copy_to(f, self.table_name, sep=',')
            print(f"Dados da tabela {self.table_name} exportados com sucesso para {db}")
        except psycopg2.Error as e:
            print("Erro ao exportar dados:", e)

        # Dump Database
        try:
            # command to dump all database
            cmd = [
                'pg_dump',
                '-U', 'postgres',
                '-d', 'database_teste',
                '-h', f'{self.host_address}',
                '-p', '5432',
                '-f', output_file
            ]

            # Executing pg_dump
            subprocess.run(cmd, check=True)
            print(f"Banco de dados exportado para {output_file} com sucesso.")

        except subprocess.CalledProcessError as e:
            print(f"Erro ao exportar banco de dados: {e}")
        # Close connection
        finally:
            self.cursor.close()
            self.conn.close()

    def menu(self):
        print("""

    _ __  _   _  __ _ _ __ ___  ___ ___ 
    | '_ \| | | |/ _` | '__/ _ \/ __/ __|
    | |_) | |_| | (_| | | |  __/\__ \__ \\
    | .__/ \__, |\__, |_|  \___||___/___/
    |_|    |___/ |___/

    """)

        print("""
        [1]: Dump database
        [2]: Restore database
        [3]: Check instances
        [4]: Exit
    """)
        option = input("\nChoose an option: ")

        if option == '1':
            self.dump_database()
        elif option == '2':
            pass
            #restore_database()
        elif option == '3':
            pass
            #check_instances()
        elif option == '4':
            pass
        else:
            print("Invalid option")

teste = Manager()
teste.menu()