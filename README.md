# BigFix TA
The BigFix TA can be used to configure Splunk to ingest BigFix client, relay, and server logs. There is also a REST input available to format and provide a starting point for "assets.csv" for Splunk Enterprise Security.

# Installation
The BigFix TA should be installed on:

- Search Heads - The add-on contains field extractions for flat logs as well as formatting for the REST input for assets
- Indexers - The add-on contains props.conf and transforms.conf configurations for properly ingesting logs for BigFix clients, relays, and server logs. NOTE: Not all available BigFix logs have been added to the TA. As development progresses, more logs will be added to the add-on for proper ingestion.
- Heavy Forwarder - The REST input should be configured on a heavy forwarder to ensure uninterrupted inputs from the BigFix deployment

This app can be distributed using a deployment server but the host responsible for performing REST API queries should have the app installed ad-hoc and to ensure the configurations are not replaced by the deployment server.

Prior to configuring the add-on, below is a list of requirements to request from the BigFix administrator

1. A console account with login access via REST API only. No other permissions are needed.
2. The account will need to be subsribed to all hosts that will be brought into the asset list.
3. A property the BigFix administrator knows will detail a list of MAC addresses for each host.
4. If necessary, permission to read the site that contains the property for the MAC address if it's not contained within the Master Action Site.

# Configuration
The add-on has configurations included for ingesting raw BigFix component logs for some sources which are listed in the "Sourcetypes" section. The configurations can be found in the "inputs.template" file in the default directory of the add-on. Tailor the app for each BigFix component accordingly. Consult the BigFix administrator for where logs will exist and deploy the configurations accordingly.

First, configure the account and server information for the BigFix deployment
- Click "Configuration" and add the account username and password provided by the BigFix administrator.
- Click the "Add-on Settings" tab and fill in the URL to the BigFix server as well as the port configured for BigFix traffic. The default port is 52311 and is filled in already. Consult your BigFix administrator and ensure this is the proper port.
- Click the "Inputs" tab and click "Create New Input".

Next, configure the Input
- Click "Inputs" and click "Create New Input"
- Configure the interval for how often to query the BigFix server for this information
- Select the index where the data will be stored. If you have a specific index, make sure it's configured prior to enabling this input.
- Select the account configured in the previous step
- Configure the provided "MAC Address Porperty" from your BigFix administrator
- Click "Add"

# Sourcetypes
The BigFix TA uses the following sourcetype format along with the log they currently support:

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

# BigFix Asset List Input
The BigFix TA contains a configurable REST input for collecting the required asset information from a BigFix deployment to be used in a Splunk Enterprise Security implementation. The REST query should return results, even from environments with a large number of clients, in a reasonable amount of time. This requires the coordination with the administrator of BigFix because the field containing the MAC address is not a default property inside of an out-of-the-box BigFix deployment.

You can use the following relevance to collect the MAC addresses of most systems that BigFix supports

```if windows of operating system then concatenation "|" of (mac addresses of adapters of network) else if not windows of operating system then concatenation "|" of ((mac address of it as string) of ip interfaces whose (not loopback of it AND exists mac address of it) of network) else ""```

Once the property is configured in BigFix, you can configure the property name when you configure the input.

# Acknowledgements

This section is to thank the many people who attirbuted the development of this TA by providing relevance, log files, development licenses, and other support.

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
