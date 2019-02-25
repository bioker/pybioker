import json
import requests as r

_api_definition = """
/api/overview                                            |Various random bits of information that describe the whole  system.
/api/cluster-name                                        |Name identifying this RabbitMQ cluster.
/api/nodes                                               |A list of nodes in the RabbitMQ cluster.
/api/nodes/{name}                                        |"An individual node in the RabbitMQ cluster. Add  ""?memory=true"" to get memory statistics, and ""?binary=true""  to get a breakdown of binary memory use (may be expensive if  there are many small binaries in the system)."
/api/extensions                                          |A list of extensions to the management plugin.
/api/definitions/{vhost}                                 |"The server definitions for a given virtual host -  exchanges, queues, bindings and policies.  POST to upload an existing set of definitions. Note that;  The definitions are merged. Anything already existing on  the server but not in the uploaded definitions is  untouched.  Conflicting definitions on immutable objects (exchanges,  queues and bindings) will cause an error.  Conflicting definitions on mutable objects will cause  the object in the server to be overwritten with the  object from the definitions.  In the event of an error you will be left with a  part-applied set of definitions.  For convenience you may upload a file from a browser to this  URI (i.e. you can use multipart/form-data as  well as application/json) in which case the  definitions should be uploaded as a form field named  ""file""."
/api/connections                                         |A list of all open connections.
/api/vhosts/{vhost}/connections                          |A list of all open connections in a specific vhost.
/api/connections/{name}                                  |"An individual connection. DELETEing it will close the  connection. Optionally set the ""X-Reason"" header when  DELETEing to provide a reason."
/api/connections/{name}/channels                         |List of all channels for a given connection.
/api/channels                                            |A list of all open channels.
/api/vhosts/{vhost}/channels                             |A list of all open channels in a specific vhost.
/api/channels/{channel}                                  |Details about an individual channel.
/api/consumers                                           |A list of all consumers.
/api/consumers/{vhost}                                   |A list of all consumers in a given virtual host.
/api/exchanges                                           |A list of all exchanges.
/api/exchanges/{vhost}                                   |A list of all exchanges in a given virtual host.
/api/exchanges/{vhost}/{name}                            |"An individual exchange. To PUT an exchange, you will need a body looking something like this;  {""type"";""direct"",""auto_delete"";false,""durable"";true,""internal"";false,""arguments"";{}}  The type key is mandatory; other keys are optional.  When DELETEing an exchange you can add the query string  parameter if-unused=true. This prevents the  delete from succeeding if the exchange is bound to a queue  or as a source to another exchange."
/api/exchanges/{vhost}/{name}/bindings/source            |A list of all bindings in which a given exchange is the source.
/api/exchanges/{vhost}/{name}/bindings/destination       |A list of all bindings in which a given exchange is the destination.
/api/exchanges/{vhost}/{name}/publish                    |"Publish a message to a given exchange. You will need a body  looking something like;  {""properties"";{},""routing_key"";""my key"",""payload"";""my body"",""payload_encoding"";""string""}  All keys are mandatory. The payload_encoding  key should be either ""string"" (in which case the payload  will be taken to be the UTF-8 encoding of the payload field)  or ""base64"" (in which case the payload field is taken to be  base64 encoded).  If the message is published successfully, the response will  look like;  {""routed""; true}  routed will be true if the message was sent to  at least one queue.  Please note that the HTTP API is not ideal for high  performance publishing; the need to create a new TCP  connection for each message published can limit message  throughput compared to AMQP or other protocols using  long-lived connections."
/api/queues                                              |A list of all queues.
/api/queues/{vhost}                                      |A list of all queues in a given virtual host.
/api/queues/{vhost}/{name}                               |"An individual queue. To PUT a queue, you will need a body looking something like this;  {""auto_delete"";false,""durable"";true,""arguments"";{},""node"";""rabbit@smacmullen""}  All keys are optional.  When DELETEing a queue you can add the query string  parameters if-empty=true and /  or if-unused=true. These prevent the delete  from succeeding if the queue contains messages, or has  consumers, respectively."
/api/queues/{vhost}/{name}/bindings                      |A list of all bindings on a given queue.
/api/queues/{vhost}/{name}/contents                      |Contents of a queue. DELETE to purge. Note you can't GET this.
/api/queues/{vhost}/{name}/actions                       |"Actions that can be taken on a queue. POST a body like;  {""action"";""sync""} Currently the actions which are  supported are sync and cancel_sync."
/api/queues/{vhost}/{name}/get                           |"Get messages from a queue. (This is not an HTTP GET as it  will alter the state of the queue.) You should post a body looking like;  {""count"";5,""ackmode"";""ack_requeue_true"",""encoding"";""auto"",""truncate"";50000}  count controls the maximum number of  messages to get. You may get fewer messages than this if  the queue cannot immediately provide them.  ackmode determines whether the messages will be  removed from the queue. If ackmode is ack_requeue_true or reject_requeue_true they will be requeued -  if ackmode is ack_requeue_false or reject_requeue_false they will be removed.  encoding must be either ""auto"" (in which case the  payload will be returned as a string if it is valid UTF-8, and  base64 encoded otherwise), or ""base64"" (in which case the payload  will always be base64 encoded).  If truncate is present it will truncate the  message payload if it is larger than the size given (in bytes).  truncate is optional; all other keys are mandatory.  Please note that the get path in the HTTP API is intended  for diagnostics etc - it does not implement reliable  delivery and so should be treated as a sysadmin's tool  rather than a general API for messaging."
/api/bindings                                            |A list of all bindings.
/api/bindings/{vhost}                                    |A list of all bindings in a given virtual host.
/api/bindings/{vhost}/e/{exchange}/q/{queue}             |"A list of all bindings between an exchange and a  queue. Remember, an exchange and a queue can be bound  together many times!  To create a new binding, POST to this  URI. Request body should be a JSON object optionally containing  two fields, routing_key (a string) and arguments (a map of optional arguments);  {""routing_key"";""my_routing_key"", ""arguments"";{""x-arg""; ""value""}}  All keys are optional.  The response will contain a Location header  telling you the URI of your new binding."
/api/bindings/{vhost}/e/{exchange}/q/{queue}/{props}     |"An individual binding between an exchange and a queue.  The props part of the URI is a ""name"" for the binding  composed of its routing key and a hash of its  arguments. props is the field named ""properties_key""  from a bindings listing response."
/api/bindings/{vhost}/e/{source}/e/{destination}         |"A list of all bindings between two exchanges, similar to  the list of all bindings between an exchange and a queue,  above.  To create a new binding, POST to this  URI. Request body should be a JSON object optionally containing  two fields, routing_key (a string) and arguments (a map of optional arguments);  {""routing_key"";""my_routing_key"", ""arguments"";{""x-arg""; ""value""}}  All keys are optional.  The response will contain a Location header  telling you the URI of your new binding."
/api/bindings/{vhost}/e/{source}/e/{destination}/{props} |"An individual binding between two exchanges. Similar to  the individual binding between an exchange and a queue,  above."
/api/vhosts                                              |A list of all vhosts.
/api/vhosts/{name}                                       |"An individual virtual host. As a virtual host usually only  has a name, you do not need an HTTP body when PUTing one of  these. To enable / disable tracing, provide a body looking like;  {""tracing"";true}"
/api/vhosts/{name}/permissions                           |A list of all permissions for a given virtual host.
/api/vhosts/{name}/topic-permissions                     |A list of all topic permissions for a given virtual host.
/api/vhosts/{name}/start/node                            |Starts virtual host name on node node.
/api/users/                                              |A list of all users.
/api/users/without-permissions                           |A list of users that do not have access to any virtual host.
/api/users/bulk-delete                                   |"Bulk deletes a list of users. Request body must contain the list;  {""users"" ; [""user1"", ""user2"", ""user3""]}"
/api/users/name                                          |"An individual user. To PUT a user, you will need a body looking something like this; {""password"";""secret"",""tags"";""administrator""} or; {""password_hash"";""2lmoth8l4H0DViLaK9Fxi6l9ds8="", ""tags"";""administrator""}  The tags key is mandatory. Either  password or password_hash  must be set. Setting password_hash to " will ensure the  user cannot use a password to log in. tags is a  comma-separated list of tags for the user. Currently recognised tags  are administrator, monitoring and management.  password_hash must be generated using the algorithm described  here.  You may also specify the hash function being used by adding the hashing_algorithm  key to the body. Currently recognised algorithms are rabbit_password_hashing_sha256, rabbit_password_hashing_sha512, and rabbit_password_hashing_md5."
/api/users/{user}/permissions                            |A list of all permissions for a given user.
/api/users/{user}/topic-permissions                      |A list of all topic permissions for a given user.
/api/whoami                                              |Details of the currently authenticated user.
/api/permissions                                         |A list of all permissions for all users.
/api/permissions/{vhost}/{user}                          |"An individual permission of a user and virtual host. To PUT a permission, you will need a body looking something like this; {""configure"";"".*"",""write"";"".*"",""read"";"".*""}  All keys are mandatory."
/api/topic-permissions                                   |A list of all topic permissions for all users.
/api/topic-permissions/{vhost}/{user}                    |"Topic permissions for a user and virtual host. To PUT a topic permission, you will need a body looking something like this;  {""exchange"";""amq.topic"",""write"";""^a"",""read"";"".*""}  All keys are mandatory."
/api/parameters                                          |A list of all vhost-scoped parameters.
/api/parameters/{component}                              |A list of all vhost-scoped parameters for a given component.
/api/parameters/{component}/{vhost}                      |A list of all vhost-scoped parameters for a given component and virtual host.
/api/parameters/{component}/{vhost}/name                 |"An individual vhost-scoped parameter. To PUT a parameter, you will need a body looking something like this; {""vhost""; ""/"",""component"";""federation"",""name"";""local_username"",""value"";""guest""}"
/api/global-parameters                                   |A list of all global parameters.
/api/global-parameters/{name}                            |"An individual global parameter. To PUT a parameter, you will need a body looking something like this; {""name"";""user_vhost_mapping"",""value"";{""guest"";""/"",""rabbit"";""warren""}}"
/api/policies                                            |A list of all policies.
/api/policies/{vhost}                                    |A list of all policies in a given virtual host.
/api/policies/{vhost}/name                               |"An individual policy. To PUT a policy, you will need a body looking something like this; {""pattern"";""^amq."", ""definition""; {""federation-upstream-set"";""all""}, ""priority"";0, ""apply-to""; ""all""}  pattern and definition are mandatory, priority and apply-to are optional."
/api/operator-policies                                   |A list of all operator policy overrides.
/api/operator-policies/{vhost}                           |A list of all operator policy overrides in a given virtual host.
/api/operator-policies/{vhost}/name                      |"An individual operator policy. To PUT a policy, you will need a body looking something like this; {""pattern"";""^amq."", ""definition""; {""expires"";100}, ""priority"";0, ""apply-to""; ""queues""}  pattern and definition are mandatory, priority and apply-to are optional."
/api/aliveness-test/{vhost}                              |"Declares a test queue, then publishes and consumes a  message. Intended for use by monitoring tools. If everything  is working correctly, will return HTTP status 200 with  body; {""status"";""ok""} Note; the test queue will  not be deleted (to to prevent queue churn if this is  repeatedly pinged)."
/api/healthchecks/node                                   |"Runs basic healthchecks in the current node. Checks that the rabbit  application is running, channels and queues can be listed successfully, and  that no alarms are in effect. If everything is working correctly, will  return HTTP status 200 with body; {""status"";""ok""} If  something fails, will return HTTP status 200 with the body of  {""status"";""failed"",""reason"";""string""}"
/api/healthchecks/node/{node}                            |"Runs basic healthchecks in the given node. Checks that the rabbit  application is running, list_channels and list_queues return, and  that no alarms are raised. If everything is working correctly, will  return HTTP status 200 with body; {""status"";""ok""} If  something fails, will return HTTP status 200 with the body of  {""status"";""failed"",""reason"";""string""}"
/api/vhost-limits                                        |Lists per-vhost limits for all vhosts.
/api/vhost-limits/{vhost}                                |Lists per-vhost limits for specific vhost.
/api/vhost-limits/{vhost}/name                           |"Set or delete per-vost limit for vhost with name.  Limits are set using a JSON document in the body;  {""max-connections""; 100, ""max-queues""; 200}"
"""

class RabbitMQAdmin:
    
    def __init__(self, url, auth):
        """Admin abstraction to perform management api requests
        
        :param url: url of rabbitmq management api
        :param auth: tuple with user and password
        
        :type url: str
        :type auth: tuple
        """
        self.url = url
        self.auth = auth

    def get_requests(self):
        """Get possible requests for api. Result is a dict with 
        path of endpoint as a key, description and callable function to
        invoke it

        :rtype: dict
        """
        requests = {}
        for line in _api_definition.strip().splitlines():
            path_template, description = line.split('|')
            requests[path_template.strip()] = {
                    'description': description,
                    # TODO complete function for calling
                    'callable': lambda method,body: json.loads(
                        r.request(method=method, url=url, body=body).text)}
        return requests
