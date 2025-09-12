from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import db, Jogo, Categoria

jogo_bp = Blueprint('jogo', __name__, template_folder='templates')

# LISTAGEM DE JOGOS
@jogo_bp.route('/')
def jogo():
    jogos = Jogo.query.all()
    categorias = Categoria.query.all()
    return render_template('jogos.html', jogos=jogos, categorias=categorias)

# CADASTRO DE JOGO
@jogo_bp.route('/cadastrar', methods=['POST'])
def cadastrar_jogo():
    nome = request.form.get('nome')
    quant = request.form.get('quant')
    descricao = request.form.get('descricao')
    categoria_ids = request.form.getlist('categoria')

    if not nome or not quant or not categoria_ids:
        flash("Todos os campos são obrigatórios!", "danger")
        return redirect(url_for('jogo.jogo')) # CORRIGIDO

    try:
        novo_jogo = Jogo(nome=nome, quant_disponivel=int(quant), descricao=descricao)
        db.session.add(novo_jogo)
        db.session.commit()

        for cat_id in categoria_ids:
            categoria = Categoria.query.get(int(cat_id))
            if categoria:
                novo_jogo.categorias.append(categoria)
        db.session.commit()

        flash("Jogo cadastrado com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao cadastrar o jogo: {e}", "danger")

    return redirect(url_for('jogo.jogo')) # CORRIGIDO

# EDIÇÃO DE JOGO
@jogo_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_jogo(id):
    jogo_obj = Jogo.query.get_or_404(id)
    categorias = Categoria.query.all()
    if request.method == 'POST':
        jogo_obj.nome = request.form.get('nome')
        jogo_obj.quant_disponivel = int(request.form.get('quant'))
        jogo_obj.descricao = request.form.get('descricao')

        categoria_ids = request.form.getlist('categoria')
        if categoria_ids:
            jogo_obj.categorias = []
            for cat_id in categoria_ids:
                categoria = Categoria.query.get(int(cat_id))
                if categoria:
                    jogo_obj.categorias.append(categoria)

        db.session.commit()
        flash("Jogo atualizado com sucesso!", "success")
        return redirect(url_for('jogo.jogo')) # CORRIGIDO

    return render_template('editar_jogo.html', jogo=jogo_obj, categorias=categorias)

# EXCLUSÃO DE JOGO
@jogo_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    jogo_obj = Jogo.query.get_or_404(id)
    db.session.delete(jogo_obj)
    db.session.commit()
    flash("Jogo excluído com sucesso!", "success")
    return redirect(url_for('jogo.jogo')) # CORRIGIDO

# CADASTRO DE CATEGORIA
@jogo_bp.route('/categorias/cadastrar', methods=['POST'])
def cadastrar_categoria():
    nome = request.form.get('nome')
    if not nome:
        flash("O nome da categoria é obrigatório!", "danger")
        return redirect(url_for('jogo.jogo')) # CORRIGIDO

    categoria_existente = Categoria.query.filter_by(nome=nome).first()
    if categoria_existente:
        flash("Essa categoria já existe.", "danger")
        return redirect(url_for('jogo.jogo')) # CORRIGIDO

    nova_categoria = Categoria(nome=nome)
    db.session.add(nova_categoria)
    db.session.commit()
    flash("Categoria cadastrada com sucesso!", "success")
    return redirect(url_for('jogo.jogo')) # CORRIGIDO