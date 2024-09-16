import os
from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL


mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Impacta2024'
app.config['MYSQL_DB'] = 'ecommerce'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('formularioProduto.html')



@app.route('/cadastrar', methods=['GET','POST'])
def cadastro():
    try:
        nome = request.form['inputNome'].title().strip()
        #title pega o comeco das palavras e transforma em maiusculo. Strip tira os espacos
        categoria = request.form['inputCategoria']
        peso = request.form['inputPeso']
        preco = request.form['inputPreco']
        descricao = request.form['inputDescricao'].lower()
        #lower deixa tudo minusculo

        if not peso :
            peso = 0
        if not descricao:
            descricao = "Não Há"
    
        cur = mysql.connection.cursor()

        cur.execute("SELECT nomeDoProduto FROM tblProduto WHERE nomeDoProduto = %s", (nome,))

        resultado = cur.fetchone()

        if resultado:
            msg = "Produto ja cadastrados na base de dados"
            return render_template('formulario_produto.html', mensagem = msg)
        else:
                       
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tblProduto (nomeDoProduto, categoria, pesoGramas, preco, descricao) VALUES (%s, %s, %s, %s, %s)', ( nome,categoria,peso,preco,descricao))
            conn.commit()
            msg = "Produtos cadastrados com sucesso"
            return render_template('formularioProduto.html', mensagem = msg)

    except Exception as e:
        return json.dumps({'error':str(e)})
    



@app.route('/list',methods=['GET'])
def list():
    try:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute ('SELECT * FROM tblProduto')
            data = cursor.fetchall()
            return render_template('listar.html', datas=data)

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/produto/<id>',methods=['GET'])    
def editProd(id):
    try:
            id = int(id)
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tblProduto WHERE produtoId = %s', (id,))
            data = cursor.fetchall()
            return render_template('editarProduto.html', datas=data)
    
    except Exception as e:
        return json.dumps({'error':str(e)})
    
@app.route('/produto/<id>',methods=['POST','GET'])
def editarProduto(id):
    
    try:
        idProd = int(request.form['idProd'])
        nome = request.form['inputNome']
        categoria = request.form['inputCategoria']
        peso = request.form['inputPeso']
        preco = request.form['inputPreco']
        descricao = request.form['inputDescricao']

        if not peso :
            peso = 0

        if nome and categoria and preco:
            
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('UPDATE tblProduto SET nomeDoProduto = %s, categoria = %s, pesoGramas = %s, preco = %s, descricao = %s WHERE produtoId = %s ', ( nome,categoria,peso,preco,descricao,idProd))
            conn.commit()
            msg = "Edição realizada com sucesso"
    
            cursor.execute ('SELECT * FROM tblProduto WHERE produtoId = %s ', (idProd,))
            data = cursor.fetchall()  
                  
            return render_template('listar.html', mensagem = msg, datas=data)
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/produto/delete/<int:id>')
def delete(id):
    try:
        id = int(id)
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tblProduto WHERE produtoId = %s', (id,))
        conn.commit()
        msg = "Excluido com sucesso"
        
        cursor.execute ('SELECT * FROM tblProduto')
        data = cursor.fetchall()

        return render_template('listar.html', mensagem = msg, datas=data)
    
    except Exception as e:
        return json.dumps({'error': str(e)})   

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)