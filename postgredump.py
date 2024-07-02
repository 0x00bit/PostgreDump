import psycopg2
from psycopg2 import sql
from tabulate import tabulate
import os


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
        self.dump_sql = f"COPY (SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema') TO '{self.DUMP_PATH}'"
        self.cursor.execute(self.dump_sql)


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