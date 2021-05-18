[logging]
loglevel = <string>

[additional_parameters]
bigfix_server_url = <string>
* Full URL for the BigFix server

bigfix_server_port = <int>
* Management port for BigFix server.
* The default port number from HCL is "52311"
* Customizable by deployment

query_timeout_seconds = <int>
* The amount of time each query sent to the BigFix server waits for a response.
* If there is no response, the query fails and exits the loop.
