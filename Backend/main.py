from flask import Flask, jsonify, request, session
import mysql.connector
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Permite credenciais (cookies)
app.secret_key = 'sua_chave_secreta'

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="2305",
        database="galeriaarte"
    )

#USUÁRIO CLIENTE INICIO
#=======================================================================================================

@app.route('/verificar_usuario', methods=['POST'])
def verificar_usuario():
    dados = request.get_json()
    nome_usuario = dados.get('NomeUsuario')
    senha = dados.get('Senha')

    if not nome_usuario or not senha:
        return jsonify({"erro": "NomeUsuario e Senha são necessários"}), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()

    query_cliente = """
    SELECT c.NomeUsuario, c.Senha, p.ID, p.Nome, p.Sobrenome, p.CPF, p.DataNascimento, p.Email, p.Telefone, c.MatriculaCliente
    FROM Cliente c
    INNER JOIN Pessoa p ON c.PessoaID = p.ID
    WHERE c.NomeUsuario = %s AND c.Senha = %s
    """

    cursor.execute(query_cliente, (nome_usuario, senha))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if not resultado:
        return jsonify({"erro": "Usuário ou senha incorretos"}), 401

    pessoa = {
        "ID": resultado[2],
        "Nome": resultado[3],
        "Sobrenome": resultado[4],
        "CPF": resultado[5],
        "DataNascimento": resultado[6],
        "Email": resultado[7],
        "Telefone": resultado[8],
        "IdDono": resultado[9]  # Usando IdDono em vez de MatriculaCliente
    }

    session['matricula_cliente'] = resultado[9]  # Armazenando IdDono na sessão

    return jsonify(pessoa)



#=======================================================================================================

@app.route('/usuario-logado', methods=['GET'])
def usuario_logado():
    matricula_cliente = session.get('matricula_cliente')

    print("Matrícula do cliente na sessão:", matricula_cliente) 

    if not matricula_cliente:
        return jsonify({"erro": "Usuário não autenticado"}), 401
    
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cliente WHERE MatriculaCliente = %s", (matricula_cliente,))
    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify(usuario)

#=======================================================================================================
#USUÁRIO CLIENTE FIM






#USUARIO AUTOR INICIO
#=======================================================================================================








#=======================================================================================================
#USUARIO AUTOR FIM



@app.route('/obras-disponiveis', methods=['GET'])
def obras_disponiveis():
    matricula_cliente = session.get('matricula_cliente')

    if not matricula_cliente:
        return jsonify({"erro": "Não autorizado"}), 401
    
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    # Consulta SQL para buscar obras disponíveis
    query = """
        SELECT 
            ObraDeArte.ID AS ObraID,
            ObraDeArte.Imagem,
            ObraDeArte.TipoArquivo,
            ObraDeArte.Titulo,
            ObraDeArte.Descricao,
            ObraDeArte.DataPublicacao,
            ObraDeArte.EstiloArte,
            ObraDeArte.AutorID,
            ObraDeArte.PaisGaleria,
            ObraDeArte.Altura,
            ObraDeArte.Largura,
            Galeria.Valor,
            Galeria.IdDono
        FROM Galeria
        INNER JOIN ObraDeArte ON Galeria.ObraID = ObraDeArte.ID
        WHERE Galeria.Status = 1 or Galeria.IdDono != %s
    """
    cursor.execute(query, (matricula_cliente,))
    obras = cursor.fetchall()

    cursor.close()
    conexao.close()

    # Converte a imagem binária para Base64 e o Valor para float
    for obra in obras:
        if obra['Imagem']:
            obra['Imagem'] = base64.b64encode(obra['Imagem']).decode('utf-8')  # Converte para Base64
        if obra['Valor']:
            obra['Valor'] = float(obra['Valor'])  # Converte o Valor para float

    # Retorna um array vazio se não houver obras
    if not obras:
        return jsonify([])  # Retorna um array vazio em vez de um erro 404

    return jsonify(obras)


#=======================================================================================================

@app.route('/obras-biblio', methods=['GET'])
def obras_biblio():
    matricula_cliente = session.get('matricula_cliente')

    # Verifica se o usuário está autenticado
    if not matricula_cliente:
        return jsonify({"erro": "Não autorizado"}), 401
    
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    # Consulta SQL para buscar obras da biblioteca
    query = """
        SELECT obradearte.*
        FROM obradearte
        JOIN galeria ON obradearte.ID = galeria.ObraID
        WHERE galeria.IdDono = %s AND galeria.status = 0;
    """
    cursor.execute(query, (matricula_cliente,))
    obras = cursor.fetchall()

    cursor.close()
    conexao.close()

    # Converte a imagem binária para Base64
    for obra in obras:
        if obra['Imagem']:
            obra['Imagem'] = base64.b64encode(obra['Imagem']).decode('utf-8')  


    if not obras:
        return jsonify([])

    return jsonify(obras)

#=======================================================================================================



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)