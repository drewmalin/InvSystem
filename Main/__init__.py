from flask      import Flask
from util       import Base, engine
from api        import *

app             = Flask(__name__)
app.debug       = True
app.secret_key  = 'under_development'

import Main.views
from views import *

#######     INDEX       #######
app.add_url_rule('/', 
                 view_func = Index.as_view('index'),
                 methods = ['GET', 'POST'])

######      ITEM        #######
app.add_url_rule('/item/',
                 defaults = {'item_id': None},
                 view_func = ItemView.as_view('item'),
                 methods = ['GET', 'POST'])
app.add_url_rule('/item/<int:item_id>',
                 view_func = ItemView.as_view('item'),
                 methods = ['GET', 'POST'])
app.add_url_rule('/item/edit/',
                 defaults = {'item_id': None},
                 view_func = ItemMod.as_view('item_mod'),
                 methods = ['GET', 'POST'])
app.add_url_rule('/item/edit/<int:item_id>',
                view_func = ItemMod.as_view('item_mod'),
                methods = ['GET', 'POST'])
app.add_url_rule('/item/history/<int:item_id>',
                view_func = ItemHistory.as_view('item_history'),
                methods = ['GET'])

######      VENDOR      #######
app.add_url_rule('/vendor/',
                 defaults = {'vendor_id':None},
                 view_func = VendorView.as_view('vendor'),
                 methods = ['GET', 'POST'])
app.add_url_rule('/vendor/<int:vendor_id>',
                 view_func = VendorView.as_view('vendor'),
                 methods = ['GET', 'POST'])
app.add_url_rule('/vendor/edit/',
                 defaults = {'vendor_id': None},
                 view_func = VendorMod.as_view('vendor_mod'),
                 methods = ['GET', 'POST'])
app.add_url_rule('/vendor/edit/<int:vendor_id>',
                 view_func = VendorMod.as_view('vendor_mod'),
                 methods = ['GET', 'POST'])

######      REPORT      #######
app.add_url_rule('/reports/',
                 view_func = ReportView.as_view('reports'),
                 methods = ['GET', 'POST'])

######      API         #######
app.add_url_rule('/api/vendors/',
    defaults={'vendor_id': None},
    view_func=VendorsAPI.as_view('vendors_api'),
    methods=['GET'])
app.add_url_rule('/api/vendors/<int:vendor_id>',
    view_func=VendorsAPI.as_view('vendors_api'),
    methods=['GET'])
app.add_url_rule('/api/quantity/',
    defaults={'item_id': None},
    view_func=QuantityAPI.as_view('quantity_api'),
    methods=['GET'])
app.add_url_rule('/api/quantity/<int:item_id>',
    view_func=QuantityAPI.as_view('quantity_api'),
    methods=['GET', 'POST'])
app.add_url_rule('/api/vendor/<int:item_id>',
    view_func=VendorAPI.as_view('vendor_api'),
    methods=['POST'])
app.add_url_rule('/api/item/<int:item_id>/vendors',
    view_func=ItemVendorsAPI.as_view('item_vendors_api'),
    methods=['GET'])

from models import *
Base.metadata.create_all(engine)
