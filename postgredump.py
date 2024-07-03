import psycopg2
from psycopg2 import sql
from tabulate import tabulate
import os
import subprocess


class Manager():
    def __init__(self, db_name) -> None:
        self.host_address = "172.17.0.1"
        self.port_db = 5432
        self.db_name = db_name

    # Connection with database
    def connect_db(self):
        """This function returns the object of the connection with Postgre """
        try:
            self.conn = psycopg2.connect(database=self.db_name,
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

        # Connecting to the database and getting cursor 
        self.connection = self.connect_db()
        self.cursor = self.connection.cursor()
        self.querry = self.cursor.execute("SELECT * FROM cadastro_clientes")
        self.dump = self.cursor.fetchall()
        
        #  Printing a formatted table
        print(tabulate(self.dump, headers=["ID", "NOME", "CPF", "Nascimento",
                                           "Telefone"], tablefmt="grid"))
        
        self.table_name = 'cadastro_clientes'
        self.db_name = 'backup_dump'

        # Creating final absolute path
        output_file_db = os.path.join(os.getcwd(), f'{self.db_name}.sql') # Database dump name
        db = os.path.join(os.getcwd(), f'{self.table_name}.csv') # Table dump name
        

        # Dump table 
        try:
            # Dump of table specified at "table_name"
            with open(db, 'w') as f:
                self.cursor.copy_to(f, self.table_name, sep=',')
            print(f"Dados da tabela {self.table_name} exportados com sucesso para {db}")
        except psycopg2.Error as e:
            print("Erro ao exportar dados:", e)

        try:
            # Create a file to write the dump
            with open(output_file_db, 'w') as f:
                # Dump schema
                self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
                tables = self.cursor.fetchall()

                for table in tables:
                    table_name = table[0]
                    f.write(f"-- Table: {table_name}\n")
                    self.cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'")
                    columns = self.cursor.fetchall()
                    f.write(f"CREATE TABLE {table_name} (\n")
                    for column in columns:
                        f.write(f"    {column[0]} {column[1]},\n")
                    f.write(");\n\n")
            
        except psycopg2.Error as e:
            print(f"Error dumping database '{self.db_name}': {e}")


    def restore_db(self):
        """This function make a request to database
        and get all informations from some table"""
        self.connection = self.connect_db()
        self.cursor = self.connection.cursor()

        # Creating final absolute path
        input_db = os.path.join(os.getcwd(), f'{self.db_name}.sql')

        # Restoring Database
        try:
            # Read and execute SQL file
            with open(input_db, 'r') as f:
                sql_commands = f.read()

            self.cursor.execute(sql_commands)
            self.conn.commit()

            print(f"Database '{self.db_name}' restored successfully from '{input_db}'.")

        except psycopg2.Error as e:
            print(f"Error restoring database '{self.db_name}': {e}")

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
            self.restore_db()
            #restore_database()
        elif option == '3':
            pass
            #check_instances()
        elif option == '4':
            pass
        else:
            print("Invalid option")

teste = Manager("database_teste")
teste.menu()