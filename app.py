from flask import Flask, render_template, request, url_for, redirect, flash 
# from flask_sqlalchemy import SQLAlchemy
from models import Funcionario, db
from werkzeug.security import generate_password_hash


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form['primeiro_nome'] + ' ' + request.form['segundo_nome']
        email = request.form['email']
        cpf = request.form['cpf']
        especialidade = request.form['especialidade']
        senha = request.form['senha']
        telefone = request.form.get('telefone', '')  # opcional

        # Validações básicas
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
            telefone=telefone,
            especialidade=especialidade
        )

        db.session.add(novo_funcionario)
        db.session.commit()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

if __name__ == "__main__":
    app.run(debug=True)
