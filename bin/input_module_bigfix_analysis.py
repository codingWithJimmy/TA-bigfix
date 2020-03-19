
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
    opt_analysis_id = helper.get_arg('analysis_id')
    opt_analysis_site_name = helper.get_arg('site_name')
    opt_sets = helper.get_arg('set_batch_value')
    int_sets = int(opt_sets)
    opt_global_account = helper.get_arg('global_account')
    base64string = base64.encodestring('%s:%s' % (opt_global_account["username"], opt_global_account["password"])).strip()
    headers = { 'Authorization' : 'Basic %s' % base64.b64encode(opt_global_account["username"]+":"+opt_global_account["password"]) }

    opt_url_start=opt_root_url + ":" + opt_rest_api_port + "/api/query?output=json&relevance="

    query='(%22analysis_id%3D%22+%2526+item+2+of+it+as+string%2C+%22analysis_name%3D%22+%2526+item+1+of+it%2C+%22property_name%3D%22+%2526+item+1+of+item+0+of+it%2C%22property_value%3D%22+%2526+item+0+of+item+0+of+item+0+of+it%2C+%22nt_host%3D%22+%2526+item+1+of+item+0+of+item+0+of+it%2C+%22client_id%3D%22+%2526+item+2+of+item+0+of+item+0+of+it+as+string%2C+%22site_name%3D%22+%2526+item+3+of+it)+of+((((values+of+it%2C+names+of+computer+of+it%2C+id+of+computer+of+it)+of+results+whose+(id+of+computer of+it+mod+SETS+%3D+RESULT)+of+it%2C+name+of+it)+of+properties+of+it)+of+it%2C+name+of+it%2C+id+of+it%2C+name+of+site+of+it)+of+bes+analysis+whose+((id+of+it+is+ANALYSISID)+AND+(name+of+site+of+it+is+%22SITENAME%22))'.replace("SETS", opt_sets).replace("ANALYSISID",opt_analysis_id).replace("SITENAME",opt_analysis_site_name)
    
    urlb=opt_url_start + query

    helper.log_info("Beginning job="+sourcee)

    for x in range(0, int_sets):
        strx=str(x)
        helper.log_info("job="+sourcee+" Beginning MOD loop="+strx)

        url=urlb.replace("RESULT", strx)
        for y in range(0, 100):
            try:
                response = helper.send_http_request(url, 'GET', parameters=None, payload=None, headers=headers, cookies=None, verify=False, cert=None, timeout=60, use_proxy=False)
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

