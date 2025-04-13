from datetime import datetime
import secrets
from decimal import Decimal
import random
import string
from flask import Flask, jsonify, make_response, request, session
import mysql.connector
from flask_cors import CORS
import base64
import re
#
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch


app = Flask(__name__)
CORS(app, supports_credentials=True)  # Permite credenciais (cookies)
app.secret_key = 'sua_chave_secreta'

#=======================================================================================================
# Conexão Do banco
#=======================================================================================================
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="2305",
        database="galeriaarte"
    )

#=======================================================================================================
# Operações de SELECT 
#=======================================================================================================


# Verificação de Usuário
@app.route('/verificar_usuario', methods=['POST'])
def verificar_usuario():
    dados = request.get_json()
    nome_usuario = dados.get('NomeUsuario')
    senha = dados.get('Senha')

    if not nome_usuario or not senha:
        return jsonify({"erro": "NomeUsuario e Senha são necessários"}), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()

    #Verifica e retorna os dados do usuario
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
        "IdDono": resultado[9]  
    }

    session['matricula_cliente'] = resultado[9]  # Armazenando IdDono na sessão

    return jsonify(pessoa)


@app.route('/dados-usuario-logado', methods=['GET'])
def dados_cliente_logado():
    matricula_cliente = session.get('matricula_cliente')

    #print("1 -- matricula do cliente: ",matricula_cliente)

    if not matricula_cliente:
        return jsonify({"erro": "Usuário não autenticado"}), 401
    
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Consulta completa com dados de Pessoa, Cliente e Endereco
        query = """
        SELECT 
            p.ID, p.Nome, p.Sobrenome, p.CPF, p.DataNascimento,
            p.Email, p.Telefone,
            e.Rua, e.Numero, e.Bairro, e.Cidade, e.Estado, e.CEP, e.Pais,
            c.MatriculaCliente
        FROM Cliente c
        JOIN Pessoa p ON c.PessoaID = p.ID
        LEFT JOIN Endereco e ON e.PessoaID = p.ID
        WHERE c.MatriculaCliente = %s limit 1
        """
        cursor.execute(query, (matricula_cliente,))
        dados = cursor.fetchone()

        if not dados:
            return jsonify({"erro": "Dados não encontrados"}), 404

        # Formatação dos dados
        resposta = {
            "id": dados['ID'],
            "nome_completo": f"{dados['Nome']} {dados['Sobrenome']}",
            "cpf": dados['CPF'],
            "data_nascimento": dados['DataNascimento'],
            "email": dados['Email'],
            "telefone": dados['Telefone'],
            "endereco": {
                "rua": dados.get("Rua"),
                "numero": dados.get("Numero"),
                "bairro": dados.get("Bairro"),
                "cidade": dados.get("Cidade"),
                "estado": dados.get("Estado"),
                "cep": dados.get("CEP"),
                "pais": dados.get("Pais")
            },
            "matricula": dados['MatriculaCliente']
        }
        print(resposta)

        return jsonify(resposta)

    except Exception as e:
        print(f"Erro ao buscar dados: {str(e)}")
        return jsonify({"erro": "Erro interno"}), 500
    finally:
        cursor.close()
        conexao.close()



# Usuário Logado
@app.route('/usuario-logado', methods=['GET'])
def usuario_logado():
    matricula_cliente = session.get('matricula_cliente')

    if not matricula_cliente:
        return jsonify({"erro": "Usuário não autenticado"}), 401
    
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    #verifica Se o usuario na sessão logado existe ou se é lixo
    cursor.execute("SELECT * FROM Cliente WHERE MatriculaCliente = %s", (matricula_cliente,))
    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify(usuario)



@app.route('/recuperar-carrinho', methods=['GET'])
def recuperar_carrinho():
    usuario_id = session.get('matricula_cliente')
    
    if not usuario_id:
        return jsonify({"erro": "Usuário não especificado"}), 400

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    # Busca informações sem a imagem (ou converte a imagem para base64 se necessário)
    cursor.execute("""
    SELECT 
        o.ID,
        o.Titulo,
        o.Descricao,
        o.DataPublicacao,
        o.EstiloArte,
        o.AutorID,  # Mantém apenas o ID se não precisar do nome
        o.PaisGaleria,
        o.Altura,
        o.Largura,
        g.valor
    FROM ObraDeArte o
    JOIN carrinhos c ON o.ID = c.ObraID
    LEFT JOIN galeria g ON o.ID = g.ObraID
    WHERE c.usuario_id = %s
    """, (usuario_id,))
    
    itens = cursor.fetchall()

    cursor.close()
    conexao.close()

    # Converter Decimal para float e tratar outros campos
    for item in itens:
        if 'valor' in item and isinstance(item['valor'], Decimal):
            item['valor'] = float(item['valor'])
        
        # Converter campos de data para string
        if 'DataPublicacao' in item and item['DataPublicacao']:
            item['DataPublicacao'] = item['DataPublicacao'].isoformat()

    return jsonify({
        "sucesso": "Carrinho recuperado com sucesso",
        "itens": itens
    }), 200


