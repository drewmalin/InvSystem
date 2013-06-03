from util           import session
import flask, flask.views
from models         import *
from Main           import app

class Index(flask.views.MethodView):
    def get(self):
        items = session.query(Item)
        return flask.render_template('home.html', items = items)
    def post(self):
        search_name     = flask.request.form['search_name'].strip()
        search_cat      = flask.request.form['search_catalog_num'].strip()
        search_vendor   = flask.request.form['search_vendor'].strip()
        search_q_from   = flask.request.form['search_quantity_from'].strip()
        search_q_to     = flask.request.form['search_quantity_to'].strip()
        
        items = session.query(Item)
        if search_name:
            items = [x for x in items if search_name in x.snapshots[0].name]
        if search_cat:
            items = [x for x in items if search_cat in x.snapshots[0].num]
        if search_vendor:
            items = [x for x in items if int(search_vendor) == x.snapshots[0].primary_vendor.id]
        if search_q_from:
            items = [x for x in items if int(search_q_from) <= x.snapshots[0].quantity_on_hand]
        if search_q_to:
            items = [x for x in items if int(search_q_to) >= x.snapshots[0].quantity_on_hand]

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
        if self.validateSubmission() != 0:
            return None

        item = Item()
        itemSnapshot = ItemSnapshot(flask.request.form['name'],
                                    flask.request.form['num'],
                                    flask.request.form['quantity'],
                                    flask.request.form['reorder_quantity'],
                                    flask.request.form['reorder_point'])

        primary_vendor = session.query(Vendor).get(flask.request.form['primary_vendor'])
        itemSnapshot.primary_vendor_p = flask.request.form['primary_vendor_p']
        itemSnapshot.primary_vendor = primary_vendor

        if (flask.request.form['secondary_vendor'] != ""):
            secondary_vendor = session.query(Vendor).get(flask.request.form['secondary_vendor'])
            itemSnapshot.secondary_vendor = secondary_vendor
        
        if (flask.request.form['secondary_vendor_p'] != ""):
            itemSnapshot.secondary_vendor_p = flask.request.form['secondary_vendor_p']

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
                                    flask.request.form['reorder_quantity'],
                                    flask.request.form['reorder_point'])
        
        primary_vendor = session.query(Vendor).get(flask.request.form['primary_vendor'])
        itemSnapshot.primary_vendor_p = flask.request.form['primary_vendor_p']
        itemSnapshot.primary_vendor = primary_vendor

        if (flask.request.form['secondary_vendor'] != ""):
            secondary_vendor = session.query(Vendor).get(flask.request.form['secondary_vendor'])
            itemSnapshot.secondary_vendor = secondary_vendor
        
        if (flask.request.form['secondary_vendor_p'] != ""):
            itemSnapshot.secondary_vendor_p = flask.request.form['secondary_vendor_p']

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
        if flask.request.form['primary_vendor_p'] == "":
            flask.flash("Primary vendor price is required")
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

class ReportView(flask.views.MethodView):
    def get(self):
        return flask.render_template('reports.html')
        
    def post(self):
        pass
