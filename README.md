# BigFix TA
The BigFix TA can be used to configure Splunk to ingest BigFix client, relay, and server logs. It also contains multiple modular inputs to query the REST API of a BigFix core server.

# Compatability
The BigFix TA was developed and tested using **Splunk Enterprise 7.3.x** using the **Splunk Add-on Builder 2.2.0**. It is currently still using Python 2.7 for the modular inputs so they may **not** fully work on **Splunk Enterprise 8.0+**. I recommend installing the add-on to collect modular inputs on **Splunk Enterprise 7.x**.

# Installation
The BigFix TA should be installed on:

- Search Heads - The add-on contains field extractions for flat logs as well as formatting for the REST input for assets
- Indexers - The add-on contains props.conf and transforms.conf configurations for properly ingesting logs for BigFix clients, relays, and server logs. NOTE: Not all available BigFix logs have been added to the TA. As development progresses, more logs will be added to the add-on for proper ingestion.
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
The improve the scalability of the BigFix TA, the inputs have been rewritten to allow for batch-adding the data. This is done by looping through based on modulation of a specific integer of the results of the relevance query. It basically increments and brings in different results based on however many batches you're looking to run the ingestion on.

The right modulous depends on the size of the environment. Lower client counts means less cardinality of events where you are less likely to have over 100,000 results for a single query using the inputs. As the number of results begins to exponentially grow, your modulous should grow as well. I would recommend that for every 10,000 potential results you have, you increase your modulous by 10.

This means if you are collecting BigFix Action results and an action has gone out to 10,000 machines, your modulous input should use be a batch of **10**. Feel free to experiment and I encourage anyone who knows maths way better than me to report back with what would be a good ratio.

# BigFix Clients Input
The BigFix TA contains a configurable REST input for collecting client information from a BigFix deployment. The REST query should return results, even from environments with a large number of clients, in a reasonable amount of time. This requires the coordination with the administrator of BigFix because the field containing the MAC address is not a default property inside of an out-of-the-box BigFix deployment.

Some notes on further requirements for this input:
- A property the BigFix administrator knows will need to be identified which details a list of MAC addresses for each host. This property will need to be configured with the input. If there is a not a currently configured property, the BigFix administrator may use the relevance below to evaluate the property.
- The account used to perform the query will need permission to, at least, read the site that contains the property for the MAC address if it's not contained within the Master Action Site.
- The query relies on results from analysis within the "BES Support" site. The user account will need to be assigned to the site to view those results.

If the MAC addresses of the clients are not being evaluated, you can use the following relevance to collect the MAC addresses of most systems that BigFix supports

```if windows of operating system then concatenation "|" of (mac addresses of adapters of network) else if not windows of operating system then concatenation "|" of ((mac address of it as string) of ip interfaces whose (not loopback of it AND exists mac address of it) of network) else ""```

Once the property is configured in BigFix, you can configure the property name when you configure the input.

# BigFix Analysis Input
The BigFix TA contains a configurable REST input for ingesting the results of a specificed analysis within BigFix. This will require the display name of the analysis being imported. Once congfigured, the results are ingested per property result per host in a single event so multiple properties within a single analysis can be identified and evaluated once the events are ingested. This will also break multi-value results into their own events with the same property name.

To configure a specific analysis for ingestion, your BigFix administrator will need to provide the integer ID of the analysis as well as the site that analysis exists under. Once you configure those values, your analysis will be ingested.

Another consideration when configuring this input is how often the analysis property is updated. If any analysis property is normally only evaluated on the endpoints once a day, the interval for the ingestion of that analysis should be no less than "86400" (24 hours in seconds). Consult your BigFix administrator for evaluation times of analysis that you want to import to ensure your ingestion interval is as long or longer than the analysis interval.

# Acknowledgements

This section is to thank the many people who contributed to the development of this TA by providing relevance, log files, development licenses, larger environments, and other support.

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
