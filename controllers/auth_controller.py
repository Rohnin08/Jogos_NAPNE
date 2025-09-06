from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import db, Funcionario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form['primeiro_nome'] + ' ' + request.form['segundo_nome']
        email = request.form['email']
        cpf = request.form['cpf']
        especialidade = request.form['especialidade']
        senha = request.form['senha']

        if Funcionario.query.filter_by(email=email).first():
            flash('Este e-mail já está cadastrado.', 'danger')
            return redirect(url_for('auth.cadastro'))

        if Funcionario.query.filter_by(cpf=cpf).first():
            flash('Este CPF já está cadastrado.', 'danger')
            return redirect(url_for('auth.cadastro'))

        senha_hash = generate_password_hash(senha)
        novo_funcionario = Funcionario(nome=nome, email=email, senha=senha_hash, cpf=cpf, especialidade=especialidade)

        db.session.add(novo_funcionario)
        db.session.commit()
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('cadastro.html')

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        senha = request.form.get('senha')

        funcionario = Funcionario.query.filter_by(email=email).first()

        if funcionario and check_password_hash(funcionario.senha, senha):
            session['usuario_id'] = funcionario.id_funcionario
            session['usuario_nome'] = funcionario.nome
            flash('Login realizado com sucesso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha incorretos.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template("login.html")

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('auth.login'))
