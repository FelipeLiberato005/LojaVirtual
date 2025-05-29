from flask import blueprints, render_template, request, redirect, url_for, flash, session, current_app
from . import mysql, bcrypt
from functools import wraps
import MySQLdb.cursors
from werkzeug.utils import secure_filename
import os

main = blueprints.Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_admin'):
            flash('Acesso restrito a administradores.', 'danger')
            return redirect(url_for('main.perfil'))
        return f(*args, **kwargs)
    return decorated_function

def extensao_permitida(nome_arquivo):
    ext = nome_arquivo.rsplit('.', 1)[1].lower()
    return '.' in nome_arquivo and ext in current_app.config.get('ALLOWED_EXTENSIONS', {'jpg', 'jpeg', 'png', 'gif'})

@main.route('/')
def homepage():
    return render_template('home.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario and bcrypt.check_password_hash(usuario['senha'], senha):
            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']
            session['usuario_admin'] = usuario.get('is_admin', 0)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.perfil'))
        else:
            flash('Email ou senha incorretos!', 'error')
    return render_template('login.html')

@main.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = bcrypt.generate_password_hash(request.form['senha']).decode('utf-8')

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
        mysql.connection.commit()
        cursor.close()

        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('main.homepage'))
    return render_template('cadastro.html')

@main.route('/produtos')
def produtos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    cursor.close()
    return render_template('produtos.html', produtos=produtos)

@main.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM compras WHERE usuario_id = %s", (session['usuario_id'],))
    compras = cursor.fetchall()
    cursor.execute("SELECT * FROM endereco WHERE usuario_id = %s", (session['usuario_id'],))
    enderecos = cursor.fetchall()
    cursor.execute("SELECT * FROM cartoes WHERE usuario_id = %s", (session['usuario_id'],))
    cartoes = cursor.fetchall()
    cursor.close()

    return render_template('perfil.html', compras=compras, enderecos=enderecos, cartoes=cartoes)

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@main.route('/enderecos', methods=['GET', 'POST'])
def enderecos():
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        usuario = session['usuario_id']
        endereco = request.form['endereco']
        cidade = request.form['cidade']
        estado = request.form['estado']
        cep = request.form['cep']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO endereco (usuario_id, endereco, cidade, estado, cep) VALUES (%s, %s, %s, %s, %s)",
                       (usuario, endereco, cidade, estado, cep))
        mysql.connection.commit()
        cursor.close()
        flash("Endereço registrado com sucesso!", "success")
        return redirect(url_for('main.perfil'))

    return render_template('registrarinfo.html')

@main.route('/cartoes', methods=['GET', 'POST'])
def cartoes():
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        usuario = session['usuario_id']
        numero_cartao = request.form['numero_cartao']
        nome_titular = request.form['nome_titular']
        validade = request.form['validade']
        cvv = request.form['cvv']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO cartoes (usuario_id, numero_cartao, nome_titular, validade, cvv) VALUES (%s, %s, %s, %s, %s)",
                       (usuario, numero_cartao, nome_titular, validade, cvv))
        mysql.connection.commit()
        cursor.close()
        flash("Cartão registrado com sucesso!", "success")
        return redirect(url_for('main.perfil'))

    return render_template('cartaoinfo.html')

@main.route('/admin/produtos/novo', methods=['GET', 'POST'])
@admin_required
def novo_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        categoria = request.form['categoria']
        estoque = request.form['estoque']
        imagem = request.files.get('imagem')

        if not imagem or imagem.filename == '':
            flash('Nenhuma imagem foi enviada.', 'error')
            return redirect(url_for('main.novo_produto'))

        if not extensao_permitida(imagem.filename):
            flash('Formato de imagem inválido! Use .jpg, .jpeg, .png ou .gif', 'error')
            return redirect(url_for('main.novo_produto'))

        filename = secure_filename(imagem.filename)
        UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
        imagem.save(os.path.join(UPLOAD_FOLDER, filename))

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO produtos (nome_produto, descricao, preco, categoria, estoque, imagem_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, descricao, preco, categoria, estoque, filename))
        mysql.connection.commit()
        cursor.close()

        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('main.produtos'))

    return render_template('novo_produto.html')

@main.route('/admin/compras')
def admin_compras():
    if not session.get('usuario_admin'):
        flash('Acesso negado. Apenas administradores.', 'error')
        return redirect(url_for('main.login'))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT u.nome, u.email, c.id, c.produto_id, c.quantidade, c.data_compra
        FROM compras c
        JOIN usuarios u ON c.usuario_id = u.id
        ORDER BY c.data_compra DESC
    """)
    compras = cursor.fetchall()
    cursor.close()

    return render_template('admin_compras.html', compras=compras)

@main.route('/admin/painel')
@admin_required
def painel_admin():
    return render_template('admin.html')
