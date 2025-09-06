from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import db, Jogo, Categoria

jogo_bp = Blueprint("jogo", __name__)

# -------------------------------
# LISTAGEM DE JOGOS
# -------------------------------
@jogo_bp.route("/jogos")
def listar_jogos():
    jogos = Jogo.query.all()
    categorias = Categoria.query.all()
    return render_template("listar_jogos.html", jogos=jogos, categorias=categorias)

# -------------------------------
# CADASTRO DE JOGO (SUPORTE MULTIPLAS CATEGORIAS)
# -------------------------------
@jogo_bp.route("/jogos/cadastrar", methods=["POST"])
def cadastrar_jogo():
    nome = request.form.get('nome')
    quant = request.form.get('quant')
    descricao = request.form.get('descricao')
    categoria_ids = request.form.getlist('categoria')  # lista de ids para múltiplas categorias

    if not nome or not quant or not categoria_ids:
        flash("Todos os campos são obrigatórios!", "danger")
        return redirect(url_for("jogo.listar_jogos"))

    try:
        novo_jogo = Jogo(nome=nome, quant_disponivel=int(quant), descricao=descricao)
        db.session.add(novo_jogo)
        db.session.commit()

        # Vincular categorias múltiplas
        for cat_id in categoria_ids:
            categoria = Categoria.query.get(int(cat_id))
            if categoria:
                novo_jogo.categorias.append(categoria)
        db.session.commit()

        flash("Jogo cadastrado com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao cadastrar o jogo: {e}", "danger")

    return redirect(url_for("jogo.listar_jogos"))

# -------------------------------
# EDIÇÃO DE JOGO
# -------------------------------
@jogo_bp.route("/jogos/editar/<int:id>", methods=["POST"])
def editar_jogo(id):
    jogo = Jogo.query.get_or_404(id)
    jogo.nome = request.form.get('nome')
    jogo.quant_disponivel = int(request.form.get('quant'))
    jogo.descricao = request.form.get('descricao')

    categoria_ids = request.form.getlist('categoria')  # múltiplas categorias
    if categoria_ids:
        jogo.categorias = []  # limpa categorias antigas
        for cat_id in categoria_ids:
            categoria = Categoria.query.get(int(cat_id))
            if categoria:
                jogo.categorias.append(categoria)

    db.session.commit()
    flash("Jogo atualizado com sucesso!", "success")
    return redirect(url_for("jogo.listar_jogos"))

# -------------------------------
# EXCLUSÃO DE JOGO
# -------------------------------
@jogo_bp.route("/jogos/excluir/<int:id>", methods=["POST"])
def excluir_jogo(id):
    jogo = Jogo.query.get_or_404(id)
    db.session.delete(jogo)
    db.session.commit()
    flash("Jogo excluído com sucesso!", "success")
    return redirect(url_for("jogo.listar_jogos"))

# -------------------------------
# CADASTRO DE CATEGORIA
# -------------------------------
@jogo_bp.route("/categorias/cadastrar", methods=["POST"])
def cadastrar_categoria():
    nome = request.form.get('nome')
    if not nome:
        flash("O nome da categoria é obrigatório!", "danger")
        return redirect(url_for("jogo.listar_jogos"))

    categoria_existente = Categoria.query.filter_by(nome=nome).first()
    if categoria_existente:
        flash("Essa categoria já existe.", "danger")
        return redirect(url_for("jogo.listar_jogos"))

    nova_categoria = Categoria(nome=nome)
    db.session.add(nova_categoria)
    db.session.commit()
    flash("Categoria cadastrada com sucesso!", "success")
    return redirect(url_for("jogo.listar_jogos"))
