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
            return flask.render_template('new_item.html')
    def post(self, item_id):
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
        return flask.redirect(flask.url_for('index'))
