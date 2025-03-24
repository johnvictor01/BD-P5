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


#Pergunta qual vai ser o iterador @
@app.route('/obras-mais-caras', methods=['GET'])
def retorna_obras_para_home():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    query = """
        SELECT oa.*
        FROM ObradeArte oa
        INNER JOIN (
            SELECT ObraID 
            FROM galeria 
            ORDER BY valor DESC 
            LIMIT 6
        ) g ON oa.ID = g.ObraID;
    """

    cursor.execute(query)
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if not resultado:
        return jsonify({"ERRO AO TENTAR CARREGAR AS IMAGENS"}), 401

    obras = []
    for obj in range(0, len(resultado)):
        obras[obj] = {
            "ID":resultado[obj][0],
            "Imagem": base64.b64encode(resultado[obj][1]).decode('utf-8'),
            "TipoArquivo": resultado[obj][2],
            "Titulo": resultado[obj][3],
            "Descricao": resultado[obj][4],
            "DataPublicacao": resultado[obj][5],
            "EstiloArte": resultado[obj][6],
            "AutorID": resultado[obj][7],
            "PaisGaleria": resultado[obj][8],
            "Altura": resultado[obj][9],
            "Largura": resultado[obj][10]
        }
    
    return jsonify(obras)



    
#=======================================================================================================
#USUARIO AUTOR FIM
#=======================================================================================================




#=======================================================================================================
#USUARIO COLABORADOR INICIO
#=======================================================================================================

@app.route('/obras', methods=['GET'])
def listar_obras():
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)
        
        query = """
        SELECT o.id, o.Titulo as nome, o.Descricao as informacoes, 
               o.Imagem, o.TipoArquivo, p.Nome as autor
        FROM ObraDeArte o
        JOIN Autor a ON o.AutorID = a.PessoaID
        JOIN Pessoa p ON a.PessoaID = p.ID
        """
        
        cursor.execute(query)
        obras = cursor.fetchall()
        
        for obra in obras:
            if obra['Imagem'] is not None:
                obra['Imagem'] = base64.b64encode(obra['Imagem']).decode('utf-8')
        
        return jsonify(obras)
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conexao' in locals(): conexao.close()

@app.route('/remover-obra', methods=['POST'])
def remover_obra():
    dados = request.get_json()
    id_obra = dados.get('id_obra')

    if not id_obra:
        return jsonify({"erro": "ID da obra é necessário"}), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        # Inicia transação
        cursor.execute("START TRANSACTION")
        
        # 1. Remove da galeria primeiro (devido à restrição de chave estrangeira)
        cursor.execute("DELETE FROM galeria WHERE ObraID = %s", (id_obra,))
        
        # 2. Remove da obra de arte - CORREÇÃO: nome correto da tabela é ObraDeArte (com E maiúsculo)
        cursor.execute("DELETE FROM ObraDeArte WHERE ID = %s", (id_obra,))
        
        # Verifica se alguma linha foi afetada
        if cursor.rowcount == 0:
            conexao.rollback()
            return jsonify({"erro": "Nenhuma obra encontrada com o ID fornecido"}), 404
        
        # Confirma transação
        conexao.commit()
        
        return jsonify({
            "sucesso": "Obra deletada com sucesso",
            "detalhes": {
                "obras_removidas": cursor.rowcount,
                "id_obra": id_obra
            }
        }), 200
        
    except mysql.connector.Error as err:
        conexao.rollback()
        # Tratamento específico para erros de FK
        if err.errno == mysql.connector.errorcode.ER_ROW_IS_REFERENCED_2:
            return jsonify({
                "erro": "Não foi possível excluir a obra pois ela está sendo referenciada em outras tabelas",
                "solucao": "Remova as referências antes de excluir"
            }), 400
        return jsonify({"erro": f"Erro ao deletar obra: {str(err)}"}), 500
    except Exception as e:
        conexao.rollback()
        return jsonify({"erro": f"Erro inesperado: {str(e)}"}), 500
    finally:
        cursor.close()
        conexao.close()



