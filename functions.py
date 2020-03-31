from flask import flash

# class Unique(object):
#     def __init__(self, model, field, message="", data):
#         self.model = model
#         self.field = field
#         self.message = message


# Checks if already exists in database
def is_unique(model, field, data, model2, id):
    if model2 and id:
        check = model.query.join(model2).filter(model2.id == id).filter(field == data).first()
    else:
        check = model.query.filter_by(field == data).first()
    if check:
        return False
    else:
        return True
