from pyddsclient.httpdao.base import Base


class MessageQueueDAO(Base):
    def __init__(self, request_adapter):
        self.request_adapter = request_adapter
        self.end_point = '/messageQueue'

    def pull(self, quantity=1):
        fields = {
            "quantity": quantity
        }

        rar = self.request_adapter.request('GET', self.end_point, fields)
        return  self.parse_input(rar)

    def push(self, msg):
        return self.request_adapter.request('POST', self.end_point, msg)

    def ack(self, msg_id):
        return self.request_adapter.request('PATCH', self.end_point + '/' + msg_id + '/ack')

    def ack_group(self, msg_group_id):

        return self.request_adapter.request('PATCH', self.end_point + '/' + msg_group_id + '/ack')
