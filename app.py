from sqlalchemy import select
from sqlalchemy.testing import db
from werkzeug.security import check_password_hash, generate_password_hash

from models import db_session, Funcionario, Produto, Movimentacao
from flask import flash, url_for, Flask, render_template, redirect, request, session
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
app.secret_key = 'uma_chave_secreta'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_funcionario = request.form.get('email_funcionario')
        senha_funcionario = request.form.get('senha_funcionario')
        funcionario = Funcionario.query.filter_by(email_funcionario=email_funcionario).first()
        if funcionario and check_password_hash(funcionario.senha_funcionario, senha_funcionario):
            session['email_funcionario'] = email_funcionario
            return redirect(url_for('inicial'))

        flash('Email ou senha incorretos. Tente novamente.', 'danger')
    return render_template('login.html')


@app.route('/funcionario/cadastrar', methods=['GET', 'POST'])
def cadastrar_funcionario():
    if request.method == "POST":
        if not request.form["nome_funcionario"]:
            flash("Preencher o nome", "error")
        if not request.form["email_funcionario"]:
            flash("Preencher o email", "error")
        if not request.form["senha_funcionario"]:
            flash("Preencher o senha", "error")
        else:
            form_evento = Funcionario(nome_funcionario=request.form["nome_funcionario"],
                                      email_funcionario=request.form["email_funcionario"],
                                      senha_funcionario=generate_password_hash(request.form["senha_funcionario"]),)
            print(form_evento)
            form_evento.save()
            db_session.close()
            flash("Evento criado!!!", "success")
            return redirect(url_for('inicial'))

    return render_template('cadastro.html')


@app.route('/inicial')
def inicial():

    estoque_produtos = select(Produto).select_from(Produto)
    estoque_produtos = db_session.execute(estoque_produtos).scalars()
    estoqueProduto = []
    for produto in estoque_produtos:
        estoqueProduto.append(produto.serialize_produto())
    print(estoqueProduto)

    return render_template('inicial.html',lista_produtos=estoqueProduto)

@app.route('/funcionarioInicial/<int:id>', methods=['POST', 'GET'])
def funcionárioInicial(id):
    funcionário = select(Funcionario).where(Funcionario.funcionario_id == id)
    print(funcionário)
    funcionario_sel = db_session.execute(funcionário).scalar()
    print(funcionario_sel)

    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('listar_estoque'))
    # db_session.commit()


@app.route('/produto/cadastrar', methods=['POST', 'GET'])
def cadastrar_produto():
    if request.method == "POST":
        if not request.form["nome_produto"]:
            flash("Preencher o nome", "error")
        if not request.form["quantidade_produto"]:
            flash("Preencher o quantidade", "error")
        if not request.form["codigo_produto"]:
            flash("Preencher o codigo", "error")
        if not request.form["categoria_produto"]:
            flash("Preencher o categoria", "error")
        if not request.form["preco_produto"]:
            flash("Preencher o preco", "error")
        if not request.form["validade_produto"]:
            flash("Preencher o validade", "error")
        else:
            form_evento = Produto(nome_produto=request.form["nome_produto"],
                                  quantidade_produto=int(request.form["quantidade_produto"]),
                                  codigo_produto=request.form["codigo_produto"],
                                  categoria_produto=request.form["categoria_produto"],
                                  preco_produto=request.form["preco_produto"],
                                  validade_produto=request.form["validade_produto"])
            print(form_evento)
            form_evento.save()
            db_session.close()
            flash("Evento cadastrado!!!", "success")
            return redirect(url_for('listar_estoque'))
    return render_template('produto.html')

@app.route('/historico')
def historico():
    lista_movimentacoes = select(Movimentacao).select_from(Movimentacao)
    lista_movimentacoes = db_session.execute(lista_movimentacoes).scalars()
    listaMovimentacoes = []
    for movimentacoes in lista_movimentacoes:
        listaMovimentacoes.append(movimentacoes.serialize_movimentacao())
    print(listaMovimentacoes)
    return render_template('historico.html', var_movimentacao=listaMovimentacoes)


