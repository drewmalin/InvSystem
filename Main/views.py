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
        
        ## Temp ##
        vendor = Vendor('test_vendor!')
        session.add(vendor)
        #offer = Offer(100, 10000)
        #session.add(offer)
        session.commit()
        items = session.query(Item)
        ## #### ##

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

class ItemHistory(flask.views.MethodView):
    def get(self, item_id):
        item = session.query(Item).get(item_id)
        return flask.render_template('item_history.html', item = item)

class ItemMod(flask.views.MethodView):
    def get(self, item_id):
        if item_id != None:
            item = session.query(Item).get(item_id)
        else:
            item = None
        return flask.render_template('new_item.html', item = item)

    def post(self, item_id):
        if item_id == None:
            item = self.createItem()
            if item == None:
                return flask.render_template('new_item.html')
            else:
                return flask.render_template('item.html', item = item)
        else:
            item = self.editItem(item_id)
            if item == None:
                item = session.query(Item).get(item_id)
                return flask.render_template('new_item.html', item = item)
            else:
                return flask.render_template('item.html', item = item)

    def createItem(self):
        if self.validateSubmission != 0:
            return None

        item = Item()
        itemSnapshot = ItemSnapshot(flask.request.form['name'],
                                    flask.request.form['num'],
                                    flask.request.form['quantity'],
                                    1, 1)
        vendor = session.query(Vendor).get(1)
        itemSnapshot.primary_vendor = vendor
        item.snapshots.append(itemSnapshot)
        session.add(item)
        session.commit()
        return item
        
    def editItem(self, item_id):
        if self.validateSubmission() != 0:
            return None
        item = session.query(Item).get(item_id)
        itemSnapshot = ItemSnapshot(flask.request.form['name'],
                                    flask.request.form['num'],
                                    flask.request.form['quantity'],
                                    1, 1)
        item.snapshots.append(itemSnapshot)
        session.commit()
        return item

    def validateSubmission(self):
        error = 0
        if flask.request.form['name'] == "":
            flask.flash("Item name is required")
            error = 1
        if flask.request.form['num'] == "":
            flask.flash("Item ID number is required")
            error = 1
        if flask.request.form['quantity'] == "":
            flask.flash("Item quantity on hand is required")
            error = 1
        if flask.request.form['reorder_point'] == "":
            flask.flash("Reorder point is required")
            error = 1
        if flask.request.form['reorder_quantity'] == "":
            flask.flash("Reorder quantity is required")
            error = 1
        if flask.request.form['primary_vendor'] == "":
            flask.flash("Primary vendor is required")
            error = 1
        return error

class VendorView(flask.views.MethodView):
    def get(self, vendor_id):
        if vendor_id != None:
            vendor = session.query(Vendor).get(vendor_id)
            return flask.render_template('vendor.html', vendor = vendor)
        else:
            return flask.redirect(flask.url_for('index'))

class VendorMod(flask.views.MethodView):
    def get(self, vendor_id):
        if vendor_id != None:
            vendor = session.query(Vendor).get(vendor_id)
        else:
            vendor = None
        return flask.render_template('new_vendor.html', vendor = vendor)

    def post(self, vendor_id):
        if vendor_id == None:
            vendor = self.createVendor()
            if vendor == None:
                return flask.render_template('new_vendor.html')
            else:
                return flask.render_template('vendor.html', vendor = vendor)
        else:
            vendor = self.editVendor(vendor_id)
            if vendor == None:
                vendor = session.query(Vendor).get(vendor_id)
                return flaks.render_template('new_vendor.html', vendor = vendor)
            else:
                return flask.render_template('vendor.html', vendor = vendor)

    def createVendor(self):
        if self.validateSubmission() != 0:
            return None
        vendor = Vendor(flask.request.form['name'])
        session.add(vendor)
        session.commit()
        return vendor

    def editVendor(self, vendor_id):
        if self.validateSubmission() != 0:
            return None
        vendor = session.query(Vendor).get(vendor_id)
        vendor.name = flask.request.form['name']
        session.commit()
        return vendor

    def validateSubmission(self):
        error = 0
        if flask.request.form['name'] == "":
            flask.flash("Vendor name is required")
            error = 1
        return error
