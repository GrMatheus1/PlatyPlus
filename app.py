from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from models import db_session, Funcionario, Produto
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
    inicial_funcionario = select(Funcionario).select_from(Funcionario)
    inicial_funcionario = db_session.execute(inicial_funcionario).scalars()
    inicialFuncionario = []
    for funcionario in inicial_funcionario:
        inicialFuncionario.append(funcionario.serialize_funcionario())
    print(inicialFuncionario)
    return render_template('inicial.html', var_funcionario=inicialFuncionario)


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
            return redirect(url_for('lista'))
    return render_template('produto.html')


@app.route('/lista')
def lista():
    lista_produtos = select(Produto).select_from(Produto)
    lista_produtos = db_session.execute(lista_produtos).scalars()
    listaProdutos = []
    for produto in lista_produtos:
        listaProdutos.append(produto.serialize_produto())
    print(listaProdutos)
    return render_template('lista.html', var_produtos=listaProdutos)


@app.route('/estoque')
def listar_estoque():
    estoque_produtos = select(Produto).select_from(Produto)
    estoque_produtos = db_session.execute(estoque_produtos).scalars()
    estoqueProduto = []
    for produto in estoque_produtos:
        estoqueProduto.append(produto.serialize_produto())
    print(estoqueProduto)
    return render_template('estoque.html', var_produtos=estoqueProduto)


@app.route('/detalhes', methods=['PUT'])
def listar_detalhe():
    detalhe_produtos = select(Produto).select_from(Produto)
    detalhe_produtos = db_session.execute(detalhe_produtos).scalars()
    detalheProduto = []
    for produto in detalhe_produtos:
        detalheProduto.append(produto.serialize_produto())
    print(detalheProduto)
    return render_template('detalhe.html', var_produtos=detalheProduto)


if __name__ == '__main__':
    app.run(debug=True)