#============
# AUTOR
#============


# Verificação de Autor
@app.route('/verificar_autor', methods=['POST'])
def verificar_autor():
    dados = request.get_json()
    nome_usuario = dados.get('NomeUsuario')
    senha = dados.get('Senha')

    if not nome_usuario or not senha:
        return jsonify({"erro": "NomeUsuario e Senha são necessários"}), 400

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Analoga a anterior
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



@app.route('/autor-logado', methods=['GET'])
def autor_logado():
    print("Pegando a matrocula do cliente")
    matricula_autor = session.get('matricula_autor')  # Recupera a matrícula do autor da sessão
    print(matricula_autor)
    if not matricula_autor:
        return jsonify({"erro": "Usuário não autenticado"}), 401
    
    print("Consegui logar")
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    #analoga a anterior
    cursor.execute("SELECT * FROM Autor WHERE MatriculaAutor = %s", (matricula_autor,))  # Corrigido: tupla
    usuario = cursor.fetchone()
    print("Fechando a conexão")
    cursor.close()
    conexao.close()

    if not usuario:
        return jsonify({"erro": "Autor não encontrado"}), 404

    return jsonify(usuario)




@app.route('/dados-autor-logado', methods=['GET'])
def dados_autor_logado():
    matricula_autor = session.get('matricula_autor')

    if not matricula_autor:
        return jsonify({"erro": "Usuário não autenticado"}), 401
    
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        query = """
        SELECT 
            p.ID, p.Nome, p.Sobrenome, p.CPF, 
            DATE_FORMAT(p.DataNascimento, '%%d/%%m/%%Y') as DataNascimento,
            p.Email, p.Telefone,
            e.Rua, e.Numero, e.Bairro, e.Cidade, e.Estado, e.CEP, e.Pais,
            a.MatriculaAutor
        FROM Autor a
        JOIN Pessoa p ON a.PessoaID = p.ID
        LEFT JOIN Endereco e ON e.PessoaID = p.ID
        WHERE a.MatriculaAutor = %s
        """
        cursor.execute(query, (matricula_autor,))
        dados = cursor.fetchone()
        
        if not dados:
            return jsonify({"erro": "Dados não encontrados"}), 404

        # Formatação dos dados
        resposta = {
            "id": dados['ID'],
            "nome_completo": f"{dados['Nome']} {dados['Sobrenome']}",
            "cpf": dados['CPF'],
            "data_nascimento": dados['DataNascimento'],
            "email": dados['Email'],
            "telefone": dados['Telefone'],
            "endereco": {
                "rua": dados['Rua'],
                "numero": dados['Numero'],
                "bairro": dados['Bairro'],
                "cidade": dados['Cidade'],
                "estado": dados['Estado'],
                "cep": dados['CEP'],
                "pais": dados['Pais']
            },
            "matricula": dados['MatriculaAutor']  # Corrigido para MatriculaAutor
        }

        return jsonify(resposta)

    except Exception as e:
        print(f"Erro ao buscar dados: {str(e)}")
        return jsonify({"erro": "Erro interno"}), 500
    finally:
        cursor.close()
        conexao.close()



# Listar Obras do Autor
@app.route('/obras-autor', methods=['GET'])
def obras_autor():
    matricula_autor = session.get('matricula_autor')  # Recupera a matrícula do autor da sessão

    if not matricula_autor:
        return jsonify({"erro": "Usuário não autenticado"}), 401
    
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    #Retorna as obras que pertencem ao autor
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
            "valor": float(obra['Valor']) if obra['Valor'] is not None else None 
        }
        obras_formatadas.append(obra_formatada)

    cursor.close()
    conexao.close()

    return jsonify(obras_formatadas)



# Pesquisar Obra por Titulo
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


# Retorna Obras mais caras
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


# Retorna Obras na Galeria do Cliente
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


# Retorna Obras na Galeria do Autor
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

# Endpoint para listar Vendas pendentes (status = 3)
@app.route('/obras-pendentes-vendas', methods=['GET'])
def listar_obras_pendentes_vendas():
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
        WHERE g.status = 3
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




#===============
#COLABORADOR
#+==============





