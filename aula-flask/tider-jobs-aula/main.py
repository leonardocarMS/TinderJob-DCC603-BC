from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, widgets, TextAreaField
from wtforms.validators import DataRequired, URL
import csv
from markupsafe import Markup

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# Formulário para Desenvolvedor
class DevForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    cel = StringField('Celular', validators=[DataRequired()])
    habilidades = TextAreaField('Habilidades', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

# Formulário para Empresa (similar ao de Desenvolvedor)
class EmpForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    cel = StringField('Celular', validators=[DataRequired()])
    area_atuacao = TextAreaField('Área de Atuação', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')
  

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dev/login")
def dev_login():
    return render_template("dev_login.html")

@app.route("/dev/register", methods=["GET", "POST"])
def dev_register():
    form = DevForm()
    if form.validate_on_submit():
        with open("devs-data.csv", mode="a", encoding="utf-8") as csv_file:
            csv_file.write(f"{form.name.data}, {form.email.data}, {form.cel.data}, {form.habilidades.data}\n")
        return redirect(url_for('home'))
    return render_template("dev_register.html", form=form)

@app.route("/emp/login")
def emp_login():
    return render_template("emp_login.html")

@app.route("/emp/register", methods=["GET", "POST"])
def emp_register():
    form = EmpForm()
    if form.validate_on_submit():
        with open("emps-data.csv", mode="a", encoding="utf-8") as csv_file:
            csv_file.write(f"{form.name.data}, {form.email.data}, {form.cel.data}, {form.area_atuacao.data}\n")
        return redirect(url_for('home'))
    return render_template("emp_register.html", form=form)


if __name__ == '__main__':
    app.run(debug=True, port=6001)