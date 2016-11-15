# Scirocco Pyclient
[![Build Status](https://travis-ci.org/eloylp/scirocco-pyclient.svg?branch=master)](https://travis-ci.org/eloylp/scirocco-pyclient)


This is a handy library to interact with the [scirocco-server](https://github.com/eloylp/scirocco-server) project. If you dont know about it , please read first that project docs.

## Installation

This client library has two main install methods.

#### From source:
```bash
 git clone https://github.com/eloylp/scirocco-pyclient.git
 python3 setup.py install
```

#### From pip3:
```bash
 pip3 install scirocco-pyclient
```

## Using the client

#### The response object

Every operation in this client will return the same [response object](https://github.com/eloylp/scirocco-pyclient/blob/docs/sciroccoclient/responses.py)
, representing the state of the operation as well as the resultant message payload representation.

#### Instantiating the client

You must instantiate the HTTPClient by passing three params. 
Respectively they are:

* [scirocco-server](https://github.com/eloylp/scirocco-server) endpoint (take care about http/https schema).
* Your pre-stablished by convention node id (hexadecimal string, will be a mongo Objectid in future). 
* The master auth token for gain access to that scirocco-server instance.

```python

from sciroccoclient.httpclient import HTTPClient

scirocco = HTTPClient('http://localhost', 'af123', 'DEFAULT_TOKEN')
```

#### Pushing messages
Pushing messages is simple as populate [scirocco message object](https://github.com/eloylp/scirocco-pyclient/blob/develop/sciroccoclient/messages.py).

```python
from sciroccoclient.messages import SciroccoMessage

# Preparing our fixed message properties.

msg = SciroccoMessage()
msg.node_destination = 'af123'

# Pushing an object

msg.payload = {"type": "message"}
scirocco.push(msg)

#Pushing a string message payload

msg.payload = 'message'
scirocco.push(msg)

# Pushing binary payload

with open('file.bin', 'rb') as f:
    msg.payload = f.read()
    msg.payload_type = '.bin'
    scirocco.push(msg)
    
# Pushing scheduled messages, 4 days in future (All in UTC).
from datetime import datetime, timedelta

msg.payload = 'This is an scheduled message.'
msg.scheduled_time = datetime.utcnow() + timedelta(days=4)
scirocco.push(msg)

```
Some tips about above code are:

* payload_type property is a 50 characters free field for determining 
  how data must be handled in the consumer part. If not setted scirocco will
  populate it with detected mime type.
* Scheduled messages, are messages that are not available to consumers
  until reaching scheduled_time in time frame. **Warning** , this is not
  the "consuming time", only the moment that are marked as "available" to
  consumers.

#### Receiving messages

You will receive messages in the same data type as you send it, except for binary
type. You will push binary , and the item is stored as binary , but you will receive 
it in base64 representation.

```python

response_object = scirocco.pull()

# print message metadata
print(response_object.metadata.__dict__)

# print the message payload.
print(response_object.payload)
```

If no pending messages the client will return None else, it will return
a response object which contains metadata and payload. The message
will change its status to 'processing', so it cannot be accesible by other
'pull' operation.

#### Confirming messages (ack operation)

When you deal with IPC (inter process communications) or interdependant operations in different processes,
you need to mark the message as "processed" for further operations
in other processes.

You only need to save the id of the message that will be confirmed from
response object (response_object.metadata.id) in its pull operation to confirm
the message by id. For example if we want to confirm '5823a70203c123003de4229b' 
message id , the code will be :

```python
scirocco.ack('5823a70203c123003de4229b')
```


#### Reviewing a message

If you only need to watch the status of a message/es , 
call for get function, passing as parameter the id of message. Like this.

```python
scirocco.get('5823a70203c123003de4229b')
```


#### Getting all messages incoming/sended to/by this node

You optionally can pass a first argument to limit the returned results.
Anyway, it will be limited by a server side config parameter. 

```python
scirocco.get_all()

# Limiting results by 10 (ordered by creation date)
scirocco.get_all(10)

```

#### Updating a message

As first parameter the id of the message. As second parameter the new data
payload.

```python
scirocco.update_one(msg_id, new_payload)
```

#### Deleting a message

You must specify as first parameter id of the message to be permanent removed
from the system no matters its state. Cannot be undone.

```python
scirocco.delete_one('5823a70203c123003de4229b')
```

#### Deleting all messages

Delete from the system all messages incoming/sended to/by this node.
This operation only may be executed if you want a total reset of the node and
its actions. Cannot be undone.

```python
scirocco.delete_all()
```

