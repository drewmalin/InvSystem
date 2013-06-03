from util           import session
import flask, flask.views
from decorators     import *
from models         import *
from datetime       import datetime, date
import json
import csv
from Tkinter        import Tk
from tkFileDialog   import askopenfilename

class VendorsAPI(flask.views.MethodView):
    @crossdomain(origin='*')
    def get(self, vendor_id):
        if vendor_id == None:
            vendor_filter = request.args.get("q")

            if not vendor_filter:
                vendors = session.query(Vendor)
            else:
                vendors = session.query(Vendor).filter(Vendor.name.contains(vendor_filter))

            vendor_list = []
            for vendor in vendors:
                vendor_dict = {}
                vendor_dict["id"] = str(vendor.id)
                vendor_dict["text"] = vendor.name
                vendor_list.append(vendor_dict)
            return flask.jsonify(results=vendor_list)
        else:
            vendor = session.query(Vendor).get(vendor_id)
            vendor_list = []
            vendor_dict = {}
            vendor_dict["id"] = str(vendor.id)
            vendor_dict["text"] = vendor.name
            vendor_list.append(vendor_dict)
            return flask.jsonify(results=vendor_list)

class VendorAPI(flask.views.MethodView):
    @crossdomain(origin='*')
    def post(self, item_id):
        
        if item_id == None or flask.request.form['vendor'] == "" or flask.request.form['quantity'] == "":
            return ""

        item = session.query(Item).get(item_id)
        vendor = session.query(Vendor).get(flask.request.form['vendor'])
        itemSnapshot = getNextSnapshot(item)

        if int(flask.request.form['vendor']) == int(item.snapshots[0].primary_vendor.id):
            itemSnapshot.primary_vendor_q = flask.request.form['quantity']
        else:
            itemSnapshot.secondary_vendor_q = flask.request.form['quantity']

        item.snapshots.append(itemSnapshot)
        session.commit()

        return flask.redirect(flask.url_for('item', item_id=item_id))


class QuantityAPI(flask.views.MethodView):
    @crossdomain(origin='*')
    def get(self, item_id):
        
        if item_id == None:
            return ""

        quantity_list = []
        date_list = []

        item = session.query(Item).get(item_id)
        uniqueQuantity = -1
        for snap in reversed(item.snapshots):
            if snap.quantity_on_hand != uniqueQuantity:
                uniqueQuantity = snap.quantity_on_hand
                quantity_list.append(snap.quantity_on_hand)
                date_list.append(snap.timestamp.strftime('%b %d'))
        
        data = getQuantityData(item, quantity_list)

        return flask.jsonify(data=data, dates=date_list)
    
    @crossdomain(origin='*')
    def post(self, item_id):
        
        if item_id == None or flask.request.form['quantity'] == "":
            return flask.render_template('index.html')

        item = session.query(Item).get(item_id)
        itemSnapshot = getNextSnapshot(item)
        itemSnapshot.quantity_on_hand = flask.request.form['quantity']

        item.snapshots.append(itemSnapshot)
        session.commit()
        return flask.redirect(flask.url_for('item', item_id=item_id))

class ItemVendorsAPI(flask.views.MethodView):
    @crossdomain(origin='*')
    def get(self, item_id):
        item = session.query(Item).get(item_id)
        vendor_list = []
        p_vendor_dict = {}
        s_vendor_dict = {}

        # Primary
        vendor = item.snapshots[0].primary_vendor
        if vendor != None:
            p_vendor_dict["id"] = vendor.id
            p_vendor_dict["text"] = vendor.name
            vendor_list.append(p_vendor_dict)

        # Secondary
        vendor = item.snapshots[0].secondary_vendor
        if vendor != None:
            s_vendor_dict["id"] = vendor.id
            s_vendor_dict["text"] = vendor.name
            vendor_list.append(s_vendor_dict) 
        return flask.jsonify(results=vendor_list)

class ReportAPI(flask.views.MethodView):
    @crossdomain(origin='*')
    def get(self, report_id):
        item_list = [] 
        if report_id == 0:
            # Reorder Report
            items = session.query(Item)
            items = [x for x in items if x.snapshots[0].quantity_on_hand <= x.snapshots[0].reorder_point]
            item_list = items
        elif report_id == 1:
            # Item Report
            items = session.query(Item)
            item_list = items

        if flask.request.args["export"] and flask.request.args["export"] == "t":
            filename = "test.csv"
            f = csv.writer(open('csv/'+filename, 'wb+'))
            f.writerow(['Name', 'Catalog Number', 'Quantity On Hand', 'Reorder Point', 'Primary Vendor', 'Secondary Vendor'])
            for item in item_list:
                sv = item.snapshots[0].secondary_vendor
                svn = ""
                if sv:
                    svn = sv.name
                f.writerow([item.snapshots[0].name,
                    item.snapshots[0].num,
                    item.snapshots[0].quantity_on_hand,
                    item.snapshots[0].reorder_quantity,
                    item.snapshots[0].primary_vendor.name,
                    svn])
        
        return flask.render_template('reports.html', items=items)

def getNextSnapshot(item):
    oldSnapshot = item.snapshots[0]
    newSnapshot = ItemSnapshot(oldSnapshot.name,
        oldSnapshot.num,
        oldSnapshot.quantity_on_hand,
        oldSnapshot.reorder_quantity,
        oldSnapshot.reorder_point)
    newSnapshot.primary_vendor_p = oldSnapshot.primary_vendor_p
    newSnapshot.primary_vendor_q = oldSnapshot.primary_vendor_q
    newSnapshot.primary_vendor = oldSnapshot.primary_vendor
    newSnapshot.secondary_vendor_p = oldSnapshot.secondary_vendor_p
    newSnapshot.secondary_vendor_q = oldSnapshot.secondary_vendor_q
    newSnapshot.secondary_vendor = oldSnapshot.secondary_vendor

    return newSnapshot

def getQuantityData(item, quantity_list):
    dataList = []
    dataDict = {}

    dataDict["name"] = item.snapshots[0].name
    dataDict["data"] = quantity_list

    dataList.append(dataDict)

    return dataList
