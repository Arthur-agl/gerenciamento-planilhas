import os, datetime, json

from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

from forms import QuoteForm, SalesForm

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = '2017023659'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')

#ESTRUTURA BD
db = SQLAlchemy(app)

class Service (db.Model): # Serviço individual
    __tablename__ = "service"
    
    id      = db.Column(db.Integer,     primary_key=True)
    name    = db.Column(db.String(300), nullable=False) #descrição do serviço
    cost    = db.Column(db.Integer,     nullable=False) #custo de compra/execução
    
    quote_id = db.Column(db.Integer, db.ForeignKey('quote.id')) #identificador do orçamento que gerou esse item

class Quote (db.Model): # Orçamento
    __tabelname__ = "quote"

    id    = db.Column(db.Integer,      primary_key=True)
    who   = db.Column(db.String(100),  nullable=False) #Responsável pelo orçamento
    date  = db.Column(db.Date,         nullable=False) #data de inserção no sistema
    cost  = db.Column(db.Integer,      nullable=False) #custo total
    pmargin = db.Column(db.Integer,    nullable=False) #margem de lucro desejada
    sell_price = db.Column(db.Integer, nullable=False) #preco de venda

    service_list = db.relationship("Service")

class Product (db.Model): #Produtos comprados
    __tablename__ = "product"
    
    id         = db.Column(db.Integer,     primary_key=True)
    name       = db.Column(db.String(300), nullable=False) #nome do produto
    cost       = db.Column(db.Integer,     nullable=False) #preço de compra
    sell_price = db.Column(db.Integer,     nullable=False) #preço de venda

class Sale (db.Model):
    __tablename__ = "sale"
    id         = db.Column(db.Integer,     primary_key=True)
    name       = db.Column(db.String(300), nullable=False) #nome do produto
    cost       = db.Column(db.Integer,     nullable=False) #preço de compra
    sell_price = db.Column(db.Integer,     nullable=False) #preço de venda

#ESTRUTURA DAS PAGINAS


@app.route('/',methods=['GET','POST'])
def home():
    page_quotes = request.args.get('page_quotes',1,type=int)
    page_sales = request.args.get('page_quotes',1,type=int)

    quote_list = Quote.query.paginate(page_quotes, 10, False)
    sales_list = Sale.query.paginate(page_sales, 10, False)
    sale = SalesForm()

    if sale.validate_on_submit():
        sale_tmp = Sale(name=sale.name.data, cost=sale.cost.data, sell_price=sale.sell_price.data)
        db.session.add(sale_tmp)
        db.session.commit()
        flash("Adicionado com sucesso!","success")

        return redirect(url_for('home'))

    return render_template('home.html', title="Dashboard",list=quote_list, form=sale, list2=sales_list)

@app.route('/new_quote',methods=['GET','POST'])

def new_quote():
    quote_form = QuoteForm()

    if quote_form.validate_on_submit():

        quote_tmp = Quote(
            who        = quote_form.who.data,
            date       = quote_form.date.data,
            cost       = quote_form.cost.data,
            pmargin    = quote_form.pmargin.data,
            sell_price = quote_form.sell_price.data
        )
        tmp_slist = json.loads(quote_form.s_list.data)
        for service in tmp_slist:
            quote_tmp.service_list.append(Service(name=service['name'], cost=service['price']))

        db.session.add(quote_tmp)
        db.session.commit()

        flash("Orçamento inserido.","success")
        return redirect(url_for("home"))

    return render_template('new_quote.html', title="Novo orçamento", form=quote_form, today=datetime.datetime.now().date())

if __name__ == "__main__":
    app.run(debug=True)