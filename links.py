from flask import Flask, redirect, request
from flask_cors import CORS
from mysql.connector import connect, Error
import random
import string

app = Flask(__name__)

CORS(app)

def get_db_connection():
    try:
        connection = connect(
            host="localhost",
            user="root",
            password="",
            database="shorts_links"
        )
        return connection
    except Error as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

# Criando o short link e salvando no banco de dados
@app.route("/", methods=['POST'])
def encurta():
    data = request.json.get('data')
    carac = string.ascii_letters + string.digits
    encurtado = "".join(random.choice(carac) for _ in range(8)) 

    print(f"Link encurtado: {encurtado} para URL: {data}")

    # Salvando no banco de dados
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO links (original_url, short_url) VALUES (%s, %s)",
                    (data, encurtado)
                )
                connection.commit()  # Confirma a transação
                print("Link salvo com sucesso no banco de dados.")
        except Error as e:
            print("Erro ao salvar no banco de dados:", e)
        finally:
            connection.close()
    else:
        return "Erro ao conectar ao banco de dados.", 500

    return encurtado


# Procurando a url que o short_link aponta
@app.route("/redirect/<short_link>", methods=['GET'])
def procura(short_link):
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT original_url FROM links WHERE short_url = %s", 
                    (short_link,)
                )
                result = cursor.fetchone()
                if result:
                    original_url = result[0]
                    return redirect(original_url)
                else:
                    return "Link não encontrado.", 404
        except Error as e:
            print("Erro ao consultar o banco de dados:", e)
            return "Erro interno do servidor.", 500
        finally:
            connection.close()
    else:
        return "Erro ao conectar ao banco de dados.", 500
    
app.run(debug=True)