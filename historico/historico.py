import os
from flask import Flask, render_template, json
from flask_mysqldb import MySQL


mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Impacta2024'
app.config['MYSQL_DB'] = 'restaurante'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/list',methods=['GET'])
def list():
    try:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute ('SELECT * FROM tblHistorico WHERE tipo = "compra" ORDER BY  data DESC')
            data = cursor.fetchall()
            print(data)
            cursor.execute('SELECT * FROM tblHistorico WHERE tipo = "venda" ORDER BY data DESC')
            data2 = cursor.fetchall()
            print(data2)
            return render_template('listarHistorico.html', datasCompra=data, datasVenda=data2)

    except Exception as e:
        return json.dumps({'error':str(e)})




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5004))
    app.run(host='0.0.0.0', port=port, debug=True)