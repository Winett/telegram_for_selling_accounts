from pymongo import MongoClient

class Mongodb:

    def __init__(self, name_db, name_collection):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[name_db]
        self.collection = self.db[name_collection]


    def change_collection(self, change_to):
        self.collection = self.db[change_to]
        return self.collection.full_name


    def change_db(self, change_to):
        self.db = self.client[change_to]
        return self.db.name


    def insert_one_data(self, data):
        return self.collection.insert_one(data).inserted_id


    def insert_many_data(self, dict_of_data):
        return self.collection.insert_many(dict_of_data)


    def find_data(self, search_data, multiple=False, limit=None):
        '''Ex: find_data({"name": "FRIENDS"})'''
        if multiple:
            results = self.collection.find(search_data)
            if limit != None:
                results.limit(limit)
            # results = self.collection.find(search_data, max_scan=4)
            return results
        else:
            return self.collection.find_one(search_data)


    def update_data(self, query_elements, new_values, all_update=False):
        '''Ex: id_ = db.find_data({'name': 'F.R.I.E.N.'}) ищет id искаемого
        db.update_data({'_id': id_}, {'name': 'FFFFF'}) по айди заменяет на что и на указанное'''
        if all_update:
            self.collection.update_many(query_elements, {'$set': new_values})
        else:
            self.collection.update_one(query_elements, {'$set': new_values})


    def delete_data(self, query, all_delete=False):
        if all_delete:
            return  self.collection.delete_many(query).deleted_count
        else:
            return self.collection.delete_one(query).deleted_count


    def count_of_data(self, query):
        return self.collection.count_documents(query)


if __name__ == '__main__':
    db = Mongodb('SeriesDB', 'series')
    print(db.find_data({'name': 'F.R.I.E.N..'}))
    db.delete_data({'_id': db.find_data({'name': 'F.R.I.E.N..'})['_id']})
