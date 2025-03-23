create database galeriaArte;

CREATE TABLE Pessoa (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Sobrenome VARCHAR(100) NOT NULL,
    CPF VARCHAR(11) UNIQUE NOT NULL,
    DataNascimento DATE NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    NomeUsuario VARCHAR(30) UNIQUE NOT NULL,
    Senha VARCHAR(255) NOT NULL,
    Telefone VARCHAR(15)
);

CREATE TABLE Endereco (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    PessoaID INT NOT NULL,
    Rua VARCHAR(200) NOT NULL,
    Numero VARCHAR(10) NOT NULL,
    Bairro VARCHAR(100) NOT NULL,
    Cidade VARCHAR(100) NOT NULL,
    Estado VARCHAR(2) NOT NULL,
    CEP VARCHAR(8) NOT NULL,
    Pais VARCHAR(4) NOT NULL,
    FOREIGN KEY (PessoaID) REFERENCES Pessoa(ID)
);

CREATE TABLE Cliente (
    PessoaID INT PRIMARY KEY,
    MatriculaCliente VARCHAR(15) UNIQUE NOT NULL,
    QuantidadeObrasCompradas INT DEFAULT 0,
    NomeUsuario VARCHAR(30) NOT NULL,
    Senha VARCHAR(255) NOT NULL,
    Recomendações TEXT,
    FOREIGN KEY (PessoaID) REFERENCES Pessoa(ID)
);

CREATE TABLE Autor (
    PessoaID INT PRIMARY KEY,
    MatriculaAutor VARCHAR(15) UNIQUE NOT NULL,
    NomeUsuario VARCHAR(30) NOT NULL,
    Senha VARCHAR(255) NOT NULL,
    FOREIGN KEY (PessoaID) REFERENCES Pessoa(ID)
);


CREATE TABLE Funcionario (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    PessoaID INT NOT NULL,
    NomeUsuario VARCHAR(30) UNIQUE NOT NULL,
    Senha VARCHAR(255) NOT NULL,
    Cargo VARCHAR(30) NOT NULL,
    DataContratacao DATE NOT NULL,
    Salario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (PessoaID) REFERENCES Pessoa(ID)
);



CREATE TABLE ObraDeArte (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Imagem LONGBLOB,
    TipoArquivo VARCHAR(10) NOT NULL,
    Titulo VARCHAR(200) NOT NULL,
    Descricao TEXT,
    DataPublicacao DATE NOT NULL,
    EstiloArte VARCHAR(60) NOT NULL,
    AutorID INT NOT NULL,
    PaisGaleria VARCHAR(4) NOT NULL,
    Altura FLOAT NOT NULL,
    Largura FLOAT NOT NULL,
    FOREIGN KEY (AutorID) REFERENCES Autor(PessoaID)
);

CREATE TABLE Galeria (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ObraID INT NOT NULL,
    Valor DECIMAL(11,2) NOT NULL,
    Status TINYINT(1) NOT NULL CHECK (Status IN (0, 1, 2)),
    FOREIGN KEY (ObraID) REFERENCES ObraDeArte(ID)
);

CREATE TABLE Venda (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ClienteID INT NOT NULL,
    FuncionarioID INT NOT NULL,
    PedidoID VARCHAR(20) UNIQUE NOT NULL,
    ValorTotal DECIMAL(10,2) NOT NULL,
    DataVenda DATE NOT NULL,
    FOREIGN KEY (ClienteID) REFERENCES Cliente(PessoaID),
    FOREIGN KEY (FuncionarioID) REFERENCES Funcionario(ID)
);

CREATE TABLE Pedido (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    VendaID INT NOT NULL,
    ObraID INT NOT NULL,
    Valor DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (VendaID) REFERENCES Venda(ID),
    FOREIGN KEY (ObraID) REFERENCES ObraDeArte(ID)
);

CREATE TABLE Pagamento (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    VendaID INT NOT NULL,
    ValorTotalPago DECIMAL(10,2) NOT NULL,
    MetodoPagamento VARCHAR(20) NOT NULL,
    Situacao TINYINT(1) NOT NULL CHECK (Situacao IN (1, 2)),
    FOREIGN KEY (VendaID) REFERENCES Venda(ID)
);

