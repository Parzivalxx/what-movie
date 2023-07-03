def compare_sqlalchemy_objects(object1, object2):
    # Get the attribute names of the instances
    attributes = object1.__table__.columns.keys()

    # Compare the attribute values
    for attr in attributes:
        if attr not in ["id", "added_on"]:
            if getattr(object1, attr) != getattr(object2, attr):
                return False
    return True