# Verificar Colaborador
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
    c.Cargo, c.DataContratacao, c.Salario, c.NomeUsuario
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
 
    session['nome_colaborador'] = nome_usuario # Armazenando Nome do Colaborador na sessão
    print(session['nome_colaborador'])
    return jsonify(pessoa)


# Lista Obras para serem aprovadas para liberação
@app.route('/obras-disponiveis', methods=['GET'])
def obras_disponiveis():
    matricula_cliente = session.get('matricula_cliente')

    print(matricula_cliente)

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
        WHERE Galeria.Status = 1 and Galeria.IdDono != %s
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



@app.route('/dados-funcionario-logado', methods=['GET'])
def dados_colaborador_logado():
    print("Pegando a matricula do colaborador")
    matricula_colaborador = session.get('nome_colaborador')  # Recupera a matrícula do colaborador da sessão
    print(matricula_colaborador)

    if not matricula_colaborador:
        return jsonify({"erro": "Usuário não autenticado"}), 401
    
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        query = """
        SELECT 
            p.ID, p.Nome, p.Sobrenome, p.CPF, p.DataNascimento,
            p.Email, p.Telefone,
            e.Rua, e.Numero, e.Bairro, e.Cidade, e.Estado, e.CEP, e.Pais,
            f.ID
        FROM funcionario f
        JOIN Pessoa p ON f.PessoaID = p.ID
        LEFT JOIN Endereco e ON e.PessoaID = p.ID
        WHERE f.NomeUsuario = %s;
        """
        cursor.execute(query, (matricula_colaborador,))
        dados = cursor.fetchone()
        
        if not dados:
            return jsonify({"erro": "Dados não encontrados"}), 404

        # Formatação dos dados
        resposta = {
            "id": dados['ID'],
            "nome_completo": f"{dados['Nome']} {dados['Sobrenome']}",
            "cpf": dados['CPF'],
            "data_nascimento": dados['DataNascimento'],
            "email": dados['Email'],
            "telefone": dados['Telefone'],
            "endereco": {
                "rua": dados['Rua'],
                "numero": dados['Numero'],
                "bairro": dados['Bairro'],
                "cidade": dados['Cidade'],
                "estado": dados['Estado'],
                "cep": dados['CEP'],
                "pais": dados['Pais']
            }, # Corrigido para MatriculaAutor
        }

        return jsonify(resposta)

    except Exception as e:
        print(f"Erro ao buscar dados: {str(e)}")
        return jsonify({"erro": "Erro interno"}), 500
    finally:
        cursor.close()
        conexao.close()





#=======================================================================================================
# Operações de INSERT
#=======================================================================================================
# Inserir Obras do Autor ao banco
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


@app.route('/salvar-carrinho', methods=['POST'])
def salvar_carrinho():
    dados = request.get_json()
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    usuario_id = session.get('matricula_cliente')
    itens = dados.get('itens', [])

    print(itens)

    if not usuario_id:
        return jsonify({"erro": "Usuário não especificado"}), 400


    # Verifica se o usuário existe
    #cursor.execute("SELECT MatriculaCliente FROM Cliente WHERE MatriculaCliente = %s", (usuario_id,))
    #if not cursor.fetchone():
    #    return jsonify({"erro": "Usuário não encontrado"}), 404

    # Limpa o carrinho atual do usuário
    cursor.execute("DELETE FROM carrinhos WHERE usuario_id = %s", (usuario_id,))

    # Insere cada item no carrinho
    for item in itens:
        obra_id = item.get('ObraID')
        if not obra_id:
            continue

        # Verifica se a obra existe
        cursor.execute("SELECT ID FROM ObraDeArte WHERE ID = %s", (obra_id,))
        if not cursor.fetchone():
            continue

        cursor.execute(
            "INSERT INTO carrinhos (usuario_id, ObraID) VALUES (%s, %s)",
            (usuario_id, obra_id)
        )

    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({"sucesso": "Carrinho salvo com sucesso"}), 201


