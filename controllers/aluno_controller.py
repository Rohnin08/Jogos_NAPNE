from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models.models import db, Aluno

aluno_bp = Blueprint('aluno', __name__, template_folder='templates')

# Decorator para exigir login
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

# LISTAGEM DE ALUNOS
@aluno_bp.route('/')
@login_required
def aluno():
    alunos = Aluno.query.all()
    return render_template('alunos.html', alunos=alunos)

# CADASTRO DE ALUNO
@aluno_bp.route('/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_aluno():
    if request.method == 'POST':
        nome = request.form.get('nome')
        matricula = request.form.get('matricula')
        necessidade_especial = request.form.get('necessidade_especial')
        observacao = request.form.get('observacao')

        if not nome or not matricula or not necessidade_especial:
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'danger')
            return redirect(url_for('aluno.cadastrar_aluno'))

        if Aluno.query.filter_by(matricula=matricula).first():
            flash('Essa matrícula já está cadastrada.', 'danger')
            return redirect(url_for('aluno.cadastrar_aluno'))

        novo_aluno = Aluno(
            nome=nome,
            matricula=matricula,
            necessidade_especial=necessidade_especial,
            observacao=observacao
        )
        try:
            db.session.add(novo_aluno)
            db.session.commit()
            flash('Aluno cadastrado com sucesso!', 'success')
            return redirect(url_for('aluno.aluno'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar aluno: {e}', 'danger')
            return redirect(url_for('aluno.cadastrar_aluno'))

    return render_template('cadastroAluno.html')

# EDIÇÃO DE ALUNO
@aluno_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_aluno(id):
    aluno_obj = Aluno.query.get_or_404(id)
    if request.method == 'POST':
        nome = request.form.get('nome')
        matricula = request.form.get('matricula')
        necessidade_especial = request.form.get('necessidade_especial')
        observacao = request.form.get('observacao')

        existente = Aluno.query.filter_by(matricula=matricula).first()
        if existente and existente.id_aluno != aluno_obj.id_aluno:
            flash('Essa matrícula já está em uso por outro aluno.', 'danger')
            return redirect(url_for('aluno.editar_aluno', id=id))

        aluno_obj.nome = nome
        aluno_obj.matricula = matricula
        aluno_obj.necessidade_especial = necessidade_especial
        aluno_obj.observacao = observacao

        try:
            db.session.commit()
            flash('Aluno atualizado com sucesso!', 'success')
            return redirect(url_for('aluno.aluno'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar aluno: {e}', 'danger')
            return redirect(url_for('aluno.editar_aluno', id=id))

    return render_template('editar_aluno.html', aluno=aluno_obj)

# EXCLUSÃO DE ALUNO
@aluno_bp.route('/excluir/<int:id>', methods=['POST', 'GET'])
@login_required
def excluir_aluno(id):
    aluno_obj = Aluno.query.get_or_404(id)
    try:
        db.session.delete(aluno_obj)
        db.session.commit()
        flash('Aluno excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir aluno: {e}', 'danger')
    return redirect(url_for('aluno.aluno'))
