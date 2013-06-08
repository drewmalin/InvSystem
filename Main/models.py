import datetime
from util           import Base
from sqlalchemy     import Column, Integer, String, ForeignKey, Float, DateTime, desc
from sqlalchemy.orm import relationship, backref

class Item(Base):
    # Table
    __tablename__ = 'Item'
    
    # Attributes
    id                  = Column(Integer, primary_key = True)
    
    # Relationships
    snapshots           = relationship('ItemSnapshot', backref='item', order_by='ItemSnapshot.timestamp.desc()')

class ItemSnapshot(Base):
    # Table
    __tablename__       = 'ItemSnapshot'
    
    # Attributes
    id 					= Column(Integer, primary_key = True)
    item_id             = Column(Integer, ForeignKey('Item.id'))
    timestamp           = Column(DateTime, default=datetime.datetime.now)
    name 				= Column(String(100))
    num					= Column(String(100))
    quantity_on_hand 	= Column(Integer)
    reorder_quantity	= Column(Integer)
    reorder_point		= Column(Integer)
    lot_id              = Column(Integer, ForeignKey('Lot.id'))
    primary_vendor_id   = Column(Integer, ForeignKey('Vendor.id'))
    secondary_vendor_id = Column(Integer, ForeignKey('Vendor.id'))
    primary_vendor_q    = Column(Integer)
    secondary_vendor_q  = Column(Integer)
    primary_vendor_p    = Column(Integer)
    secondary_vendor_p  = Column(Integer)
    
    # Relatioships
    primary_vendor      = relationship('Vendor', primaryjoin='Vendor.id==ItemSnapshot.primary_vendor_id', backref='snapshots_as_primary')
    secondary_vendor    = relationship('Vendor', primaryjoin='Vendor.id==ItemSnapshot.secondary_vendor_id', backref='snapshots_as_secondary')
    lot 				= relationship('Lot', backref='snapshots')
    
    def __init__(self, name, num, quantity_on_hand, reorder_quantity, reorder_point):
        self.name 				= name
        self.num 				= num
        self.quantity_on_hand 	= quantity_on_hand
        self.reorder_quantity	= reorder_quantity
        self.reorder_point		= reorder_point

class Vendor(Base):
    # Table
    __tablename__   = 'Vendor'
    
    # Attributes
    id              = Column(Integer, primary_key = True)
    name 		    = Column(String(100))
    
    def __init__(self, name):
        self.name = name

class Lot(Base):
    # Table
    __tablename__   = 'Lot'

    # Attributes
    id              = Column(Integer, primary_key = True)
    state           = Column(String(100))
    name            = Column(String(100))

    def __init__(self, name):
        self.name = name
