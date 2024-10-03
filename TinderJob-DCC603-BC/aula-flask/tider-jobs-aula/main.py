from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Inicializando o Flask-Bootstrap 
Bootstrap5(app)

# Função para conectar ao banco de dados
def connect_db():
    conn = sqlite3.connect('app.db')  # Conectando ao banco 'app.db'
    conn.row_factory = sqlite3.Row
    return conn

# Função para criar tabelas se não existirem
def create_tables():
    with connect_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS devs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        cel TEXT NOT NULL,
                        habilidades TEXT NOT NULL,
                        senha TEXT NOT NULL
                        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS empresas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        cel TEXT NOT NULL,
                        area_atuacao TEXT NOT NULL,
                        cnpj TEXT NOT NULL,
                        patrimonio TEXT NOT NULL,
                        senha TEXT NOT NULL
                        )''')

# Inicializando tabelas
create_tables()

# Formulário para Desenvolvedor
class DevForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    cel = StringField('Celular', validators=[DataRequired()])
    habilidades = TextAreaField('Habilidades', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

# Formulário para Empresa
class EmpForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    cel = StringField('Celular', validators=[DataRequired()])
    area_atuacao = TextAreaField('Área de Atuação', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired()])
    patrimonio = StringField('Patrimônio', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

@app.route("/")
def home():
    return render_template("index.html")

# Rota para login dev
@app.route("/dev/login", methods=["GET", "POST"])
def dev_login():
    if request.method == "POST":
        email = request.form['email']
        senha = request.form['senha']
        with connect_db() as conn:
            dev = conn.execute('SELECT * FROM devs WHERE email = ? AND senha = ?', (email, senha)).fetchone()
        if dev:
            return redirect(url_for('dev_profile', dev_id=dev['id']))
        else:
            flash("Credenciais inválidas", "danger")
            return render_template("dev_login.html")
    return render_template("dev_login.html")

@app.route("/dev/register", methods=["GET", "POST"])
def dev_register():
    form = DevForm()
    if form.validate_on_submit():
        with connect_db() as conn:
            conn.execute('INSERT INTO devs (name, email, cel, habilidades, senha) VALUES (?, ?, ?, ?, ?)', 
                         (form.name.data, form.email.data, form.cel.data, form.habilidades.data, form.senha.data))
        return redirect(url_for('dev_login'))
    return render_template("dev_register.html", form=form)

# Rota para exibir perfil de desenvolvedor
@app.route("/dev/profile/<int:dev_id>")
def dev_profile(dev_id):
    with connect_db() as conn:
        dev = conn.execute('SELECT * FROM devs WHERE id = ?', (dev_id,)).fetchone()
    return render_template("dev_profile.html", dev=dev)

# Rota para login empresa
@app.route("/emp/login", methods=["GET", "POST"])
def emp_login():
    if request.method == "POST":
        email = request.form['email']
        senha = request.form['senha']
        with connect_db() as conn:
            dev = conn.execute('SELECT * FROM devs WHERE email = ? AND senha = ?', (email, senha)).fetchone()
        if dev:
            return redirect(url_for('emp_profile', dev_id=dev['id']))
        else:
            flash("Credenciais inválidas", "danger")
            return render_template("emp_login.html")
    return render_template("emp_login.html")

# Rota para exibir perfil de empresa
@app.route("/empresa/profile/<int:empresa_id>")
def empresa_profile(empresa_id):
    with connect_db() as conn:
        empresa = conn.execute('SELECT * FROM empresas WHERE id = ?', (empresa_id,)).fetchone()
    return render_template("empresa_profile.html", empresa=empresa)

@app.route("/emp/register", methods=["GET", "POST"])
def emp_register():
    form = EmpForm()
    if form.validate_on_submit():
        with connect_db() as conn:
            conn.execute('INSERT INTO empresas (name, email, cel, area_atuacao, cnpj, patrimonio, senha) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                         (form.name.data, form.email.data, form.cel.data, form.area_atuacao.data, form.cnpj.data, form.patrimonio.data, form.senha.data))
        return redirect(url_for('home'))
    return render_template("emp_register.html", form=form)

if __name__ == '__main__':
    app.run(debug=True, port=6001)
