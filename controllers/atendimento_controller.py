from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models.models import db, Atendimento, Aluno, Jogo
from datetime import date

atendimento_bp = Blueprint('atendimento', __name__, template_folder='templates')

# Decorator para exigir login
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

# =========================
# LISTAGEM DE ATENDIMENTOS
# =========================
@atendimento_bp.route('/')
@login_required
def atendimento():
    atendimentos = Atendimento.query.order_by(Atendimento.data_atendimento.desc()).all()
    alunos = Aluno.query.all()  # necessário para o modal de cadastro
    jogos = Jogo.query.all()    # necessário para o modal de cadastro
    return render_template('atendimentos.html', atendimentos=atendimentos, alunos=alunos, jogos=jogos)

# =========================
# CADASTRO DE ATENDIMENTO
# =========================
@atendimento_bp.route('/cadastrar', methods=['POST'])
@login_required
def cadastrar_atendimento():
    aluno_ids = request.form.getlist('alunos')
    jogo_ids = request.form.getlist('jogos')
    progresso = request.form.get('progresso')

    if not aluno_ids or not jogo_ids:
        flash("Selecione pelo menos um aluno e um jogo.", "danger")
        return redirect(url_for('atendimento.atendimento'))

    novo_atendimento = Atendimento(
        progresso_aluno=progresso,
        data_atendimento=date.today(),
        id_funcionario=session['usuario_id']
    )

    # Vincula os alunos selecionados
    for aluno_id in aluno_ids:
        aluno = Aluno.query.get(aluno_id)
        if aluno:
            novo_atendimento.alunos.append(aluno)

    # Vincula os jogos selecionados
    for jogo_id in jogo_ids:
        jogo = Jogo.query.get(jogo_id)
        if jogo:
            novo_atendimento.jogos.append(jogo)

    try:
        db.session.add(novo_atendimento)
        db.session.commit()
        flash("Atendimento cadastrado com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao cadastrar atendimento: {e}", "danger")

    return redirect(url_for('atendimento.atendimento'))

# =========================
# EDIÇÃO DE ATENDIMENTO
# =========================
@atendimento_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_atendimento(id):
    atendimento_obj = Atendimento.query.get_or_404(id)
    alunos = Aluno.query.all()
    jogos = Jogo.query.all()

    if request.method == 'POST':
        atendimento_obj.progresso_aluno = request.form.get('progresso')

        # Atualiza alunos
        aluno_ids = request.form.getlist('alunos')
        atendimento_obj.alunos = []
        for aluno_id in aluno_ids:
            aluno = Aluno.query.get(aluno_id)
            if aluno:
                atendimento_obj.alunos.append(aluno)

        # Atualiza jogos
        jogo_ids = request.form.getlist('jogos')
        atendimento_obj.jogos = []
        for jogo_id in jogo_ids:
            jogo = Jogo.query.get(jogo_id)
            if jogo:
                atendimento_obj.jogos.append(jogo)

        try:
            db.session.commit()
            flash("Atendimento atualizado com sucesso!", "success")
            return redirect(url_for('atendimento.atendimento'))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar atendimento: {e}", "danger")
            return redirect(url_for('atendimento.editar_atendimento', id=id))

    return render_template('editarAtendimento.html', atendimento=atendimento_obj, alunos=alunos, jogos=jogos)

# =========================
# EXCLUSÃO DE ATENDIMENTO
# =========================
@atendimento_bp.route('/excluir/<int:id>', methods=['POST', 'GET'])
@login_required
def excluir_atendimento(id):
    atendimento_obj = Atendimento.query.get_or_404(id)
    try:
        db.session.delete(atendimento_obj)
        db.session.commit()
        flash("Atendimento excluído com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir atendimento: {e}", "danger")
    return redirect(url_for('atendimento.atendimento'))