@app.route('/finalizar-compra', methods=['POST'])
def finalizar_compra():
    try:
        # Verifica autenticação
        matricula_cliente = session.get('matricula_cliente')
        print("Matricula", matricula_cliente)
        if not matricula_cliente:
            return jsonify({"erro": "Usuário não autenticado"}), 401
        
        # Obtém dados da requisição
        try:
            data = request.get_json()
            print("Dados recebidos:", data)
            if not data:
                return jsonify({"erro": "Dados inválidos"}), 400
        except Exception as e:
            print("Erro ao parsear JSON:", str(e))
            return jsonify({"erro": "Formato de dados inválido"}), 400
            
        metodo_pagamento = data.get('metodo_pagamento')
        preferencias = data.get('preferencias', {})  # Assume padrão vazio se não enviado
        valor_original = data.get('valor_original', 0)
        valor_final = data.get('valor_final', 0)
        desconto = data.get('desconto', 0)

        print(f"Preferencias recebidas: {preferencias}")
        print(f"Time: {preferencias.get('time', '').lower()}")
        print(f"É fã de One Piece: {preferencias.get('assisteOnePiece', False)}")
        print(f"É de Sousa: {preferencias.get('ehDeSousa', False)}")  # Corrigido para ehDeSousa

        # Métodos válidos (incluindo os especiais)
        metodos_validos = ['cartao', 'pix', 'boleto', 'vasco', 'berrys']
        if not metodo_pagamento or metodo_pagamento.lower() not in metodos_validos:
            return jsonify({
                "erro": "Método de pagamento inválido",
                "metodos_aceitos": metodos_validos
            }), 400

        # Verificação especial para pagamento com Berrys
        if metodo_pagamento.lower() == 'berrys' and not preferencias.get('assisteOnePiece'):
            return jsonify({
                "erro": "Pagamento com Berrys disponível apenas para fãs de One Piece",
                "detalhes": "É necessário marcar 'Sou fã de One Piece'"
            }), 400

        print("Conectando ao banco...")
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)

        try:
            print("Obtendo dados do cliente...")
            # 1. Obtém dados do cliente
            cursor.execute("""
                SELECT PessoaID 
                FROM Cliente 
                WHERE MatriculaCliente = %s
            """, (matricula_cliente,))
            cliente = cursor.fetchone()
            
            print("Resultado cliente:", cliente)
            if not cliente:
                return jsonify({"erro": "Usuário não encontrado"}), 404
                
            pessoa_id = cliente['PessoaID']
            print("Pessoa ID", pessoa_id)

            # 2. Recupera itens do carrinho com estoque disponível
            print("Matricula que vai pra query", matricula_cliente)

            cursor.execute("""
                SELECT o.ID, g.valor 
                FROM ObraDeArte o
                JOIN carrinhos c ON o.ID = c.ObraID
                JOIN galeria g ON o.ID = g.ObraID
                WHERE c.usuario_id = %s AND g.valor IS NOT NULL AND g.status = 1
                FOR UPDATE
            """, (matricula_cliente,))
            itens = cursor.fetchall()
            print(itens)

            if not itens:
                return jsonify({"erro": "Carrinho vazio ou itens indisponíveis"}), 400
            print("Passou do if")

            # 3. Valida valores recebidos com cálculo real
            valor_original_calculado = sum(float(item['valor']) for item in itens)  # Corrigido a sintaxe
            print("Valor original Calculado", valor_original_calculado)
            print(type(valor_original_calculado))
            print(abs(valor_original - valor_original_calculado))
            if abs(valor_original - valor_original_calculado) > 0.01:
                return jsonify({
                    "erro": "Divergência no valor da compra",
                    "detalhes": f"Valor recebido: {valor_original}, Valor calculado: {valor_original_calculado}"
                }), 400
            print("Indo para o steep 4")

            # 4. Aplica regras especiais e valida descontos
            mensagem_desconto = ""
            time_cliente = preferencias.get('time', '').lower()
            
            # Cortesia para torcedores do Vasco
            if time_cliente == 'vasco':
                valor_final = 0
                desconto = valor_original
                mensagem_desconto = "Cortesia para torcedor do Vasco - Grande Time!"
                metodo_pagamento = 'vasco'  # Sobrescreve o método para registro
            
            # Verificação de desconto máximo (35% exceto para Vasco)
            elif desconto > (valor_original * 0.35):
                return jsonify({
                    "erro": "Desconto inválido",
                    "detalhes": f"Desconto máximo permitido é 35% (R$ {valor_original * 0.35:.2f})"
                }), 400

            # 5. Gera ID único para o pedido
            pedido_id = f"PED-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(3).upper()}"

            # 6. Inicia transação
            cursor.execute("START TRANSACTION")

            # 7. Insere venda
            cursor.execute("""
                INSERT INTO Venda (ClienteID, PedidoID, ValorTotal, DataVenda)
                VALUES (%s, %s, %s, NOW())
            """, (pessoa_id, pedido_id, valor_final))
            venda_id = cursor.lastrowid

            # 8. Insere itens do pedido
            for item in itens:
                cursor.execute("""
                    INSERT INTO Pedido (VendaID, ObraID, Valor)
                    VALUES (%s, %s, %s)
                """, (venda_id, item['ID'], item['valor']))

            # 9. Insere pagamento com observação sobre descontos
            situacao = 1 if metodo_pagamento == 'boleto' else 2
            cursor.execute("""
                INSERT INTO Pagamento (
                    VendaID,
                    ValorTotalPago,
                    MetodoPagamento,
                    Situacao
                ) VALUES (%s, %s, %s, %s)
            """, (venda_id, valor_final, metodo_pagamento, situacao))

            # 10. Atualiza status das obras
            for item in itens:
                cursor.execute("""
                    UPDATE galeria
                    SET status = 3, IdDono = %s
                    WHERE ObraID = %s AND status = 1
                """, (matricula_cliente, item['ID']))

            # 11. Limpa carrinho
            cursor.execute("DELETE FROM carrinhos WHERE usuario_id = %s", (matricula_cliente,))

            # Confirma transação
            conexao.commit()

            # Atualiza quantidade de obras compradas (se a stored procedure existir)
            try:
                cursor.callproc('AtualizarQuantidadeObrasCompradas', [matricula_cliente])
                conexao.commit()
            except Exception as proc_error:
                print(f"Ignorando erro na procedure: {str(proc_error)}")

            return jsonify({
                "sucesso": True,
                "mensagem": "Compra processada com sucesso",
                "pedido_id": pedido_id,
                "detalhes": {
                    "metodo_pagamento": metodo_pagamento,
                    "valor_original": valor_original,
                    "desconto": desconto,
                    "valor_final": valor_final,
                    "preferencias": preferencias
                }
            })

        except Exception as e:
            conexao.rollback()
            print("Erro na transação:", str(e))
            return jsonify({
                "erro": "Erro ao processar compra",
                "detalhes": str(e)
            }), 500

        finally:
            cursor.close()
            conexao.close()

    except Exception as e:
        print("Erro geral:", str(e))
        return jsonify({
            "erro": "Erro interno no servidor",
            "detalhes": str(e)
        }), 500


