from flask import Flask, render_template, request, session, url_for, redirect, flash 
from flask_sqlalchemy import SQLAlchemy
from models import Funcionario, db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para usar flash()

# Configuração do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco com o app
db.init_app(app)

# Cria as tabelas se não existirem
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
            telefone = request.form.get('telefone', '')  # opcional

            if Funcionario.query.filter_by(email=email).first():
                print('Este e-mail já está cadastrado.', 'danger')
                flash('Este e-mail já está cadastrado.', 'danger')
                return redirect(url_for('cadastro'))

            if Funcionario.query.filter_by(cpf=cpf).first():
                print('Este e-mail já está cadastrado.', 'danger')
                flash('Este CPF já está cadastrado.', 'danger')
                return redirect(url_for('cadastro'))

            senha_hash = generate_password_hash(senha)

            novo_funcionario = Funcionario(
                nome=nome,
                email=email,
                senha=senha_hash,
                cpf=cpf,
                telefone=telefone,
                especialidade=especialidade
            )
            

            db.session.add(novo_funcionario)
            db.session.commit()
            print("Comitado no banco")
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))

        except Exception as err:
            print(err)

    return render_template('cadastro.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        senha = request.form['senha']

        funcionario = Funcionario.query.filter_by(email=email).first()

        if funcionario and check_password_hash(funcionario.senha, senha):
            session['usuario_id'] = funcionario.id_funcionario
            session['usuario_nome'] = funcionario.nome
            flash('Login realizado com sucesso', 'success')
        else:
            flash('Email ou senha encorreto, por favor tente novamente', 'danger')
            return(redirect(url_for('login')))
        
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        flash('Não sei como você veio parar aqui, mas sei que você deve sair', 'warning')
        return redirect(url_for('login'))
    return f"Bem-vindo {session['usuario_nome']}"

if __name__ == '__main__':
    app.run(debug=True)