@app.route('/estoque')
def listar_estoque():
    estoque_produtos = select(Produto).select_from(Produto)
    estoque_produtos = db_session.execute(estoque_produtos).scalars()
    estoqueProduto = []
    for produto in estoque_produtos:
        estoqueProduto.append(produto.serialize_produto())
    print(estoqueProduto)
    return render_template('estoque.html', var_produtos=estoqueProduto)

@app.route('/funcionario/lista')
def funcionario():
    lista_funcionario = select(Funcionario).select_from(Funcionario)
    lista_funcionario = db_session.execute(lista_funcionario).scalars()
    listaFuncionario = []
    for funcionario in lista_funcionario:
        listaFuncionario.append(funcionario.serialize_funcionario())
    print(listaFuncionario)
    return render_template('funcionario.html', var_funcionarios=listaFuncionario)

@app.route('/editarProduto/<int:id>', methods=['POST', 'GET'])
def editarProduto(id):
    produto = Produto.query.get(id)
    if produto is None:
        flash('Produto inexistente', 'error')
        return redirect(url_for('listar_estoque'))

    if request.method == 'POST':
        form_data = request.form
        produto.nome_produto = form_data['nome_produto']
        produto.codigo_produto = form_data['codigo_produto']
        produto.categoria_produto = form_data['categoria_produto']
        produto.preco_produto = form_data['preco_produto']
        produto.quantidade_produto = form_data['quantidade_produto']
        produto.validade_produto = form_data['validade_produto']

        try:
            db_session.commit()
            flash('Produto atualizado com sucesso!', 'success')
        except Exception as e:
            db_session.rollback()
            flash('Erro ao atualizar produto: {}'.format(e), 'error')

        return redirect(url_for('historico'))

    return render_template('editar.html', produto=produto)


@app.route('/deletarProduto/<int:id>', methods=['POST', 'GET'])
def deletarProduto(id):
    produto = select(Produto).where(Produto.produto_id == id)
    print(produto)
    produto_del = db_session.execute(produto).scalar()
    print(produto_del)
    produto_del.delete()
    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('listar_estoque'))
    # db_session.commit()

@app.route('/movimentacaoProduto', methods=['POST', "GET"])
def movimentacaoProduto():
    if request.method == 'POST':
        if not request.form['produto_id']:
            flash("Escolha um produto para cadastrar uma entrada no estoque!", "error")
        if not request.form['funcionario_id']:
            flash("Informe o funcionário que está movimentando!", "error")
        if not request.form['quantidade_movimentacao']:
            flash("Informe quantos produtos foram inseridos no estoque!", "error")
        if not request.form['data_de_movimentacao']:
            flash("Informe a data da movimentação!", "error")
        if not request.form['tipo_movimentacao']:
            flash("Informe o tipo de movimentacao!", "error")

        else:
            form_evento = Movimentacao(produto_id=int(request.form['produto_id']),
                                       funcionario_id=int(request.form['funcionario_id']),
                                       quantidade_movimentacao=int(request.form['quantidade_movimentacao']),
                                       data_de_movimentacao=request.form['data_de_movimentacao'],
                                       tipo_movimentacao=bool(int(request.form['tipo_movimentacao'])))
            print(form_evento)
            form_evento.save()
            db_session.close()
            flash("Movimentação de Produto Cadastrada!", "success")
            return redirect(url_for('movimentacaoProduto'))

    # Recupera a lista de funcionários
    lista_funcionarios = select(Funcionario).select_from(Funcionario)
    lista_funcionarios = db_session.execute(lista_funcionarios).scalars()
    listaFuncionarios = []
    for funcionario in lista_funcionarios:
        listaFuncionarios.append(funcionario.serialize_funcionario())

    # Recupera a lista de produtos
    lista_produtos = select(Produto).select_from(Produto)
    lista_produtos = db_session.execute(lista_produtos).scalars()
    listaProdutos = []
    for produto in lista_produtos:
        listaProdutos.append(produto.serialize_produto())

        # Renderiza o template com as listas de funcionários e produtos
    return render_template('movimentacao.html', var_funcionario=listaFuncionarios, var_produtos=listaProdutos)

if __name__ == '__main__':
    app.run(debug=True)
