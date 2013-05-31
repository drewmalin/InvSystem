from util           import session
import flask, flask.views
from decorators     import *
from models         import *

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
