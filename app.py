from flask import (Flask, request,render_template, redirect, url_for, flash) 

app = Flask(__name__) 
app.secret_key = 'segredo'

@app.route("/", methods=( 'GET',)) 
def index(): 
    nome = request.args.get('nome') 
    return render_template('index.html', nome=nome)

@app.route("/galeria", methods=( 'GET', )) 
def galeria():
    return "<h1>Galeria</h1>"

@app.route("/contato", methods=( 'GET', )) 
def contato():
    return "<h1>contato</h1>"

@app.route("/sobre", methods=( 'GET', )) 
def sobre():
    return "<h1>sobre</h1>"

@app.route("/area/<float:largura>/<float:altura>", methods=( 'GET', ))
def area(largura: float, altura: float):
    return f"""<h1> A área
    informada >L={largura} * A={altura}
    => Area={largura*altura}</h1>"""

@app.route("/parimpar/<float:numero>", methods=('GET',))
def par_ou_impar(numero):
  if numero % 2 == 0:
    return f"O número {numero} é par."
  else:
    return f"O número {numero} é ímpar."
  
@app.route("/sobrenome/<string:nome>/<string:sobrenome>", methods=('GET',))
def nomesobrenome(nome: str, sobrenome: str):
  return f"""<h1> sobrenome </h1>
  <p>{sobrenome},{nome}</p>"""

@app.route("/potencia/<float:um>/<float:dois>", methods=( 'GET', ))
def potencia(um: float, dois: float):
    return f"""<h1>{um}^{dois}
     ={um**dois}</h1>"""

@app.route("/tabuada")
@app.route("/tabuada/<numero>", methods=("GET" , ))
def tabuada(numero = None): 

    if 'numero' in request.args: 
        numero = int(request.args.get('numero')) 

    return render_template('tabuada.html', numero=numero)

@app.route('/calculojuros', methods=['GET', 'POST'])
def calculo_juros():
    if request.method == 'POST':
        try:
            investimento_inicial = float(request.form['investimento_inicial'])
            juros_ano = float(request.form['juros_ano'])
            tempo_meses = int(request.form['tempo_meses'])
            aporte_mensal = float(request.form['aporte_mensal'])

          
            juros_mensal = juros_ano / 12 / 100
            total = investimento_inicial

            for _ in range(tempo_meses):
                total += aporte_mensal
                total *= (1 + juros_mensal)

            return render_template('calculo_juros.html', total=total)
        except ValueError:
            return render_template('calculo_juros.html', error="Por favor, insira valores válidos.")

    return render_template('calculo_juros.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        
        if email == 'aluno@senai.br' and senha == 'senai':
            flash('Usuário Logado com Sucesso!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Usuário ou senha incorretos, tente novamente.', 'error')

    return render_template('login.html')


@app.route('/imc', methods=['GET', 'POST'])
def imc():
    imc = None
    categoria = None

    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        imc = peso / (altura ** 2)

        if imc < 18.5:
            categoria = 'Magreza'
        elif imc < 24.9:
            categoria = 'Normal'
        elif imc < 29.9:
            categoria = 'Sobrepeso - Grau 1'
        elif imc <39.9:
            categoria = 'Obesidade - Grau 2'
        else:
            categoria = 'Obesidade Grave - Grau 3'

    return render_template('imc.html', imc=imc, categoria=categoria)




medicoes_mensais = []

@app.route('/consumoenergia', methods=['GET', 'POST'])
def calcular_consumo():
    global medicoes_mensais 

    if request.method == 'POST':
        try:
            nova_medicao = float(request.form['nova_medicao'])
            medicoes_mensais.append(nova_medicao)

           
            consumo = [medicoes_mensais[i] - medicoes_mensais[i - 1] for i in range(1, len(medicoes_mensais))]
            valor_kwh = 0.89  
            valores = [c * valor_kwh for c in consumo]

            return render_template('consumo.html', medicoes=medicoes_mensais, consumo=consumo, valores=valores)

        except ValueError:
            flash("Por favor, insira um valor válido.")
            return redirect(url_for('calcular_consumo'))

    return render_template('consumo.html', medicoes=medicoes_mensais)