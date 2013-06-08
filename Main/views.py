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
            return flask.render_template('item.html', item=item)
        else:
            return flask.redirect(flask.url_for('index'))

class ItemHistory(flask.views.MethodView):
    def get(self, item_id):
        item = session.query(Item).get(item_id)
        return flask.render_template('item_history.html', item=item)

class ItemMod(flask.views.MethodView):
    def get(self, item_id):
        if item_id != None:
            item = session.query(Item).get(item_id)
        else:
            item = None
        return flask.render_template('new_item.html', item=item)

    def post(self, item_id):
        if item_id == None:
            item = self.createItem()
            if item == None:
                return flask.redirect(flask.url_for('item_mod'))
            else:
                return flask.redirect(flask.url_for('item', item_id=item_id))
        else:
            item = self.editItem(item_id)
            if item == None:
                item = session.query(Item).get(item_id)
                return flask.redirect(flask.url_for('item_mod', item_id=item.id))
            else:
                return flask.redirect(flask.url_for('item', item_id=item.id))

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
            return flask.render_template('vendor.html', vendor=vendor)
        else:
            return flask.redirect(flask.url_for('index'))

class VendorMod(flask.views.MethodView):
    def get(self, vendor_id):
        if vendor_id != None:
            vendor = session.query(Vendor).get(vendor_id)
        else:
            vendor = None
        return flask.render_template('new_vendor.html', vendor=vendor)

    def post(self, vendor_id):
        if vendor_id == None:
            vendor = self.createVendor()
            if vendor == None:
                return flask.redirect(flask.url_for('vendor_mod'))
            else:
                return flask.redirect(flask.url_for('vendor', vendor_id=vendor.id))
        else:
            vendor = self.editVendor(vendor_id)
            if vendor == None:
                vendor = session.query(Vendor).get(vendor_id)
                return flask.redirect(flask.url_for('vendor_mod', vendor_id=vendor.id))
            else:
                return flask.redirect(flask.url_for('vendor', vendor_id=vendor.id))

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

class LotView(flask.views.MethodView):
    def get(self, lot_id):
        if lot_id != None:
            lot = session.query(Lot).get(lot_id)
            return flask.render_template('lot.html', lot=lot)
        else:
            return flask.redirect(flask.url_for('index'))

    def post(self, lot_id):
        pass

class LotMod(flask.views.MethodView):
    def get(self, lot_id):
        if lot_id != None:
            lot = session.query(Lot).get(lot_id)
        else:
            lot = None
        return flask.render_template('new_lot.html', lot=lot)

    def post(self, lot_id):
        if lot_id == None:
            lot = self.createLot()
            if lot == None:
                return flask.redirect(flask.url_for('lot_mod'))
            else:
                return flask.redirect(flask.url_for('lot', lot_id=lot.id))
        else:
            lot = self.editLot(lot_id)
            if lot == None:
                lot = session.query(Lot).get(lot_id)
                return flask.redirect(flask.url_for('lot_mod', lot_id=lot.id))
            else:
                return flask.redirect(flask.url_for('lot', lot_id=lot.id))

    def createLot(self):
        if self.validateSubmission() != 0:
            return None
        lot = Lot(flask.request.form['name'])
        session.add(lot)
        session.commit()
        return lot

    def editLot(self, lot_id):
        if self.validateSubmission() != 0:
            return None
        lot = session.query(Lot).get(lot_id)
        lot.name = flask.request.form['name']
        session.commit()
        return lot

    def validateSubmission(self):
        error = 0
        if flask.request.form['name'] == "":
            flask.flash("Lot name is required")
            error = 1
        return error
