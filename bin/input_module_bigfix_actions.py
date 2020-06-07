
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
    opt_global_timeout = helper.get_global_setting('query_timeout_seconds')
    int_global_timeout = int(opt_global_timeout)
    opt_mac = helper.get_arg('mac_address_property')
    opt_sets = helper.get_arg('set_batch_value')
    int_sets = int(opt_sets)
    opt_global_account = helper.get_arg('global_account')
    account = opt_global_account["username"] + ":" + opt_global_account["password"]
    base64string = base64.b64encode(account.encode()).decode()
    headers = { 'Authorization' : 'Basic %s' % base64string }

    opt_url_start=opt_root_url + ":" + opt_rest_api_port + "/api/query?output=json&relevance="

    query='%28%22nt_host%3D%22+%26+item+0+of+it%2C+%22client_id%3D%22+%26+item+12+of+it%2C+%22status%3D%22+%26+item+1+of+it%2C+%22issuer%3D%22+%26+item+2+of+it%2C+%22issue_time%3D%22+%26+item+3+of+it%2C+%22end_time%3D%22+%26+item+4+of+it%2C+%22start_time%3D%22+%26+item+5+of+it%2C+%22action_id%3D%22+%26+item+6+of+it%2C+%22action_name%3D%22+%26+item+7+of+it%2C+%22reapply%3D%22+%26+item+8+of+it%2C+%22restart_required%3D%22+%26+item+9+of+it%2C+%22stopper%3D%22+%26+item+10+of+it%2C+%22time_stopped%3D%22+%26+item+11+of+it%29+of+%28name+of+computers+of+item+0+of+it+as+string%2C+status+of+item+0+of+it+as+string%2C+name+of+issuer+of+item+1+of+it+as+string%2C+time+issued+of+item+1+of+it+as+string%2C+%28if+%28exists+end+date+of+item+1+of+it%29+then+end+date+of+item+1+of+it+as+string+%26+%22+%22+%26+end+time_of_day+of+item+1+of+it+as+string+else+%22%22%29%2C+%28if+%28exists+start+date+of+item+1+of+it%29+then+start+date+of+item+1+of+it+as+string+%26+%22+%22+%26+start+time_of_day+of+item+1+of+it+as+string+else+%22%22%29%2C+id+of+item+1+of+it+as+string%2C+%28concatenation+%22%252527%22+of+%28substrings+separated+by+%22%252522%22+of+name+of+item+1+of+it+as+string%29%29%2C+reapply+flag+of+item+1+of+it+as+string%2C+restart+flag+of+item+1+of+it+as+string%2C+%28if+%28exists+stopper+of+item+1+of+it%29+then+name+of+stopper+of+item+1+of+it+as+string+else+%22%22%29%2C+%28if+%28exists+time+stopped+of+item+1+of+it%29+then+time+stopped+of+item+1+of+it+as+string+else+%22%22%29%2C+%28id+of+computers+of+item+0+of+it+as+string%29%29+of+%28results+of+it%2C+it%29+of+%28bes+actions+whose+%28id+of+computers+of+results+of+it+mod+SETS%3DRESULT%29%29'.replace("SETS", opt_sets)

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
