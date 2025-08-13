CREATE TABLE IF NOT EXISTS Funcionario (
    id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(100) NOT NULL,
    telefone VARCHAR(14),
    especialidade VARCHAR(400) NOT NULL
);

CREATE TABLE IF NOT EXISTS Aluno (
    id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    matricula VARCHAR(13) NOT NULL,
    necessidade_especial VARCHAR(100) NOT NULL,
    observacao VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS Categoria (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Jogo (
    id_jogo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    quant_disponivel INTEGER NOT NULL,
    descricao VARCHAR(400)
);

CREATE TABLE IF NOT EXISTS Jogos_Categoria (
    id_jogos_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    id_categoria INTEGER NOT NULL,
    id_jogo INTEGER NOT NULL,
    FOREIGN KEY (id_jogo) REFERENCES Jogo(id_jogo),
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria)
);

CREATE TABLE IF NOT EXISTS Atendimento (
    id_atendimento INTEGER PRIMARY KEY AUTOINCREMENT,
    progresso_aluno VARCHAR(400),
    data_atendimento DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Atendimento_Aluno (
    id_atendimento INTEGER NOT NULL,
    id_aluno INTEGER NOT NULL,
    PRIMARY KEY (id_atendimento, id_aluno),
    FOREIGN KEY (id_atendimento) REFERENCES Atendimento(id_atendimento) ON DELETE CASCADE,
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Atendimento_Jogo (
    id_atendimento INTEGER NOT NULL,
    id_jogo INTEGER NOT NULL,
    PRIMARY KEY (id_atendimento, id_jogo),
    FOREIGN KEY (id_atendimento) REFERENCES Atendimento(id_atendimento) ON DELETE CASCADE,
    FOREIGN KEY (id_jogo) REFERENCES Jogo(id_jogo) ON DELETE CASCADE
);
