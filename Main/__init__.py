from flask      import Flask
from util       import Base, engine

app             = Flask(__name__)
app.debug       = True
app.secret_key  = 'under_development'

import Main.views
from views import *

app.add_url_rule('/', 
                 view_func = Index.as_view('index'),
                 methods = ['GET', 'POST'])
app.add_url_rule('/item/',
                 defaults = {'item_id': None},
                 view_func = ItemView.as_view('item'),
                 methods = ['GET', 'POST'])
app.add_url_rule('/item/<int:item_id>',
                 view_func = ItemView.as_view('item'),
                 methods = ['GET', 'POST', 'PUT'])
app.add_url_rule('/item/edit/',
                 defaults = {'item_id': None},
                 view_func = ItemMod.as_view('item_mod'),
                 methods = ['GET', 'POST'])
app.add_url_rule('/item/edit/<int:item_id>',
                view_func = ItemMod.as_view('item_mod'),
                methods = ['GET', 'POST'])

from models import *
Base.metadata.create_all(engine)
