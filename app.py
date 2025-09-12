from flask import Flask, render_template, session, url_for, redirect, flash
from models.models import db
from controllers.auth_controller import auth_bp
from controllers.jogo_controller import jogo_bp
from controllers.aluno_controller import aluno_bp
from controllers.atendimento_controller import atendimento_bp

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Cria o banco na primeira execução
with app.app_context():
    db.create_all()

# Registro dos blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(jogo_bp, url_prefix='/jogos')
app.register_blueprint(aluno_bp, url_prefix='/alunos')
app.register_blueprint(atendimento_bp, url_prefix='/atendimentos')

# Rota inicial
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