@app.route('/relatorio-cliente-pdf', methods=['GET'])
def gerar_relatorio_pdf():
    matricula_cliente = session.get('matricula_cliente')
    
    if not matricula_cliente:
        return jsonify({"erro": "Usuário não autenticado"}), 401

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        # Buscar dados do cliente
        cursor.execute("""
           SELECT 
            p.Nome, p.Sobrenome, p.Email, p.Telefone,  p.CPF, 
            c.MatriculaCliente, 
            e.Rua,  e.Numero,  e.Bairro,  e.Cidade, e.Estado, e.CEP,  e.Pais
            FROM 
            Cliente c JOIN Endereco e ON c.PessoaID = e.PessoaID
            JOIN Pessoa p ON c.PessoaID = p.ID
            WHERE c.MatriculaCliente = %s limit 1
        """, (matricula_cliente,))
        cliente = cursor.fetchone()

        if not cliente:
            return jsonify({"erro": "Cliente não encontrado"}), 404

        # Buscar histórico de compras
        cursor.execute("""
            SELECT v.ID, v.PedidoID, v.ValorTotal, v.DataVenda,
                   pg.MetodoPagamento, pg.Situacao
            FROM Venda v
            JOIN Cliente c on v.ClienteID = c.PessoaID
            JOIN Pagamento pg ON v.ID = pg.VendaID
            where c.MatriculaCliente = %s
            ORDER BY v.DataVenda DESC;
        """, (matricula_cliente,))
        compras = cursor.fetchall()

        # Buscar obras adquiridas
        cursor.execute("""
            SELECT o.Titulo, p.Valor, v.DataVenda
            FROM Pedido p
            JOIN Venda v ON p.VendaID = v.ID
            JOIN Cliente c on c.PessoaID = v.ClienteID
            JOIN ObraDeArte o ON p.ObraID = o.ID
            WHERE c.MatriculaCliente = %s
            ORDER BY v.DataVenda DESC;
            
        """, (matricula_cliente,))
        obras = cursor.fetchall()

        # Calcular total gasto
        total_gasto = sum(compra['ValorTotal'] for compra in compras)

        # Criar PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilo personalizado
        estilo_titulo = ParagraphStyle(
            'titulo',
            parent=styles['Heading1'],
            fontSize=18,
            alignment=1,  # 0=Left, 1=Center, 2=Right
            spaceAfter=20,
            textColor=colors.HexColor('#2c3e50')
        )
        
        estilo_subtitulo = ParagraphStyle(
            'subtitulo',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#7f8c8d'),
            spaceAfter=10
        )
        
        estilo_texto = ParagraphStyle(
            'texto',
            parent=styles['BodyText'],
            fontSize=10,
            leading=14
        )
        
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("RELATÓRIO DO CLIENTE", estilo_titulo))
        elements.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", estilo_subtitulo))
        elements.append(Spacer(1, 30))
        
        # Seção 1: Dados Pessoais
        elements.append(Paragraph("DADOS PESSOAIS", styles['Heading2']))
        data = [
            ["Nome:", f"{cliente['Nome']} {cliente['Sobrenome']}"],
            ["Matrícula:", cliente['MatriculaCliente']],
            ["CPF:", cliente['CPF']],
            ["Email:", cliente['Email']],
            ["Telefone:", cliente['Telefone']]
        ]
        
        tbl = Table(data, colWidths=[100, 300])
        tbl.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#7f8c8d')),
            ('TEXTCOLOR', (1,0), (1,-1), colors.black),
        ]))
        
        elements.append(tbl)
        elements.append(Spacer(1, 30))
        
        # Seção 2: Histórico de Compras
        elements.append(Paragraph("HISTÓRICO DE COMPRAS", styles['Heading2']))
        
        data_compras = [["Pedido", "Data", "Valor (R$)", "Pagamento", "Status"]]
        for compra in compras:
            data_compras.append([
                compra['PedidoID'],
                compra['DataVenda'].strftime('%d/%m/%Y'),
                f"{compra['ValorTotal']:.2f}",
                compra['MetodoPagamento'].capitalize(),
                'Aprovado' if compra['Situacao'] == 2 else 'Pendente'
            ])
        
        tbl_compras = Table(data_compras, colWidths=[120, 80, 80, 100, 60])
        tbl_compras.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.white),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#e0e0e0')),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 9),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        
        elements.append(tbl_compras)
        elements.append(Spacer(1, 30))
        
        # Seção 3: Obras Adquiridas
        elements.append(Paragraph("OBRAS ADQUIRIDAS", styles['Heading2']))
        
        data_obras = [["Obra", "Valor (R$)", "Data da Compra"]]
        for obra in obras:
            data_obras.append([
                obra['Titulo'],
                f"{obra['Valor']:.2f}",
                obra['DataVenda'].strftime('%d/%m/%Y')
            ])
        
        tbl_obras = Table(data_obras, colWidths=[300, 80, 80])
        tbl_obras.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2ecc71')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.white),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#e0e0e0')),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 9),
        ]))
        
        elements.append(tbl_obras)
        elements.append(Spacer(1, 30))
        
        # Rodapé com total
        elements.append(Paragraph(f"TOTAL GASTO: R$ {total_gasto:.2f}", 
                                ParagraphStyle(
                                    'total',
                                    parent=styles['Heading2'],
                                    fontSize=12,
                                    alignment=2,
                                    textColor=colors.HexColor('#e74c3c')
                                )))
        
        # Gerar PDF
        doc.build(elements)
        
        buffer.seek(0)

        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=relatorio.pdf'
        return response

    except Exception as e:
        print(f"ERRO DETALHADO: {str(e)}")  # Log completo no terminal
        import traceback
        traceback.print_exc()  # Imprime stack trace completo
        return jsonify({"erro": f"Falha ao gerar PDF: {str(e)}"}), 500

    finally:
        cursor.close()
        conexao.close()


