from mongoengine import *

class Card(Document):
    cid         = ObjectIdField()
    name        = StringField(required=True, max_length=35)
    desc        = StringField(required=False)
    ucost       = IntField()
    bcost       = IntField()
    rcost       = IntField()
    gcost       = IntField()
    wcost       = IntField()
    total_cost  = ListField(IntField(), default=list)
    ccost       = IntField(required=True)
    image_path  = StringField()

