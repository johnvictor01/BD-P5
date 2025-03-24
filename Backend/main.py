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


#=======================================================================================================
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
#=======================================================================================================



#=======================================================================================================
#USUARIO AUTOR INICIO
#=======================================================================================================
@app.route('/verificar_autor', methods=['POST'])
def verificar_autor():
    dados = request.get_json()
    nome_usuario = dados.get('NomeUsuario')
    senha = dados.get('Senha')

    if not nome_usuario or not senha:
        return jsonify({"erro": "NomeUsuario e Senha são necessários"}), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()

    query_autor = """
    SELECT c.NomeUsuario, c.Senha, p.ID, p.Nome, p.Sobrenome, p.CPF, p.DataNascimento, p.Email, p.Telefone, c.MatriculaAutor
    FROM Autor c
    INNER JOIN Pessoa p ON c.PessoaID = p.ID
    WHERE c.NomeUsuario = %s AND c.Senha = %s
    """

    cursor.execute(query_autor, (nome_usuario, senha))
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
        "MatriculaAutor": resultado[9]  # Adicionando a matrícula do autor na resposta
    }

    session['matricula_autor'] = resultado[9]  # Armazenando Matricula do Autor na Sessão
    print("Matrícula do Autor armazenada na sessão:", session['matricula_autor'])  # Depuração

    return jsonify(pessoa)

#==============================================================================================


@app.route('/autor-logado', methods=['GET'])
def autor_logado():
    
    matricula_autor = session.get('matricula_autor')  # Recupera a matrícula do autor da sessão
    print(matricula_autor)
    if not matricula_autor:
        return jsonify({"erro": "Usuário não autenticado"}), 401
    
    print("Consegui logar")
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Autor WHERE MatriculaAutor = %s", (matricula_autor,))  # Corrigido: tupla
    usuario = cursor.fetchone()
    print("Fechando a conexão")
    cursor.close()
    conexao.close()

    if not usuario:
        return jsonify({"erro": "Autor não encontrado"}), 404

    return jsonify(usuario)

#===================================================================================

@app.route('/obras-autor', methods=['GET'])
def obras_autor():
    matricula_autor = session.get('matricula_autor')  # Recupera a matrícula do autor da sessão

    if not matricula_autor:
        return jsonify({"erro": "Usuário não autenticado"}), 401
    
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    # Consulta SQL ajustada para incluir o campo Valor da tabela Galeria
    query = """
        SELECT oa.*, 
               (SELECT g.Valor FROM Galeria g WHERE g.ObraID = oa.ID LIMIT 1) AS Valor
        FROM ObraDeArte oa
        INNER JOIN Autor a ON oa.AutorID = a.PessoaID
        WHERE a.MatriculaAutor = %s;
    """
    cursor.execute(query, (matricula_autor,))
    obras_de_arte = cursor.fetchall()

    # Converte os dados para o formato esperado pelo frontend
    obras_formatadas = []
    for obra in obras_de_arte:
        obra_formatada = {
            "id": obra['ID'],
            "imagem": f"data:{obra['TipoArquivo']};base64,{base64.b64encode(obra['Imagem']).decode('utf-8')}" if obra['Imagem'] else 'caminho/para/imagem-padrao.jpg',
            "nome": obra['Titulo'],
            "informacoes": obra['Descricao'],
            "valor": float(obra['Valor']) if obra['Valor'] is not None else None  # Adiciona o campo Valor
        }
        obras_formatadas.append(obra_formatada)

    cursor.close()
    conexao.close()

    return jsonify(obras_formatadas)


