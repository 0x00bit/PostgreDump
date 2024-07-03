import psycopg2
from psycopg2 import sql
from tabulate import tabulate
import os
import docker


class Manager():
    def __init__(self, db_name) -> None:
        self.host_address = "172.17.0.1"
        self.port_db = 5432
        self.db_name = db_name
        self.user = "postgres"
        self.password = "password"

    # Connection with database
    def connect_db(self):
        """This function returns the object of the connection with Postgre """
        try:
            self.conn = psycopg2.connect(database=self.db_name,
                                host=self.host_address,
                                user=self.user,
                                password=self.password,
                                port=self.port_db)
            return self.conn
        except (Exception, psycopg2.Error) as error:
            print("Erro durante a conexão com o PostgreSQL", error)

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
                    f.write(f"-- Table: {table_name}\n") # Writting a comment
                    self.cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'") 
                    columns = self.cursor.fetchall()
                    f.write(f"CREATE TABLE {table_name} (\n")
                    
                    # Write columns except the last one
                    for i, column in enumerate(columns):
                        if i < len(columns) - 1:
                            f.write(f"    {column[0]} {column[1]},\n")
                        else:
                            f.write(f"    {column[0]} {column[1]}\n")
                    
                    f.write(");\n\n")

            
        except psycopg2.Error as e:
            print(f"Error dumping database '{self.db_name}': {e}")


    def creating_database(self):
        """This function is only called by restore_db() function
        to restore database because there's no connect without 
        an valid database"""

        try:
            # Connecting to default database and getting cursor
            self.conn = psycopg2.connect(dbname='postgres', user=self.user, password=self.password, host=self.host_address, port=self.port_db)
            self.conn.autocommit = True  # Set autocommit to True for executing CREATE DATABASE command
            cursor = self.conn.cursor()
            # Create the database
            create_db_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.db_name))
            cursor.execute(create_db_query)

            print(f"Database '{self.db_name}' foi criada com sucesso!.")
            return self.conn

        except psycopg2.Error as e:
            print(f"Erro durante a criação da base de dados: '{self.db_name}': {e}")


    def restore_db(self):
        """This function make a request to database
        and get all informations from some table"""
        self.connection = self.creating_database()
        self.cursor = self.connection.cursor()
        self.input_file = 'backup_dump'  # Input file name  (database dump file)

        # Creating final absolute path
        input_db = os.path.join(os.getcwd(), f'{self.input_file}.sql')

        # Restoring Database
        try:    
            # Read and execute SQL file
            with open(input_db, 'r') as f:
                sql_commands = f.read()

            self.cursor.execute(sql_commands)
            self.connection.commit()

            print(f"Database '{self.db_name}' foi restaurada com sucesso de: '{input_db}'.")

        except psycopg2.Error as e:
            print(f"Erro ao restaurar tabela '{self.db_name}': {e}")

    
    def check_instances(self):
        self.instances = ['postgredump-jboss-service-1','postgredump-jboss-service-1','postgredump-jboss-service-1']
        client = docker.from_env() # getting docker info from env (localhost)
        for container in self.instances:
            try:
                client.containers.get(container)
                print(f"Container {container} esta ativo.")
            except docker.errors.NotFound:
                print(f"Container {container} esta parado.")


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
        elif option == '3':
            pass
            self.check_instances()
        elif option == '4':
            exit()
        else:
            print("Invalid option")

teste = Manager("database_teste")
teste.menu()