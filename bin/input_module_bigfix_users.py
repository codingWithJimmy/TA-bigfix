
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
    # global_account = definition.parameters.get('global_account', None)
    pass
    
def collect_events(helper, ew):
    opt_root_url = helper.get_global_setting('bigfix_server_url')
    sourcee= helper.get_input_stanza_names()
    opt_rest_api_port = helper.get_global_setting('bigfix_server_port')
    opt_global_account = helper.get_arg('global_account')
    opt_global_timeout = helper.get_global_setting('query_timeout_seconds')
    int_global_timeout = int(opt_global_timeout)
    opt_sets = 1
    int_sets = int(opt_sets)
    base64string = base64.encodestring('%s:%s' % (opt_global_account["username"], opt_global_account["password"])).strip()
    headers = { 'Authorization' : 'Basic %s' % base64.b64encode(opt_global_account["username"]+":"+opt_global_account["password"]) }

    opt_url_start=opt_root_url + ":" + opt_rest_api_port + "/api/query?output=json&relevance="

    query='(%22name%3D%22+%26+name+of+it%2C+%22master_operator%3D%22+%26+master+flag+of+it+as+string%2C+%22action_count%3D%22+%26+number+of+issued+actions+of+it+as+string%2C+%22creation_time%3D%22+%26+creation+time+of+it+as+string%2C+%22last_login_time%3D%22+%26+(if+(exists+last+login+time+of+it)+then+last+login+time+of+it+as+string+else+%22%22))+of+bes+users'
    
    urlb=opt_url_start + query

    helper.log_info("Beginning job="+sourcee)

    for x in range(0, int_sets):
        strx=str(x)
        helper.log_info("job="+sourcee+" Beginning MOD loop="+strx)

        url=urlb.replace("RESULT", strx)
        for y in range(0, 100):
            try:
                response = helper.send_http_request(url, 'GET', parameters=None, payload=None, headers=headers, cookies=None, verify=False, cert=None, timeout=int_global_timeout, use_proxy=False)
            except Exception, e:
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

