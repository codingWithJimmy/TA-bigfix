BigFix TA
Created by Jimmy Maple

#############################################
################### Setup ###################
#############################################

This add-on utilizes two input methods. The first being the asset list obtained by polling the BigFix REST API. The setup of the REST API input requires a coordination with the BigFix administrator in your environment.

Things to request from the BigFix administrator

1. A console account with login access via REST API only. No other permissions are needed.
2. The account will need to be subsribed to all hosts that will be brought into the asset list.
3. A property the BigFix administrator knows will detail a list of MAC addresses for each host.

If the BigFix administrator does not have a property available, you can use the following relevance to evaluate what is necessary.

if windows of operating system then (mac addresses of adapters of network) else if not windows of operating system then ((mac address of it as string) of ip interfaces whose (not loopback of it AND exists mac address of it) of network) else ""

#############################################
############## Acknowledgments ##############
#############################################

This section is to thank the many people who attirbuted the development of this TA by providing relevance, log files, development licenses, and other support.

Jason Walker
Geetha Alagppan
Mark "Gunny" Collins
Mark Spryer
Eric Howard
Josh Rice
James Stewart
Aram Eblighatian
Jimmy Glass
Keith Hutchison