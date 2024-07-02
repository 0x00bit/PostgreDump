import psycopg2 
from tabulate import tabulate

host_address = "172.17.0.1"
port_db = 5432

# Connection with database
def connect_db():
    """This function returns the object of the connection with Postgre """
    try:
        conn = psycopg2.connect(database="database_teste",
                            host=host_address,
                            user="postgres",
                            password="password",
                            port=port_db)
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

def dump_database(): 
    connection = connect_db()    
    cursor = connection.cursor()
    dump = cursor.execute("SELECT * FROM cadastro_clientes")
    test = cursor.fetchall()
    print(tabulate(test, headers=["ID", "NOME", "CPF", "Nascimento", "Telefone"], tablefmt="grid"))

def menu():
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
        dump_database()
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

menu()