@app.route('/cadastro-cliente', methods=['POST'])
def cadastro_cliente():
    # Obter dados JSON da requisição
    data = request.get_json()
    print(data)
    
    # Extrair dados básicos
    pessoa = data.get('pessoa', {})
    cliente = data.get('cliente', {})
    endereco = data.get('endereco', {})
    
    try:
        # Conectar ao banco de dados
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)
        
        # Inserir na tabela Pessoa
        cursor.execute(
            "INSERT INTO Pessoa (Nome, Sobrenome, CPF, DataNascimento, Email, Telefone) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (
                pessoa.get('Nome'),
                pessoa.get('Sobrenome'),
                pessoa.get('CPF', '').replace('.', '').replace('-', ''),
                pessoa.get('DataNascimento'),
                pessoa.get('Email'),
                pessoa.get('Telefone', '').replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
            )
        )
        pessoa_id = cursor.lastrowid
        
        # Gerar matrícula simples
        matricula = f"CL{pessoa_id:04d}"
        
        # Inserir na tabela Cliente (com hash da senha)
        cursor.execute(
            "INSERT INTO Cliente (PessoaID, MatriculaCliente, NomeUsuario, Senha) "
            "VALUES (%s, %s, %s, %s)",
            (
                pessoa_id,
                matricula,
                cliente.get('NomeUsuario'),
                cliente.get('Senha', '')
            )
        )

        # Inserir na tabela Endereco
        cursor.execute(
            "INSERT INTO Endereco (PessoaID, Rua, Numero, Bairro, Cidade, Estado, CEP, Pais) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                pessoa_id,
                endereco.get('Rua'),
                endereco.get('Numero'),
                endereco.get('Bairro'),
                endereco.get('Cidade'),
                endereco.get('Estado'),
                endereco.get('CEP'),
                endereco.get('Pais'),
            )
        )
        
        # Confirmar as alterações
        conexao.commit()
        
        return jsonify({
            "success": True,
            "message": "Cliente cadastrado com sucesso",
            "cliente_id": pessoa_id,
            "matricula": matricula
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erro no servidor",
            "error": str(e)
        }), 500
        
    finally:
        cursor.close()
        conexao.close()



