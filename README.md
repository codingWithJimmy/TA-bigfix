# HCL BigFix Add-on for Splunk
The HCL BigFix Add-on for Splunk can be used to configure Splunk to ingest BigFix client, relay, and server logs. It also contains multiple modular inputs to query the REST API of a BigFix core server.

# Compatability
The HCL BigFix Add-on for Splunk is Python2 and Python3 compatible so it will run on Splunk Enterprise 7.x and 8.x.

# Installation
The HCL BigFix Add-on for Splunk should be installed on:

- Search Heads - The add-on contains field extractions for flat logs as well as formatting for the REST input for assets
- Indexers - The add-on contains props.conf and transforms.conf configurations for properly ingesting logs for BigFix clients, relays, and server logs. NOTE: Not all available BigFix logs have been added to the add-on. As development progresses, more logs will be added to the add-on for proper ingestion.
- Heavy Forwarder - The modular inputs should be configured on a heavy forwarder to ensure uninterrupted inputs from the BigFix deployment

This app can be distributed using a deployment server but the host responsible for performing modular input queries should have the app installed ad-hoc and to ensure the configurations are not replaced by the deployment server.

Prior to configuring the add-on, below is a list of requirements to request from the BigFix administrator

1. A console account with the following capabilities:
- Show Other Operators' Actions
- Can Submit Queries
- Can use REST API
2. The account will need to be subscribed to all sites where information is to be evaluated from.
3. The account will need to have the proper computer assignments.

# Configuration
The add-on has configurations included for ingesting raw BigFix component logs for some sources which are listed in the "Sourcetypes" section. The configurations can be found in the "inputs.template" file in the default directory of the add-on. Tailor the app for each BigFix component accordingly. Consult the BigFix administrator for where logs will exist and deploy the configurations accordingly.

Configure the account and server information for the BigFix deployment by doing the following:
- Click "Configuration" and add the account username and password provided by the BigFix administrator.	- Click the "Add-on Settings" tab and fill in the URL to the BigFix server as well as the port configured for BigFix traffic. The default port is 52311 and is filled in already. Consult your BigFix administrator and ensure this is the proper port.
- Click the "Inputs" tab and click the "Create New Input" dropdown to configure the modular REST API inputs.

# Configure the HCL BigFix Add-on for Splunk using configuration files
It is possible to configure the add-on without the use of the Splunk Web front-end by following these steps.

