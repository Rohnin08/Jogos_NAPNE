CREATE TABLE IF NOT EXISTS Funcionario (
    id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(100),
    telefone VARCHAR(14) NOT NULL,
    especialidade VARCHAR(400)

);

CREATE TABLE IF NOT EXISTS Alunos (
    id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100),
    matricula CHAR(13),
    necessidade_especial VARCHAR(100),
    observacao VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS Categoria (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Jogos (
    id_jogos INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100),
    quant_disponivel INTEGER,
    descricao VARCHAR(400)
);

CREATE TABLE IF NOT EXISTS Jogos_Categoria (
    id_jogos_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    id_categoria INTEGER NOT NULL,
    id_jogos INTEGER NOT NULL,
    FOREIGN KEY (id_jogos) REFERENCES Jogos(id_jogos),
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria)

);

CREATE TABLE IF NOT EXISTS Jogos_Atendimento (
    id_jogos_atendimento INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    id_jogos int NOT NULL,
    FOREIGN KEY (id_jogos) REFERENCES Jogos (id_jogos)
);


CREATE TABLE IF NOT EXISTS Atendimento (
    id_atendimento INTEGER PRIMARY KEY AUTOINCREMENT,
    progresso_aluno VARCHAR(400),
    id_aluno INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    id_jogos_atendimento INTEGER NOT NULL,
    data DATE NOT NULL,
    FOREIGN KEY (id_aluno) REFERENCES Alunos(id_aluno),
    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario),
    FOREIGN KEY (id_jogos_atendimento) REFERENCES Jogos_Atendimento(id_jogos_atendimento)
);

