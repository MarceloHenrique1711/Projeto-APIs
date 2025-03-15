from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def getUsers():
    dados = {'mensagem' : 'Bem-vindo à minha API Flask!'}
    return jsonify(dados)

@app.route('/produtos', methods=['GET'])
def getProdutos():
    dados = {'mensagem' : 'Voce esta na pagina de produtos'}
    return jsonify(dados)

@app.route('/estoque', methods=['GET'])
def getEstoque():
    dados = {'mensagem' : 'Voce esta na pagina de estoque'}
    return jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True)