@app.route('/cadastro-autor', methods=['POST'])
def cadastro_autor():
    print("\n=== INÍCIO DA REQUISIÇÃO ===")
    try:
        data = request.get_json()
        print("Dados recebidos:", data)
        
        # Validação básica dos dados recebidos
        required_fields = {
            'pessoa': ['Nome', 'Sobrenome', 'CPF', 'DataNascimento', 'Email'],
            'autor': ['NomeUsuario', 'Senha']
        }
        
        for category, fields in required_fields.items():
            if category not in data:
                print(f"Campo {category} faltando nos dados")
                return jsonify({"success": False, "message": f"Dados de {category} não fornecidos"}), 400
            for field in fields:
                if field not in data[category] or not data[category][field]:
                    print(f"Campo obrigatório faltando: {category}.{field}")
                    return jsonify({"success": False, "message": f"Campo obrigatório: {field}"}), 400
    
        pessoa = data['pessoa']
        autor = data['autor']
        endereco = data.get('endereco', {})
        print("Dados validados com sucesso")

        # Conexão com o banco
        print("Conectando ao banco de dados...")
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)
        print("Conexão estabelecida")

        # 1. Inserir na tabela Pessoa
        cpf_limpo = pessoa['CPF'].replace('.', '').replace('-', '')
        telefone_limpo = re.sub(r'[^0-9]', '', pessoa.get('Telefone', ''))
        print(f"Inserindo pessoa: {pessoa['Nome']} {pessoa['Sobrenome']}, CPF: {cpf_limpo}")
        
        cursor.execute(
            "INSERT INTO Pessoa (Nome, Sobrenome, CPF, DataNascimento, Email, Telefone) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (
                pessoa['Nome'],
                pessoa['Sobrenome'],
                cpf_limpo,
                pessoa['DataNascimento'],
                pessoa['Email'],
                telefone_limpo
            )
        )
        pessoa_id = cursor.lastrowid
        print(f"Pessoa inserida com ID: {pessoa_id}")

        # 2. Gerar matrícula de autor
        cursor.execute("SELECT COUNT(*) as total FROM Autor")
        total_autores = cursor.fetchone()['total']
        matricula = f"AU{total_autores + 1:04d}"
        print(f"Matrícula gerada: {matricula}")

        # 3. Inserir na tabela Autor (senha em texto puro)
        print(f"Inserindo autor: {autor['NomeUsuario']}")
        cursor.execute(
            "INSERT INTO Autor (PessoaID, MatriculaAutor, NomeUsuario, Senha) "  # Mantenha a coluna como Senha
            "VALUES (%s, %s, %s, %s)",
            (
                pessoa_id,
                matricula,
                autor['NomeUsuario'],
                autor['Senha']  # Senha em texto puro
            )
        )
        print("Autor inserido com sucesso")

        # 4. Inserir endereço se fornecido
        if endereco:
            cep_limpo = endereco.get('CEP', '').replace('-', '')
            print(f"Inserindo endereço - CEP: {cep_limpo}")
            cursor.execute(
                "INSERT INTO Endereco (PessoaID, Rua, Numero, Bairro, Cidade, Estado, CEP, Pais) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    pessoa_id,
                    endereco.get('Rua'),
                    endereco.get('Numero'),
                    endereco.get('Bairro'),
                    endereco.get('Cidade'),
                    endereco.get('Estado'),
                    cep_limpo,
                    endereco.get('Pais', 'BRA')
                )
            )
            print("Endereço inserido com sucesso")
        
        conexao.commit()
        print("Transação commitada")

        return jsonify({
            "success": True,
            "message": "Autor cadastrado com sucesso",
            "autor_id": pessoa_id,
            "matricula": matricula
        }), 201
        
    except mysql.connector.IntegrityError as e:
        print("ERRO DE INTEGRIDADE:", str(e))
        if 'conexao' in locals():
            conexao.rollback()
            print("Rollback executado")
        error_message = "Erro de integridade no banco de dados"
        if "Duplicate entry" in str(e):
            if "CPF" in str(e):
                error_message = "CPF já cadastrado"
            elif "Email" in str(e):
                error_message = "Email já cadastrado"
            elif "NomeUsuario" in str(e):
                error_message = "Nome de usuário já existe"
        print("Mensagem de erro:", error_message)
        return jsonify({
            "success": False,
            "message": error_message
        }), 400
        
    except Exception as e:
        print("ERRO INESPERADO:", str(e))
        print("Tipo do erro:", type(e).__name__)
        if 'conexao' in locals():
            conexao.rollback()
            print("Rollback executado")
        return jsonify({
            "success": False,
            "message": "Erro no servidor",
            "error": str(e),
            "error_type": type(e).__name__
        }), 500
        
    finally:
        if 'cursor' in locals(): 
            cursor.close()
            print("Cursor fechado")
        if 'conexao' in locals(): 
            conexao.close()
            print("Conexão fechada")
        print("=== FIM DA REQUISIÇÃO ===\n")

        

