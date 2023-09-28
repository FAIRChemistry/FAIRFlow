def enumerate_objects(self, objects):
    object_dict = {index: object for index, object in enumerate(self.objects)}
    for index, object in object_dict.items():
        print(f"{index}: {object.id}")
    return object_dict
