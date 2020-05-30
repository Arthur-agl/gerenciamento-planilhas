from flask_wtf import FlaskForm
from wtforms import DateField, StringField, IntegerField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired

class QuoteForm(FlaskForm):
    who  = SelectField('Responsável:',choices=[('celio','Responsável: Célio'),('josafa',' Responsável: Josafá'),('mazinho','Responsável: Mazinho')], validators=[DataRequired()] )
    date = DateField("data",validators=[DataRequired()])
    cost = IntegerField("Custo",validators=[DataRequired()])
    pmargin = IntegerField("Margem de lucro(em %)",validators=[DataRequired()])
    sell_price = IntegerField("Preço de venda",validators=[DataRequired()])

    s_list = HiddenField("lista",validators=[DataRequired("É necessário incluri pelo menos 1 produto/serviço")])
    submit = SubmitField("Adicionar")

class SalesForm(FlaskForm):
    name = StringField("Produto",validators=[DataRequired()])
    cost = IntegerField("Preço de compra",validators=[DataRequired()])
    sell_price= IntegerField("Preço de venda",validators=[DataRequired()])

    submit = SubmitField("Adicionar")