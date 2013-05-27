from util           import session
import flask, flask.views
from models         import *
from Main           import app

class Index(flask.views.MethodView):
    def get(self):
        # Temporary data creation
        # item = Item('test 1', '1', 10, 1, 1)
        # session.add(item)
        # session.commit()
        items = session.query(Item)
        return flask.render_template('home.html', items = items)
    def post(self):
        if flask.request.form['search'] == "":
            flask.flash("Search query is required!")
            return flask.redirect(flask.url_for('index'))
        else:
            items = session.query(Item).filter(Item.name == flask.request.form['search'])
            return flask.render_template('home.html', items = items)
        
class ItemView(flask.views.MethodView):
    def get(self, item_id):
        if item_id != None:
            item = session.query(Item).get(item_id)
            return flask.render_template('item.html', item = item)
        else:
            return flask.redirect(flask.url_for('index'))

class ItemMod(flask.views.MethodView):
    def get(self, item_id):
        if item_id != None:
            item = session.query(Item).get(item_id)
        else:
            item = None
        return flask.render_template('new_item.html', item = item)

    def post(self, item_id):
        if item_id == None:
            self.myPost()
            return flask.redirect(flask.url_for('index'))
        else:
            self.myPut(item_id)
            item = session.query(Item).get(item_id)
            return flask.render_template('item.html', item = item)

    def myPost(self):
        error = 0
        if flask.request.form['name'] == "":
            flask.flash("Name is required!")
            error = 1
        if flask.request.form['num'] == "":
            flask.flash("Num is required!")
            error = 1
        if flask.request.form['quantity'] == "":
            flask.flash("Quantity is required!")
            error = 1
        if error > 0:
            return flask.redirect(flask.url_for('item'))
        
        item = Item(flask.request.form['name'],
                    flask.request.form['num'],
                    flask.request.form['quantity'],
                    1, 1)
        session.add(item)
        session.commit()
        
    def myPut(self, item_id):
        error = 0
        if flask.request.form['name'] == "":
            flask.flash("Name is required!")
            error = 1
        if flask.request.form['num'] == "":
            flask.flash("Num is required!")
            error = 1
        if flask.request.form['quantity'] == "":
            flask.flash("Quantity is required!")
            error = 1
        if error > 0:
            return flask.redirect(flask.url_for('item'))
        #session.query(Item).get(item_id).update({'name':flask.request.form['name'], 'num':flask.request.form['num'], 'quantity_on_hand':flask.request.form['quantity']})
        item = session.query(Item).get(item_id)
        item.name = flask.request.form['name']
        item.num = flask.request.form['num']
        item.quantity_on_hand = flask.request.form['quantity']
        session.add(item)
        session.commit()
