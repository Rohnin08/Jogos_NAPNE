from flask import Flask, render_template, request, session, url_for, redirect, flash
from models.models import Funcionario, Categoria, Aluno, db, Jogo, Atendimento
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

# IMPORT CORRETO DOS BLUEPRINTS
from controllers.auth_controller import auth_bp
from controllers.jogo_controller import jogo_bp
from controllers.aluno_controller import aluno_bp   # <--- IMPORT CORRETO
from controllers.atendimento_controller import atendimento_bp


app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# CRIE/THEME o banco caso precise (somente em dev)
with app.app_context():
    db.create_all()

# REGISTRE OS BLUEPRINTS (prefixos opcionais)
app.register_blueprint(auth_bp)                 # rotas de auth como /login, /cadastro
app.register_blueprint(jogo_bp, url_prefix='') # pode ajustar para url_prefix='/jogos' se preferir
app.register_blueprint(aluno_bp, url_prefix='/alunos')
app.register_blueprint(atendimento_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'warning')
        return redirect(url_for('auth.login'))
    return render_template("dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)



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
    jogos = Jogo.query.all()  # mantém como objetos
    return render_template("listar_jogos.html", jogos=jogos)

@app.route('/alunos')
def listar_alunos():
    # Busca todos os alunos no banco de dados
    alunos = Aluno.query.all()
    # Renderiza o template, passando a lista de alunos
    return render_template('listar_alunos.html', alunos=alunos)


# Adicione esta rota no seu arquivo app.py
@app.route('/alunos/editar/<int:id>', methods=['GET', 'POST'])
def editar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    if request.method == 'POST':
        aluno.nome = request.form.get('nome')
        aluno.matricula = request.form.get('matricula')
        aluno.necessidade_especial = request.form.get('necessidade_especial')
        aluno.observacao = request.form.get('observacao')
        db.session.commit()
        flash('Aluno atualizado com sucesso!', 'success')
        return redirect(url_for('listar_alunos'))
    
    return render_template('editar_aluno.html', aluno=aluno)

# Adicione a rota de exclusão também
@app.route('/alunos/excluir/<int:id>', methods=['POST', 'GET'])
def excluir_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    flash('Aluno excluído com sucesso!', 'success')
    return redirect(url_for('listar_alunos'))

@app.route('/jogos/editar/<int:id>', methods=['GET', 'POST'])
def editar_jogo(id):
    jogo = Jogo.query.get_or_404(id)
    categorias = Categoria.query.all()

    if request.method == 'POST':
        jogo.nome = request.form.get('nome')
        jogo.quant_disponivel = int(request.form.get('quant'))
        jogo.descricao = request.form.get('descricao')

        categoria_id = request.form.get('categoria')
        if categoria_id:
            categoria = Categoria.query.get(int(categoria_id))
            if categoria and categoria not in jogo.categorias:
                jogo.categorias = [categoria]  # ou append, dependendo da lógica

        db.session.commit()
        flash('Jogo atualizado com sucesso!', 'success')
        return redirect(url_for('listar_jogos'))

    return render_template('editar_jogo.html', jogo=jogo, categorias=categorias)

@app.route('/jogos/excluir/<int:id>', methods=['POST', 'GET'])
def excluir_jogo(id):
    jogo = Jogo.query.get_or_404(id)
    db.session.delete(jogo)
    db.session.commit()
    flash('Jogo excluído com sucesso!', 'success')
    return redirect(url_for('listar_jogos'))

if __name__ == '__main__':
    app.run(debug=True)
