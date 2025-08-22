from flask import Flask, render_template, request, session, url_for, redirect, flash #Importação do flask e funções dele.
from models import Funcionario, Categoria, Aluno, db, Jogo, Atendimento #Importação das tabelas de models
from werkzeug.security import generate_password_hash, check_password_hash #Importar o hash
from datetime import date

app = Flask(__name__) #Definição dessa pagina como o app da aplicação
app.secret_key = 'sua_chave_secreta_aqui'  #Secret key generica

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #Configurações do banco de dados da aplicação
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db.init_app(app) #Inicialização do banco de dados

with app.app_context(): 
    db.create_all()

@app.route('/') #Rota da pagina inicial "index.html"
def index():
    return render_template("index.html")

@app.route('/cadastro', methods=["GET", "POST"]) #Rota de cadastro
def cadastro():
    if request.method == "POST": #Requisição  com metodo post: ele enviara as informações para o banco de dados.
        try:
            nome = request.form['primeiro_nome'] + ' ' + request.form['segundo_nome'] #Concatena  as strings nome e sobrenome
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

            senha_hash = generate_password_hash(senha) #Gera o hash da senha do usuário, vai criptografar a senha, aumentando assim a segurança.

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

from flask import render_template, request, redirect, url_for, flash
from models import db, Jogo, Categoria, JogosCategoria  # certifique-se que Categoria está importado

@app.route('/cadastroJogos', methods=["GET", "POST"])
def cadastro_jogos():
    categorias = Categoria.query.all()

    if request.method == "POST":
        nome = request.form.get('nome')
        quant = request.form.get('quant')
        descricao = request.form.get('Descricao')
        id_categoria = request.form.get('categoria')  # pega ID da categoria selecionada

        if not nome or not quant or not id_categoria:
            flash("Todos os campos são obrigatórios!", "danger")
            return redirect(url_for('cadastro_jogos'))

        try:
            novo_jogo = Jogo(
                nome=nome,
                quant_disponivel=int(quant),
                descricao=descricao
            )
            db.session.add(novo_jogo)
            db.session.commit()

            relacao = JogosCategoria(
                id_jogo=novo_jogo.id_jogo,
                id_categoria=int(id_categoria)
            )
            db.session.add(relacao)
            db.session.commit()

        except Exception as e:
            db.session.rollback()

        return redirect(url_for('cadastro_jogos'))

    return render_template('cadastroJogos.html', categorias=categorias)

#Cadastro de atendimentos
@app.route('/cadastroAtendimento', methods=['GET', 'POST'])
def cadastro_atendimento():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para cadastrar um atendimento.', 'warning')
        return redirect(url_for('login'))

    alunos = Aluno.query.all()
    jogos = Jogo.query.all()

    if request.method == 'POST':
        aluno_ids = request.form.getlist('alunos')
        jogo_ids = request.form.getlist('jogos')
        progresso = request.form.get('progresso')

        if not aluno_ids or not jogo_ids:
            flash("Selecione pelo menos um aluno e um jogo.", "danger")
            return redirect(url_for('cadastro_atendimento'))

        novo_atendimento = Atendimento(
            progresso_aluno=progresso,
            data_atendimento=date.today(),
            id_funcionario=session['usuario_id']
        )

        for aluno_id in aluno_ids:
            aluno = Aluno.query.get(aluno_id)
            if aluno:
                novo_atendimento.alunos.append(aluno)

        for jogo_id in jogo_ids:
            jogo = Jogo.query.get(jogo_id)
            if jogo:
                novo_atendimento.jogos.append(jogo)

        try:
            db.session.add(novo_atendimento)
            db.session.commit()
            flash("Atendimento cadastrado com sucesso!", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            print(e)  # <-- Aqui imprime o erro no console
            raise      # <-- Aqui relança o erro para não silenciar

    return render_template('cadastroAtendimento.html', alunos=alunos, jogos=jogos)


@app.route("/jogos")
def listar_jogos():
    jogos = Jogo.query.all()
    jogos_formatados = []
    for j in jogos:
        categorias = ", ".join([c.nome for c in j.categorias]) if j.categorias else "Sem categoria"
        jogos_formatados.append({
            "id": j.id_jogo,
            "nome": j.nome,
            "quant": j.quant_disponivel,
            "descricao": j.descricao or "Sem descrição",
            "categorias": categorias
        })
    return render_template("listar_jogos.html", jogos=jogos_formatados)

if __name__ == '__main__':
    app.run(debug=True)
