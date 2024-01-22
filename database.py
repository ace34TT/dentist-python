import psycopg2
from psycopg2 import sql

# Connection parameters
db_params = {
    'dbname': 'dokotera',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

def get_parametrePatients_par_consultation (idConsultaion):
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(**db_params)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Example query to fetch data
    query = sql.SQL("""
        SELECT idparametre , niveau  FROM parametrePatient WHERE idconsultation = %s
    """)

    cursor.execute(query, (idConsultaion,))

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Process and print the fetched data
    result_set = []
    for row in rows:
        result_set.append(row)
    # Close the cursor and connection
    cursor.close()
    conn.close()
    return result_set

def get_medicines ():
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(**db_params)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Example query to fetch data
    query = sql.SQL("""
        SELECT
            m.idmedicament,
            m.nommedicament,
            mp.idparametre,
            mp.efficacite,
            m.prix
        FROM
            medicament AS m
            INNER JOIN medicamentparametre AS mp ON m.idmedicament = mp.idmedicament 
            WHERE mp.idparametre IN (2,7) AND mp.efficacite > 0;
    """)

    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Process and print the fetched data
    result_set = []
    for row in rows:
        result_set.append(row)
    # Close the cursor and connection
    cursor.close()
    conn.close()
    return result_set