1. Install the HCL BigFix Add-on for Splunk into `$SPLUNK_HOME/etc/apps` and restart Splunk
2. Use curl to send requests to the Splunk REST API to configure the password for the BigFix account.
- Take note of the [bracketed] value below. This password is the password of the user account that will be used to access the BigFix server.
```
curl -k -u admin https://localhost:8089/servicesNS/nobody/TA-bigfix/storage/passwords -d name='BigFix``splunk_cred_sep``1' -d password='{"password": "[bigfix_user_account_password]"}' -d realm=__REST_CREDENTIAL__#TA-bigfix#configs/conf-ta_bigfix_account
```
- The second curl command does not need to be changed and should be added as is.
```
curl -k -u admin https://localhost:8089/servicesNS/nobody/TA-bigfix/storage/passwords -d name='BigFix``splunk_cred_sep``2' -d password='``splunk_cred_sep``S``splunk_cred_sep``P``splunk_cred_sep``L``splunk_cred_sep``U``splunk_cred_sep``N``splunk_cred_sep``K``splunk_cred_sep``' -d realm=__REST_CREDENTIAL__#TA-bigfix#configs/conf-ta_bigfix_account
```
3. Create `$SPLUNK_HOME/etc/apps/TA-bigfix/local/ta_bigfix_account.conf` and populate it with the following:
```
[BigFix]
password = ********
username = [bigfix_user_account_name]
```
- Add the proper BigFix user account name to the configuration in the `username` field. Do *NOT* change the value for `password`.
4. Create `$SPLUNK_HOME/etc/apps/TA-bigfix/local/ta_bigfix_settings.conf` and populate it with the following:
```
[additional_parameters]
bigfix_server_port = 52311
bigfix_server_url = [ bigfix_server_url ]
query_timeout_seconds = 120

[logging]
loglevel = DEBUG
```
- Configure the proper BigFix URL of the core server or backup server with access to the backend database to perform REST calls.
5. Create `$SPLUNK_HOME/etc/apps/TA-bigfix/local/inputs.conf` and populate it with the following:
```
[bigfix_clients://Clients]
mac_address_property = <BIGFIX_PROPERTY_FOR_MAC_ADDRESS>
global_account = BigFix
set_batch_value = 1
interval = 3600
index = <PREFERED_INDEX>

[bigfix_actions://Actions]
set_batch_value = 1
global_account = BigFix
disabled = 0
interval = 3600
index = <PREFERED_INDEX>

[bigfix_available_fixlets://AvailableFixlets]
site_name = <DESIRED_SITE_NAME>
fixlet_types = Fixlet~Task~Analysis
global_account = BigFix
set_batch_value = 1
interval = 3600
index = <PREFERED_INDEX>

[bigfix_relevant_fixlets://RelevantFixlets]
site_name = <DESIRED_SITE_NAME>
global_account = BigFix
set_batch_value = 1
interval = 3600
index = <PREFERED_INDEX>

[bigfix_infrastructure://Infrastructure]
global_account = BigFix
interval = 3600
index = <PREFERED_INDEX>

[bigfix_users://Users]
global_account = BigFix
interval = 3600
index = <PREFERED_INDEX>

[bigfix_analysis://<ANALYSIS_NAME>]
site_name = <DESIRED_SITE_NAME>
analysis_id = <DESIRED_ANALYSIS_ID>
global_account = BigFix
set_batch_value = 1
interval = 3600
index = <PREFERED_INDEX>
```
- Adjust the values for each of the inputs according to the needs of the environment.
- See [BigFix Analysis Input](#bigfix-analysis-input) for the details on how to configure Analysis input(s).
- See [BigFix Client Input](#bigfix-clients-input) for details on configuring the property of the MAC Address for clients.
6. Restart Splunk

# Sourcetypes
The HCL BigFix Add-on for Splunk uses the following sourcetype format along with the log they currently support:

 Sourcetype | BigFix Component
 --- | ---
bigfix:client:log | BigFix Clients
bigfix:relay:log | BigFix Relays
bigfix:server:log | BigFix Server Core
bigfix:server:audit:log | BigFix Server Audit
bigfix:filldb:log | BigFix FillDB
bigfix:gather:log | BigFix GatherDB
bigfix:webrepoprt:log | BigFix Web Reports
bigfix:ape:mfs:log | BigFix Server Automation Core
bigfix:ape:notifier:app:log | BigFix Server Automation Notification Service app
bigfix:ape:notifier:monitor:log | BigFix Server Automation Notification Service monitor  
bigfix:ape:notifier:service:log | BigFix Server Automation Notification Service status
bigfix:ape:plan:engine:log | BigFix Server Automation Plan Engine
bigfix:compliance:import:log | BigFix Compliance Import Log

 Modular Inputs | Sourcetype | BigFix Component
--- | --- | ---
BigFix Clients | bigfix:clients | BigFix client list export using REST (Requires "BES Component Versions" analysis of "BES Support" site to be activated)
BigFix Actions | bigfix:action | BigFix action status export using REST
BigFix Analysis | bigfix:analysis | BigFix analysis result export using REST
BigFix Users | bigfix:users | BigFix user list export using REST
BigFix Infrastructure | bigfix:infrastructure | BigFix infrastructure export using REST (Requires "BES Health Checks" analysis of "BES Support" site to be activated)
BigFix Available Fixlets | bigfix:fixlets:available | BigFix available fixlet export using REST
BigFix Relevant Fixlets | bigfix:fixlets:relevant | BigFix relevant fixlet export using REST

# BigFix Inputs Using Batching
The improve the scalability of the HCL BigFix Add-on for Splunk, the inputs have been rewritten to allow for batch-adding the data. This is done by looping through based on modulation of a specific integer of the results of the relevance query. It basically increments and brings in different results based on however many batches you're looking to run the ingestion on.

The right modulous depends on the size of the environment. Lower client counts means less cardinality of events where you are less likely to have over 100,000 results for a single query using the inputs. As the number of results begins to exponentially grow, your modulous should grow as well. I would recommend that for every 10,000 potential results you have, you increase your modulous by 10.

This means if you are collecting BigFix Action results and an action has gone out to 10,000 machines, your modulous input should use be a batch of **10**. Feel free to experiment and I encourage anyone who knows maths way better than me to report back with what would be a good ratio.

# BigFix Clients Input
The HCL BigFix Add-on for Splunk contains a configurable REST input for collecting client information from a BigFix deployment. The REST query should return results, even from environments with a large number of clients, in a reasonable amount of time. This requires the coordination with the administrator of BigFix because the field containing the MAC address is not a default property inside of an out-of-the-box BigFix deployment.

Some notes on further requirements for this input:
- A property the BigFix administrator knows will need to be identified which details a list of MAC addresses for each host. This property will need to be configured with the input. If there is a not a currently configured property, the BigFix administrator may use the relevance below to evaluate the property.
- The account used to perform the query will need permission to, at least, read the site that contains the property for the MAC address if it's not contained within the Master Action Site.
- The query relies on results from analysis within the "BES Support" site. The user account will need to be assigned to the site to view those results.

If the MAC addresses of the clients are not being evaluated, you can use the following relevance to collect the MAC addresses of most systems that BigFix supports

```
if windows of operating system then concatenation "|" of (mac addresses of adapters of network) else if not windows of operating system then concatenation "|" of ((mac address of it as string) of ip interfaces whose (not loopback of it AND exists mac address of it) of network) else ""
```

Once the property is configured in BigFix, you can configure the property name when you configure the input.

# BigFix Analysis Input
The HCL BigFix Add-on for Splunk contains a configurable REST input for ingesting the results of a specificed analysis within BigFix. This will require the display name of the analysis being imported. Once congfigured, the results are ingested per property result per host in a single event so multiple properties within a single analysis can be identified and evaluated once the events are ingested. This will also break multi-value results into their own events with the same property name.

To configure a specific analysis for ingestion, your BigFix administrator will need to provide the integer ID of the analysis as well as the site that analysis exists under. Once you configure those values, your analysis will be ingested.

Another consideration when configuring this input is how often the analysis property is updated. If any analysis property is normally only evaluated on the endpoints once a day, the interval for the ingestion of that analysis should be no less than "86400" (24 hours in seconds). Consult your BigFix administrator for evaluation times of analysis that you want to import to ensure your ingestion interval is as long or longer than the analysis interval.

# Acknowledgements

This section is to thank the many people who contributed to the development of this add-on by providing relevance, log files, development licenses, larger environments, and other support.

- Jason Walker
- Geetha Alagppan
- Mark "Gunny" Collins
- Mark Spryer
- Eric Howard
- Josh Rice
- James Stewart
- Aram Eblighatian
- Jimmy Glass
- Keith Hutchison
- John Talbert
- Brian Kessler
- LaVon Smith
