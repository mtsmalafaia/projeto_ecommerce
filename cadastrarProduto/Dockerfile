FROM python:3.8-slim
RUN pip install flask
RUN pip install flask-mysqldb
RUN mkdir templates
RUN mkdir static
COPY cadastrarProduto.py /cadastrarProduto2.py
COPY templates/*  /templates/
COPY static/*  /static/
RUN chmod -R a+rwx static
RUN chmod -R a+rwx templates
CMD ["python","cadastrarProduto2.py"]