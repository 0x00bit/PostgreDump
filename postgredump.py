import psycopg2
from psycopg2 import sql
import docker
import subprocess
import os


class Manager():
    def __init__(self, db_name) -> None:
        self.host_address = "127.0.0.1"
        self.port_db = 5432
        self.db_name = db_name
        self.user = "postgres"
        self.password = "password"

    # Connection with database
    def connect_db(self, database):
        """This function returns the object of the connection with Postgre """
        try:
            self.conn = psycopg2.connect(
                                database=database,
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

        # Command payload
        self.output_file = "backup.sql"
        self.container_name = input("Insira o nome do container: ")
        
        # Payload to dump
        command = [
            "docker-compose", "exec", "-e", f"PGPASSWORD={self.password}",f"{self.container_name}",
            "sh", "-c", f"pg_dump -U '{self.user}' '{self.db_name}'"
            ]  
        
        try:
            # execute the command using subprocess.Popen to catch stdout and stderr
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            stdout, stderr = process.communicate()
            
            # verify return code 
            return_code = process.returncode
            if return_code != 0:
                print(f"Erro ao executar o comando: {stderr}")
            else:
                with open(self.output_file, 'w') as f:
                    f.write(stdout)
                print("Dump realizado com sucesso!")
        except Exception as e:
            print(f"Erro ao realizar o dump do banco de dados: {e}")


    def restore_db(self):

        # file generated by dump function
        self.input_file = input("Insira o nome do arquivo base: ")
        self.container_name = input("Insira o nome do container: ")

        try:
            conn = self.connect_db('postgres') # it must be the default database
            conn.autocommit = True
            curs = conn.cursor()
            curs.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.db_name)))
        except Exception as e:
            print(f"Erro ao tentar recriar database")

        # payload to restore
        command = [
            "docker-compose", "exec", "-e", f"PGPASSWORD={self.password}", self.container_name,
            "sh", "-c", f"psql -U '{self.user}' -d '{self.db_name}' -f '/{self.input_file}'"
        ]

        # payload to transfer backup file to docker
        copy_command = f"docker-compose cp {self.input_file} {self.container_name}:/"

        # transfering file to the docker 
        try:
            os.system(copy_command)
            print("Arquivo de backup transferido para o servidor!")
        except Exception as err:
            print(f"Não foi possível transferir o arquivo de backup para o servidor! {err}")

        # restoring database
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                print(f"Erro ao executar o comando de restore: {result.stderr}")
                return False
            
            print("Restore realizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao realizar o restore do banco de dados: {e}")
            return False

    def check_instances(self):
        try:
            container_names = ['projetoesig-jboss-service-1', 
                               'projetoesig-postgres-1', 
                               'projetoesig-tomcat-service-1']
            
            client = docker.from_env()
            
            for container_name in container_names:
                container = client.containers.get(container_name)
                stats = container.stats(stream=False)
                print(f"Container: {container_name}")
                print(f"Status: {container.status}")
                print(f"ID: {container.id}")
                print("\n")

                if container.status == "running":
                    print(f"O contêiner '{container_name}' está rodando.")
                else:
                    print(f"O contêiner '{container_name}' está parado. Iniciando...")
                    container.start()
                    print(f"O contêiner '{container_name}' foi iniciado com sucesso.")
        
        except docker.errors.NotFound:
            print(f"O contêiner '{container_name}' não foi encontrado.")
        except docker.errors.APIError as e:
            print(f"Erro ao interagir com o Docker: {e}")
    
    
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