@app.route('/cadastro-colaborador', methods=['POST'])
def cadastro_colaborador():
    # Obter dados JSON da requisição
    data = request.get_json()
    print(data)
    
    # Extrair dados básicos
    pessoa = data.get('pessoa', {})
    funcionario = data.get('funcionario', {})
    endereco = data.get('endereco', {})
    
    try:
        # Conectar ao banco de dados
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)
        
        # Inserir na tabela Pessoa
        cursor.execute(
            "INSERT INTO Pessoa (Nome, Sobrenome, CPF, DataNascimento, Email, Telefone) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (
                pessoa.get('Nome'),
                pessoa.get('Sobrenome'),
                pessoa.get('CPF', '').replace('.', '').replace('-', ''),
                pessoa.get('DataNascimento'),
                pessoa.get('Email'),
                pessoa.get('Telefone', '').replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
            )
        )
        pessoa_id = cursor.lastrowid
        
        # Gerar matrícula simples
        # matricula = f"CL{pessoa_id:04d}"
        
        # Inserir na tabela Cliente (com hash da senha)
        cursor.execute(
            "INSERT INTO Funcionario (PessoaID, NomeUsuario, Senha, Cargo, DataContratacao, Salario) "
            "VALUES (%s, %s, %s, %s)",
            (
                pessoa_id,
                funcionario.get('NomeUsuario'),
                funcionario.get('Senha', ''),
                funcionario.get('Cargo'),
                funcionario.get('DataContratacao'),
                funcionario.get('Salario', 0)
            )
        )

        # Inserir na tabela Endereco
        cursor.execute(
            "INSERT INTO Endereco (PessoaID, Rua, Numero, Bairro, Cidade, Estado, CEP, Pais) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                pessoa_id,
                endereco.get('Rua'),
                endereco.get('Numero'),
                endereco.get('Bairro'),
                endereco.get('Cidade'),
                endereco.get('Estado'),
                endereco.get('CEP'),
                endereco.get('Pais'),
            )
        )
        
        # Confirmar as alterações
        conexao.commit()
        
        return jsonify({
            "success": True,
            "message": "Cliente cadastrado com sucesso",
            "cliente_id": pessoa_id,
            "matricula": matricula
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erro no servidor",
            "error": str(e)
        }), 500
        
    finally:
        cursor.close()
        conexao.close()


#=======================================================================================================
# Operações de UPDATE 
#=======================================================================================================
# Atualizar Obra do Autor
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


@app.route('/autorizar-venda', methods=['POST'])
def autorizar_venda():
    dados = request.get_json()
    
    # Validações básicas
    if not dados or 'id_obra' not in dados:
        return jsonify({"erro": "ID da obra é obrigatório"}), 400
   
  
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        # 1. Verifica se a obra existe e está pendente
        cursor.execute("""
            SELECT status FROM galeria 
            WHERE ObraID = %s
        """, (dados['id_obra'],))
        obra = cursor.fetchone()
        
        print("Obra encontrada")
        if not obra:
            return jsonify({"erro": "Obra não encontrada na galeria"}), 404
        
        # 2. Atualiza o status para 0 
        print(dados['id_obra'])
        cursor.execute("""
            UPDATE galeria 
            SET status = '0'
            WHERE ObraID = %s
        """, (dados['id_obra'],))
        
        print("Depois de executar na galeria")
        conexao.commit()
        print("Obra autorizada com sucesso")
        return jsonify({
            "sucesso": "Venda autorizada com sucesso",
            "detalhes": {
                "id_obra": dados['id_obra'],
                "novo_status": 0,
            }
        }), 200
        
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao autorizar venda: {str(e)}")
        return jsonify({"erro": "Falha ao autorizar venda"}), 500
    finally:
        cursor.close()
        conexao.close()



#=======================================================================================================
# Operações de DELETE 
#=======================================================================================================
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


#=======================================================================================================

# Bloco do Python para executar o script
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)