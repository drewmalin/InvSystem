from util           import session
import flask, flask.views
from decorators     import *
from models         import *
from datetime       import datetime, date

class VendorAPI(flask.views.MethodView):
    @crossdomain(origin='*')
    def get(self, vendor_id):
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

class QuantityAPI(flask.views.MethodView):
    @crossdomain(origin='*')
    def get(self, item_id):
        quantity_list = []
        date_list = []

        item = session.query(Item).get(item_id)
        for snap in reversed(item.snapshots):
            quantity_list.append(snap.quantity_on_hand)
            date_list.append(snap.timestamp.strftime('%m/%d/%Y %I:%M:%S %p'))
        
        data = getQuantityData(item, quantity_list)

        return flask.jsonify(data=data, dates=date_list)

def getQuantityData(item, quantity_list):
    dataList = []
    dataDict = {}

    dataDict["name"] = item.snapshots[0].name
    dataDict["data"] = quantity_list

    dataList.append(dataDict)

    return dataList