# Endpoint para listar obras pendentes (status = 2)
@app.route('/obras-pendentes', methods=['GET'])
def listar_obras_pendentes():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    
    query = """
        SELECT o.id, o.Titulo AS nome, o.Descricao AS informacoes, 
               o.Imagem, o.TipoArquivo,  -- Adicionado TipoArquivo
               p.Nome AS autor, o.DataPublicacao, o.EstiloArte AS estilo,
               o.PaisGaleria, o.Altura, o.Largura, g.valor
        FROM ObraDeArte o
        JOIN Autor a ON o.AutorID = a.PessoaID
        JOIN Pessoa p ON a.PessoaID = p.ID
        JOIN Galeria g ON o.id = g.ObraID
        WHERE g.status = 2
    """
    
    cursor.execute(query)
    obras = cursor.fetchall()
    
    # Converter a imagem binária para base64
    for obra in obras:
        if obra['Imagem'] is not None:
            obra['Imagem'] = base64.b64encode(obra['Imagem']).decode('utf-8')
        else:
            obra['Imagem'] = None
    
    cursor.close()
    conexao.close()
    
    return jsonify(obras)


# Endpoint unificado para liberação de obras
@app.route('/liberar-obra', methods=['POST'])
def liberar_obra():
    dados = request.get_json()
    print(dados)
    
    # Validações
    if not dados or 'id_obra' not in dados:
        return jsonify({"erro": "ID da obra é obrigatório"}), 400
    
    # Valores padrão
    novo_status = 1  # Status "liberado"
    novo_valor = dados.get('valor', 0)  # Valor padrão 0 se não informado
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    try:
        # Query dinâmica baseada nos parâmetros recebidos
        if 'valor' in dados:
            query = """
            UPDATE galeria 
            SET status = %s, valor = %s 
            WHERE ObraID = %s
            """
            params = (novo_status, novo_valor, dados['id_obra'])
        else:
            query = """
            UPDATE galeria 
            SET status = %s 
            WHERE ObraID = %s
            """
            params = (novo_status, dados['id_obra'])
        
        cursor.execute(query, params)
        conexao.commit()
        
        return jsonify({
            "sucesso": "Obra liberada com sucesso",
            "detalhes": {
                "id_obra": dados['id_obra'],
                "novo_status": novo_status,
                "novo_valor": novo_valor if 'valor' in dados else None
            }
        }), 200
        
    except Exception as e:
        conexao.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conexao.close()




@app.route('/verificar-colaborador', methods=['POST'])
def verificar_colaborador():
    dados = request.get_json()
    nome_usuario = dados.get('NomeUsuario')
    senha = dados.get('Senha')

    if not nome_usuario or not senha:
        return jsonify({"erro": "NomeUsuario e Senha são necessários"}), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()

    query = """
    SELECT c.NomeUsuario, c.Senha, p.ID, p.Nome, p.Sobrenome, p.CPF, p.DataNascimento, p.Email, p.Telefone,
    c.Cargo, c.DataContratacao, c.Salario
    FROM Funcionario c
    INNER JOIN Pessoa p ON c.PessoaID = p.ID
    WHERE c.NomeUsuario = %s AND c.Senha = %s
    """

    cursor.execute(query, (nome_usuario, senha))
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
        "Cargo": resultado[9],
        "DataContratacao": resultado[10],
        "Salario": resultado[10],
    }

    session['nome_colaborador'] = resultado[0]  # Armazenando Nome do Colaborador na sessão

    return jsonify(pessoa)

"""
@app.router('/colaborado-logado', methods=['GET'])
def funcionario_logado():
    
    nome_colaborador = session.get('nome_colaborador')
    print("Nome do Colaborador na sessão:", nome_colaborador) 

    if not nome_colaborador:
        return jsonify({"erro": "Usuário não autenticado"}), 401
    
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Funcionario WHERE NomeUsuario = %s", (nome_colaborador,))
    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify(usuario)

"""




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