import os
from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Impacta2024'
app.config['MYSQL_DB'] = 'restaurante'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    conn = mysql.connection 
    cursor = conn.cursor() 
    cursor.execute("SELECT nomeCategoria FROM tblCategoria")
    categorias=cursor.fetchall()
    return render_template('formularioItemMenu.html',categorias=categorias)




@app.route('/categoria')
def categoria():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute ('SELECT * FROM tblCategoria')
    dados = cursor.fetchall()
    
    return render_template('categoria.html', dados=dados)





# @app.route('/cadastrar_categoria',methods=['POST','GET'])
# def cadastrar_categoria():
#     try:
#         nome_categoria = request.form['inputNomeCategoria'].upper()

#         cur = mysql.connection.cursor()
#         cur.execute("SELECT NomeCategoria FROM tbl_categoria WHERE NomeCategoria = %s",(nome_categoria,))
#         resultado = cur.fetchone()

#         conn = mysql.connection
#         cursor = conn.cursor()
#         cursor.execute ('select * from tbl_categoria')
#         dados = cursor.fetchall()

#         if resultado:
#             msg = "Categoria ja cadastrada na base de dados"
#             return render_template('categoria.html',mensagem = msg, dados=dados)
#         else:
#             conn = mysql.connection
#             cursor = conn.cursor()
#             cursor.execute('insert into tbl_categoria(NomeCategoria) VALUES (%s)', ( nome_categoria,))
#             conn.commit()
#             msg = "Categoria cadastrada com sucesso"
#             return render_template('categoria.html',mensagem = msg, dados=dados)
#     except Exception as e:
#         return json.dumps({'error': str(e)})





@app.route('/cadastrarItem', methods=['POST', 'GET'])
def cadastro():
    try:
        nome = request.form['inputNome'].title().strip()
        #title pega o comeco das palavras. Strip tira os espacoes
        categoria = request.form['inputCategoria']
        descricao = request.form['inputDescricao']
        preco = request.form['inputPreco']


        cur = mysql.connection.cursor()
        cur.execute("SELECT nomeDoItem FROM tblMenu WHERE nomeDoItem = %s",(nome,))

        resultado = cur.fetchone()
        if resultado:
            msg = "Produto ja cadastrados na base de dados"
            return render_template('formularioItemMenu.html',mensagem = msg)
        else:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tblMenu (nomeDoItem, categoria, descricao, preco) VALUES(%s, %s, %s, %s)',(nome, categoria,  descricao, preco))
            conn.commit()
            msg = "Item cadastrado com sucesso"
            return render_template('formularioItemMenu.html', mensagem = msg)
    except Exception as e:
        return json.dumps({'error': str(e)})





@app.route('/list',methods=['GET'])
def list():
    try:
            conn = mysql.connection
            cursor = conn.cursor()
            
            cursor.execute ('SELECT * FROM tblMenu WHERE Categoria = "Bebida"')
            dataBebida = cursor.fetchall()

            cursor.execute ('select * from tblMenu WHERE Categoria = "Drink"')
            dataDrink = cursor.fetchall()

            cursor.execute ('select * from tblMenu WHERE Categoria = "Pizza"')
            dataPizza = cursor.fetchall()
            
            cursor.execute ('select * from tblMenu WHERE Categoria = "Prato"')
            dataPrato = cursor.fetchall()

            cursor.execute ('select * from tblMenu WHERE Categoria = "Sobremesa"')
            dataSobremesa = cursor.fetchall()
            
            return render_template('listarMenu.html', datas1=dataBebida, datas2=dataDrink,datas3 = dataPizza, datas4 = dataPrato,datas5 = dataSobremesa)

    except Exception as e:
        return json.dumps({'error':str(e)})
@app.route('/produto/<id>',methods=['GET'])    
def editProd(id):

    try:

            id = int(id)
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tblMenu WHERE itemId = %s', (id,))
            print("antes do try edit prod")
            data = cursor.fetchall()
            return render_template('editarItemMenu.html', datas=data)
    
    except Exception as e:
        return json.dumps({'error':str(e)})
    
@app.route('/produto/<id>',methods=['POST','GET'])
def editarProduto(id):
    
    try:
        idProd = int(request.form['idProd'])
        nome = request.form['inputNome']
        categoria = request.form['inputCategoria']
        descricao = request.form['inputDescricao']
        preco = request.form['inputPreco']



        if request.method == 'POST':
            if nome and categoria and preco:
                conn = mysql.connection
                cursor = conn.cursor()
                print("Oi")
                cursor.execute('UPDATE tblMenu SET nomeDoItem = %s, categoria = %s, descricao = %s, preco = %s WHERE ItemId = %s ', ( nome,categoria,descricao, preco, idProd))
                conn.commit()
                msg = "Edição realizada com sucesso"
            
            cursor.execute ('SELECT * FROM tblMenu WHERE itemId = %s', (idProd,))
            data = cursor.fetchall()
            
            return render_template('listarUnicoMenu.html', mensagem = msg, datas=data)
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/produto/delete/<int:id>')
def deleteProduto(id):
    try:
        id = int(id)
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tblMenu WHERE itemId = %s', (id,))
        conn.commit()
        msg = "Excluido com sucesso"
        
        cursor.execute ('SELECT * FROM tblMenu WHERE itemId = %s ', (id,))
        data = cursor.fetchall()

        return render_template('listarUnicoMenu.html', mensagem = msg, datas=data)
    
    except Exception as e:
        return json.dumps({'error': str(e)})   


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)