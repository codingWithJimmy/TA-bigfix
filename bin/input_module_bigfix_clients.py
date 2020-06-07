
# encoding = utf-8

import os
import sys
import time
import datetime
import base64
import json

def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # root_url = definition.parameters.get('root_url', None)
    # rest_api_port = definition.parameters.get('rest_api_port', None)
    # mac_address_property = definition.parameters.get('mac_address_property', None)
    # global_account = definition.parameters.get('global_account', None)
    pass

def collect_events(helper, ew):
    opt_root_url = helper.get_global_setting('bigfix_server_url')
    sourcee= helper.get_input_stanza_names()
    opt_rest_api_port = helper.get_global_setting('bigfix_server_port')
    opt_mac = helper.get_arg('mac_address_property')
    opt_sets = helper.get_arg('set_batch_value')
    int_sets = int(opt_sets)
    opt_global_account = helper.get_arg('global_account')
    opt_global_timeout = helper.get_global_setting('query_timeout_seconds')
    int_global_timeout = int(opt_global_timeout)
    account = opt_global_account["username"] + ":" + opt_global_account["password"]
    base64string = base64.b64encode(account.encode()).decode()
    headers = { 'Authorization' : 'Basic %s' % base64string }

    opt_url_start=opt_root_url + ":" + opt_rest_api_port + "/api/query?output=json&relevance="
    
    query='("nt_host=" %26 (name of item 0 of it | "missing Name") ,"client_id=" %26 id of item 0 of it as string, "last_report_time=" %26 concatenation "|" of values of results (item 0 of it , elements of item 1 of it) ,"ip=" %26 (if (size of item 3 of it = 1) then (concatenation "|" of values whose (it as string does not start with "169.254") of results (item 0 of it , elements of item 3 of it)) else (if (size of item 3 of it > 1) then (("IP Address property duplicates: " %26 concatenation "|" of ((name of it) %26 "=" %26 (id of it as string)) of elements of item 3 of it) as string) else (""))) , "mac=" %26 (concatenation "|" of values of results (item 0 of it , elements of item 4 of it) |"") ,"dns=" %26 (if (size of item 5 of it = 1) then ((if it = "" then "" else it) of concatenation "|" of values of results (item 0 of it , elements of item 5 of it)) else (if (size of item 5 of it > 1) then (("Property 3 duplicates: " %26 concatenation "|" of ((name of it) %26 "=" %26 (id of it as string)) of elements of item 5 of it) as string) else (""))) , "operating_system=" %26 concatenation "|" of values of results (item 0 of it , elements of item 6 of it) , ("user=" %26 concatenation "|" of values of results (item 0 of it , elements of item 7 of it)) , ("client_version=" %26 (value of result (item 0 of it , elements of item 8 of it))) , "subscribed_sites=" %26 concatenation "|" of display names of subscribed sites whose (custom site flag of it OR external site flag of it) of item 0 of it) of (elements of item 0 of it , item 1 of it , item 2 of it , item 3 of it , item 4 of it , item 5 of it , item 6 of it , item 7 of it, item 8 of it) of (set of BES computers whose (id of it mod SETS = RESULT), set of bes properties whose (name of it as lowercase = ("Last Report Time") as lowercase) , set of bes properties whose (reserved flag of it AND name of it as lowercase = ("id")) , set of bes properties whose (reserved flag of it and name of it as lowercase = ("ip address")) , (set of bes properties whose (name of it as lowercase = ("MACFIELD") as lowercase)) , set of bes properties whose (reserved flag of it and name of it as lowercase = ("dns name")) , set of bes properties whose (reserved flag of it and name of it as lowercase = ("os")) , (set of bes properties whose (name of it as lowercase = ("user name"))) , set of bes properties whose (reserved flag of it AND name of it as lowercase = ("agent version"))) '.replace("SETS", opt_sets).replace("MACFIELD",opt_mac)
    
    urlb=opt_url_start + query

    helper.log_info("Beginning job="+sourcee)

    for x in range(0, int_sets):
        strx=str(x)
        helper.log_info("job="+sourcee+" Beginning MOD loop="+strx)

        url=urlb.replace("RESULT", strx)
        for y in range(0, 100):
            try:
                response = helper.send_http_request(url, 'GET', parameters=None, payload=None, headers=headers, cookies=None, verify=False, cert=None, timeout=int_global_timeout, use_proxy=False)
            except Exception as e:
                helper.log_error("job="+sourcee+" Error Response for loop="+str(x)+" error="+str(e))
                if y == 99:
                    helper.log_error("job="+sourcee+" Total Failure. Exiting")
                    return
                helper.log_error("job="+sourcee+" Sleeping for 1 minute and retry="+str(y))
                time.sleep(30)
                continue
            if response.status_code==200:
                break
            helper.log_error("job="+sourcee+" Response for MOD loop="+str(x)+" code="+str(response.status_code))
            if y == 99:
                helper.log_error("job="+sourcee+" Total Failure. Exiting " + response.text )
                return 
            helper.log_error("job="+sourcee+" Sleeping for 1 minute and retry="+str(y))
            time.sleep(30)
        helper.log_info("job="+sourcee+" Response for MOD loop="+str(x)+" code="+str(response.status_code))

        r_text = response.json()
        helper.log_info("job="+sourcee+" Begin Event Processing for MOD loop="+str(x))
        helper.log_info("job="+sourcee+" JSON item count="+str(len(r_text['result']))+" for MOD loop="+str(x))
        for item in r_text['result']:
            eventitem=""
            s=sourcee+strx
            space=", \""
            output=[]
            for value in item:
                output.append(value.replace("=","\": \"",1)+"\"")
            eventitem=space.join(output)
            j_convert="{ \"" + eventitem + " }"
            event = helper.new_event(source=s, index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=j_convert)
            ew.write_event(event)
        helper.log_info("job="+sourcee+" Ending MOD loop="+str(x))
    helper.log_info("Ending job="+sourcee)