#=======================================================================================================
@app.route('/inserir-obra', methods=['POST'])
@app.route('/inserir-obra', methods=['POST'])
def inserir_obra():
    dados = request.get_json()
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    # Converte a imagem de base64 para bytes
    imgblob = base64.b64decode(dados.get('imagem'))

    # Busca o ID do autor com base no nome de usuário
    username = dados.get('usuario')
    print(username)
    query = "SELECT PessoaID FROM Autor WHERE NomeUsuario = %s"
    cursor.execute(query, (username,))
    id_autor = cursor.fetchone()

    if not id_autor:
        return jsonify({"erro": "Autor não encontrado"}), 404

    # Dados para salvar no banco de dados
    dados_para_salvar = {
        "Imagem": imgblob,
        "TipoArquivo": dados.get('tipoarquivo'),
        "Titulo": dados.get('titulo'),
        "Descricao": dados.get('descricao'),
        "DataPublicacao": dados.get('dataPublicacao'),
        "EstiloArte": dados.get('estiloArte'),
        "AutorID": id_autor['PessoaID'],
        "PaisGaleria": dados.get('paisGaleria'),
        "Altura": dados.get('altura'),
        "Largura": dados.get('largura')
    }

    # Insere os dados no banco de dados
    query = """
    INSERT INTO ObraDeArte (Imagem, TipoArquivo, Titulo, Descricao, DataPublicacao, EstiloArte, AutorID, PaisGaleria, Altura, Largura)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(query, (
        dados_para_salvar["Imagem"],
        dados_para_salvar["TipoArquivo"],
        dados_para_salvar["Titulo"],
        dados_para_salvar["Descricao"],
        dados_para_salvar["DataPublicacao"],
        dados_para_salvar["EstiloArte"],
        dados_para_salvar["AutorID"],
        dados_para_salvar["PaisGaleria"],
        dados_para_salvar["Altura"],
        dados_para_salvar["Largura"]
    ))

    conexao.commit()



    obraID = PesquisarObraId(dados_para_salvar["Titulo"], dados_para_salvar["Descricao"], dados_para_salvar["DataPublicacao"])
    
    if not obraID:
        return jsonify({"erro": "Falha ao obter ID da obra"}), 500

    query2 = """ INSERT INTO galeria (ObraID, valor, status, IdDono)
    VALUES (%s, 0, 2, 230546);
    """
    cursor.execute(query2, (obraID['id'],))  # Note the comma to make it a tuple

    conexao.commit()

    cursor.close()
    conexao.close()

    return jsonify({"sucesso": "Obra inserida com sucesso"}), 201



def PesquisarObraId(titulo, descricao, datapubli):
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    print("Dados passados:", titulo,descricao,datapubli)
    query = """SELECT id FROM obradearte 
        WHERE Titulo = %s AND Descricao = %s AND DataPublicacao = %s LIMIT 1;
    """
    cursor.execute(query, (titulo, descricao, datapubli))
    obra = cursor.fetchone()  # Changed from fetchall to fetchone
    
    cursor.close()
    conexao.close()
    
    print("Executado com sucesso, id devolvido: ", obra)
    return obra

#==============================================================================
@app.route('/editar-obra', methods=['POST'])
def editar_obra():
    dados = request.get_json()
    
    if not dados or 'id' not in dados or 'Titulo' not in dados or 'Descricao' not in dados:
        return jsonify({"erro": "Dados incompletos"}), 400  # Retorna erro se faltar algum campo

    conexao = conectar_banco()
    cursor = conexao.cursor()

    query = """
    UPDATE ObraDeArte 
    SET Titulo = %s, Descricao = %s
    WHERE ID = %s;
    """
    
    try:
        cursor.execute(query, (dados['Titulo'], dados['Descricao'], dados['id']))
        conexao.commit()  # Confirma a alteração no banco

        cursor.close()
        conexao.close()

        return jsonify({"sucesso": "Obra editada com sucesso"}), 200

    except Exception as e:
        conexao.rollback()  # Desfaz alterações se houver erro
        return jsonify({"erro": f"Erro ao editar obra: {str(e)}"}), 500





    
#=======================================================================================================
#USUARIO AUTOR FIM
#=======================================================================================================




#=======================================================================================================
#USUARIO COLABORADOR INICIO
#=======================================================================================================

@app.route('/remover-obra', methods=['POST'])
def remvover_obra():
    dados = request.get_json()
    id_obra = dados.get('id_obra') #Procura Parametro corretor

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    query = "START TRANSACTION;DELETE FROM galeria WHERE ObraID = %s;DELETE FROM ObradeArte WHERE ID = %s;COMMIT;"
    cursor.execute(query, (id_obra, id_obra))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()

    if not resultado:
        return jsonify({"erro": "Alguma coisa deu errado ao tentar delata a imagem"}), 401
    else:
        return jsonify({"sucesso": "Imagem Deletada com sucesso"}), 201




# Endpoint para listar obras pendentes (status = 2)
@app.route('/obras-pendentes', methods=['GET'])
def listar_obras_pendentes():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    
    query = """
    SELECT o.id, o.Titulo as nome, o.Descricao as informacoes, o.Imagem, 
           a.Nome as autor, o.DataPublicacao, o.EstiloArte as estilo,
           o.PaisGaleria, o.Altura, o.Largura, g.valor
    FROM ObraDeArte o
    JOIN Autor a ON o.AutorID = a.id
    JOIN galeria g ON o.id = g.ObraID
    WHERE g.status = 2
    """
    
    cursor.execute(query)
    obras = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return jsonify(obras)


# Endpoint para liberar obra
@app.route('/liberar-obra', methods=['POST'])
def liberar_obra():
    dados = request.get_json()
    
    if not dados or 'id' not in dados or 'valor' not in dados:
        return jsonify({"erro": "Dados incompletos"}), 400
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    try:
        query = """
        UPDATE galeria 
        SET status = 1, valor = %s 
        WHERE ObraID = %s
        """
        cursor.execute(query, (dados['valor'], dados['id']))
        conexao.commit()
        
        return jsonify({"sucesso": "Obra liberada com sucesso"}), 200
    except Exception as e:
        conexao.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conexao.close()


@app.route('/Liberar-Obra', methods=['POST'])
def obrasParaLiberacao():

    dados = request.get_json()
    id_obra = dados.get('id_obra') 

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    query = "UPDATE galeria SET Status = 1 WHERE ObraID = %s"
    cursor.execute(query, (id_obra))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()








#=======================================================================================================
#USUARIO COLABORADOR FIM
#=======================================================================================================



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