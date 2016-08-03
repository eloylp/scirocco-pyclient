class BatchDAO(object):
    def __init__(self, request_adapter):
        self.request_adapter = request_adapter
        self.end_point = '/batches'

    def get_all(self):
        return self.request_adapter.request('GET', self.end_point)

    def get_one(self, id):
        return self.request_adapter.request('GET', self.end_point + '/' + id)

    def delete_one(self, id):
        return self.request_adapter.request('DELETE', self.end_point + '/' + id)

    def delete_all(self):
        return self.request_adapter.request('DELETE', self.end_point)

    def update_one(self, id, data):
        return self.request_adapter.request('PATCH', self.end_point + '/' + id, data)
