from flask import Flask, render_template, request, session, url_for, redirect, flash 
from flask_sqlalchemy import SQLAlchemy
from models import Funcionario, Categoria, Aluno, db, Jogo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        try:
            nome = request.form['primeiro_nome'] + ' ' + request.form['segundo_nome']
            email = request.form['email']
            cpf = request.form['cpf']
            especialidade = request.form['especialidade']
            senha = request.form['senha']

            if Funcionario.query.filter_by(email=email).first():
                flash('Este e-mail já está cadastrado.', 'danger')
                return redirect(url_for('cadastro'))

            if Funcionario.query.filter_by(cpf=cpf).first():
                flash('Este CPF já está cadastrado.', 'danger')
                return redirect(url_for('cadastro'))

            senha_hash = generate_password_hash(senha)

            novo_funcionario = Funcionario(
                nome=nome,
                email=email,
                senha=senha_hash,
                cpf=cpf,
                especialidade=especialidade
            )
            
            db.session.add(novo_funcionario)
            db.session.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))

        except Exception as err:
            flash(f'Erro ao cadastrar: {err}', 'danger')

    return render_template('cadastro.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        senha = request.form.get('senha')

        funcionario = Funcionario.query.filter_by(email=email).first()

        if funcionario:
            if check_password_hash(funcionario.senha, senha):
                session['usuario_id'] = funcionario.id_funcionario
                session['usuario_nome'] = funcionario.nome
                flash('Login realizado com sucesso', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Senha incorreta.', 'danger')
        else:
            flash('Email não encontrado.', 'danger')

        return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    return render_template("dashboard.html")

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('login'))

@app.route('/cadastroCategoria', methods=["GET", "POST"])
def cadastrar_categoria():
    if request.method == "POST":
        nome = request.form.get('nome')
        
        if not nome:
            flash("O nome da categoria é obrigatório.", 'danger')
            return redirect(url_for('cadastrar_categoria'))

        categoria_existente = Categoria.query.filter_by(nome=nome).first()
        if categoria_existente:
            flash("Essa categoria já existe.", 'danger')
            return redirect(url_for('cadastrar_categoria'))

        nova_categoria = Categoria(nome=nome)
        db.session.add(nova_categoria)
        db.session.commit()
        flash("Categoria cadastrada com sucesso!", 'success')
        return redirect(url_for('cadastrar_categoria'))
    
    return render_template("cadastroCategoria.html")

@app.route('/cadastroAluno', methods=["GET", "POST"])
def cadastro_aluno():
    if request.method == "POST":
        nome = request.form.get('nome')
        matricula = request.form.get('matricula')
        necessidade_especial = request.form.get("necessidade_especial")
        observacao = request.form.get("observacao")

        if not nome or not matricula or not necessidade_especial:
            flash("Todos os campos obrigatórios devem ser preenchidos.", 'danger')
            return redirect(url_for('cadastro_aluno'))

        novo_aluno = Aluno(
            nome=nome,
            matricula=matricula,
            necessidade_especial=necessidade_especial, 
            observacao=observacao
        )

        db.session.add(novo_aluno)
        db.session.commit()

        flash("Aluno cadastrado com sucesso!", 'success')
        return redirect(url_for('cadastro_aluno'))

    return render_template("cadastroAluno.html")

@app.route('/cadastroJogos', methods=["GET", "POST"])
def cadastro_jogos():
    if request.method == "POST":
        nome = request.form.get('nome')
        quant = request.form.get('quant')
        descricao = request.form.get('Descricao')

        if not nome or not quant:
            flash("Nome e quantidade são obrigatórios!", "danger")
            return redirect(url_for('cadastro_jogos'))

        try:
            novo_jogo = Jogo(
                nome=nome,
                quant_disponivel=int(quant),
                descricao=descricao
            )
            db.session.add(novo_jogo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
           

        return redirect(url_for('cadastro_jogos'))

    return render_template('cadastroJogos.html')


if __name__ == '__main__':
    app.run(debug=True)
