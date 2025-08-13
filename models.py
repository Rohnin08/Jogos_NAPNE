from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Funcionario(db.Model):
    __tablename__ = 'funcionario'
    id_funcionario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(14))
    especialidade = db.Column(db.String(400), nullable=False)

    atendimentos = db.relationship('Atendimento', backref='funcionario', lazy=True)


class Aluno(db.Model):
    __tablename__ = 'aluno'
    id_aluno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(13), nullable=False, unique=True)
    necessidade_especial = db.Column(db.String(100), nullable=False)
    observacao = db.Column(db.String(200))

    atendimentos = db.relationship(
        'Atendimento',
        secondary='atendimento_aluno',
        back_populates='alunos',
        lazy='subquery'
    )


class Categoria(db.Model):
    __tablename__ = 'categoria'
    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)

    jogos_categorias = db.relationship('JogosCategoria', backref='categoria', lazy=True)


class Jogo(db.Model):
    __tablename__ = 'jogo'
    id_jogo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    quant_disponivel = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(400))

    jogos_categorias = db.relationship('JogosCategoria', backref='jogo', lazy=True)

    atendimentos = db.relationship(
        'Atendimento',
        secondary='atendimento_jogo',
        back_populates='jogos',
        lazy='subquery'
    )


class JogosCategoria(db.Model):
    __tablename__ = 'jogos_categoria'
    id_jogos_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False)
    id_jogo = db.Column(db.Integer, db.ForeignKey('jogo.id_jogo'), nullable=False)


# Tabela associativa Atendimento ↔ Aluno
atendimento_aluno = db.Table(
    'atendimento_aluno',
    db.Column('id_atendimento', db.Integer, db.ForeignKey('atendimento.id_atendimento'), primary_key=True),
    db.Column('id_aluno', db.Integer, db.ForeignKey('aluno.id_aluno'), primary_key=True)
)

# Tabela associativa Atendimento ↔ Jogo
atendimento_jogo = db.Table(
    'atendimento_jogo',
    db.Column('id_atendimento', db.Integer, db.ForeignKey('atendimento.id_atendimento'), primary_key=True),
    db.Column('id_jogo', db.Integer, db.ForeignKey('jogo.id_jogo'), primary_key=True)
)


class Atendimento(db.Model):
    __tablename__ = 'atendimento'
    id_atendimento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    progresso_aluno = db.Column(db.String(400))
    data_atendimento = db.Column(db.Date, nullable=False)
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionario.id_funcionario'), nullable=False)

    alunos = db.relationship(
        'Aluno',
        secondary=atendimento_aluno,
        back_populates='atendimentos',
        lazy='subquery'
    )

    jogos = db.relationship(
        'Jogo',
        secondary=atendimento_jogo,
        back_populates='atendimentos',
        lazy='subquery'
    )
