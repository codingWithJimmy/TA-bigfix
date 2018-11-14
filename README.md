# BigFix TA
The BigFix TA can be used to configure Splunk to ingest BigFix client, relay, and server logs. There is also a REST input available to format and provide a starting point for "assets.csv" for Splunk Enterprise Security.

# Installation
The BigFix TA should be installed on:

- Search Heads - The add-on contains field extractions for flat logs as well as formatting for the REST input for assets
- Indexers - The add-on contains props.conf configurations for properly ingesting logs for BigFix clients, relays, and server logs. NOTE: Not all available BigFix logs have been added to the TA. As development progresses, more logs will be added to the add-on for proper ingestion.
- Heavy Forwarder - The REST input should be configured on a heavy forwarder to ensure uninterrupted inputs from the BigFix deployment

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

`if windows of operating system then concatenation "|" of (mac addresses of adapters of network) else if not windows of operating system then concatenation "|" of ((mac address of it as string) of ip interfaces whose (not loopback of it AND exists mac address of it) of network) else ""`

One the property is configured in BigFix, you can configure the property name when you configure the input.
