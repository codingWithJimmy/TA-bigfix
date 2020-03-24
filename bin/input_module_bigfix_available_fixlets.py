
# encoding = utf-8

import os
import sys
import time
import datetime
import base64
import re

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''

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
    opt_global_account = helper.get_arg('global_account')
    opt_global_timeout = helper.get_global_setting('query_timeout_seconds')
    opt_sets = helper.get_arg('set_batch_value')
    int_sets = int(opt_sets)
    TAG_RE = re.compile(r'<[^>]+>')
    #key=sourcee
    #helper.delete_check_point(key)
    #check=helper.get_check_point(key) 
    #from datetime import datetime, timedelta
    #nextcheck=datetime.now().strftime('%a, %d %b %Y %H:%M:%S -0000')
    #yesterday=datetime.now() - timedelta(1)
    #yesterday=yesterday.strftime('%a, %d %b %Y %H:%M:%S -0000')
    #if check is None:
    #    check=yesterday
    #    helper.log_info("job="+sourcee+" no checkpoint, using yesterday checkpoint=\""+check+"\"")
    #helper.log_info("job="+sourcee+" checkpoint=\""+check+"\" nextcheckpoint=\""+nextcheck+"\"")
    base64string = base64.encodestring('%s:%s' % (opt_global_account["username"], opt_global_account["password"])).strip()
    headers = { 'Authorization' : 'Basic %s' % base64.b64encode(opt_global_account["username"]+":"+opt_global_account["password"]) }
    #header= { 
    #    "Content-type: application/json", 
    #    "Accept: application/json"
    #    }
    
    opt_url_start=opt_root_url + ":" + opt_rest_api_port + "/api/query?output=json&relevance="

    
    query='%28%22fixlet_id%3D%22+%26+item+0+of+it%2C+%22fixlet_name%3D%22+%26+item+1+of+it%2C+%22fixlet_severity%3D%22+%26+item+2+of+it%2C+%22fixlet_source%3D%22+%26+item+7+of+it%2C+%22fixlet_type%3D%22+%26+item+8+of+it+as+string%2C+%22site_name%3D%22+%26+item+3+of+it%2C+%22source_category%3D%22+%26+item+4+of+it%2C+%22source_release_date%3D%22+%26+item+5+of+it%2C+%22source_id%3D%22+%26+item+6+of+it%29+of+%28item+0+of+it+as+string%2C+item+1+of+it+as+string%2C+item+2+of+it+as+string%2C+item+3+of+it+as+string%2C+item+4+of+it+as+string%2C+item+5+of+it+as+string%2C+item+6+of+it+as+string%2C+item+7+of+it+as+string%2C+item+8+of+it+as+string%29+of+%28id+of+it%2C+name+of+it%2C+%28if+exists+source+severity+of+it+then+source+severity+of+it+else+%22N%252FA%22%29%2C+name+of+site+of+it%2C+%28if+exists+category+of+it+then+category+of+it+else+%22N%252FA%22%29%2C+%28if+exists+source+release+date+of+it+then+source+release+date+of+it+as+string+else+%22N%252FA%22%29%2C+%28if+exists+source+id+of+it+then+source+id+of+it+as+string+else+%22N%252FA%22%29%2C+%28if+exists+source+of+it+then+source+of+it+else+%22N%252FA%22%29%2Ctype+of+it%29+of+fixlets+whose+%28id+of+it+mod+SETS+%3D+RESULT%29+of+all+bes+sites'.replace("SETS", opt_sets)
    
    
    #("client_id=" %26 item 0 of it as string, "fixlet_id=" %26 item 0 of item 2 of it as string, "site_name=" %26 item 1 of item 2 of it as string, "last_report_time=" %26 item 1 of it) of (id of it, last report time of it as string, (id of it, name of site of it) of relevant fixlets of it) of bes computers whose ((id of it mod SETS = RESULT))'.replace("SETS", opt_sets)#.replace("CHECKPOINT", check)
    urlb=opt_url_start + query

    helper.log_info("Beginning job="+sourcee)

    for x in range(0, int_sets):
        strx=str(x)
        helper.log_info("job="+sourcee+" Beginning MOD loop="+strx)

        url=urlb.replace("RESULT", strx)
        for y in range(0, 100):
            try:
                response = helper.send_http_request(url, 'GET', parameters=None, payload=None, headers=headers, cookies=None, verify=False, cert=None, timeout=int(opt_global_timeout), use_proxy=False)
                 #response.raise_for_status()
            except Exception, e:
                #response.raise_for_status()
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
    #helper.log_info("Writing Checkpoint checkpoint=\""+nextcheck+"\"")
    #helper.save_check_point(key, nextcheck)
    helper.log_info("Ending job="+sourcee)

    #import random
    #data = str(random.randint(0,100))
   # event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=r_text)
    #ew.write_event(event)
    """Implement your data collection logic here

    # The following examples get the arguments of this input.
    # Note, for single instance mod input, args will be returned as a dict.
    # For multi instance mod input, args will be returned as a single value.
    opt_root_url = helper.get_arg('root_url')
    opt_rest_api_port = helper.get_arg('rest_api_port')
    opt_mac_address_property = helper.get_arg('mac_address_property')
    opt_global_account = helper.get_arg('global_account')
    # In single instance mode, to get arguments of a particular input, use
    opt_root_url = helper.get_arg('root_url', stanza_name)
    opt_rest_api_port = helper.get_arg('rest_api_port', stanza_name)
    opt_mac_address_property = helper.get_arg('mac_address_property', stanza_name)
    opt_global_account = helper.get_arg('global_account', stanza_name)

    # get input type
    helper.get_input_type()

    # The following examples get input stanzas.
    # get all detailed input stanzas
    helper.get_input_stanza()
    # get specific input stanza with stanza name
    helper.get_input_stanza(stanza_name)
    # get all stanza names
    helper.get_input_stanza_names()

    # The following examples get options from setup page configuration.
    # get the loglevel from the setup page
    loglevel = helper.get_log_level()
    # get proxy setting configuration
    proxy_settings = helper.get_proxy()
    # get account credentials as dictionary
    account = helper.get_user_credential_by_username("username")
    account = helper.get_user_credential_by_id("account id")
    # get global variable configuration
    global_userdefined_global_var = helper.get_global_setting("userdefined_global_var")

    # The following examples show usage of logging related helper functions.
    # write to the log for this modular input using configured global log level or INFO as default
    helper.log("log message")
    # write to the log using specified log level
    helper.log_debug("log message")
    helper.log_info("log message")
    helper.log_warning("log message")
    helper.log_error("log message")
    helper.log_critical("log message")
    # set the log level for this modular input
    # (log_level can be "debug", "info", "warning", "error" or "critical", case insensitive)
    helper.set_log_level(log_level)

    # The following examples send rest requests to some endpoint.
    response = helper.send_http_request(url, method, parameters=None, payload=None,
                                        headers=None, cookies=None, verify=True, cert=None,
                                        timeout=None, use_proxy=True)
    # get the response headers
    r_headers = response.headers
    # get the response body as text
    r_text = response.text
    # get response body as json. If the body text is not a json string, raise a ValueError
    r_json = response.json()
    # get response cookies
    r_cookies = response.cookies
    # get redirect history
    historical_responses = response.history
    # get response status code
    r_status = response.status_code
    # check the response status, if the status is not sucessful, raise requests.HTTPError
    response.raise_for_status()

    # The following examples show usage of check pointing related helper functions.
    # save checkpoint
    helper.save_check_point(key, state)
    # delete checkpoint
    helper.delete_check_point(key)
    # get checkpoint
    state = helper.get_check_point(key)

    # To create a splunk event
    helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
    """

    '''
    # The following example writes a random number as an event. (Multi Instance Mode)
    # Use this code template by default.
    import random
    data = str(random.randint(0,100))
    event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=data)
    ew.write_event(event)
    '''

    '''
    # The following example writes a random number as an event for each input config. (Single Instance Mode)
    # For advanced users, if you want to create single instance mod input, please use this code template.
    # Also, you need to uncomment use_single_instance_mode() above.
    import random
    input_type = helper.get_input_type()
    for stanza_name in helper.get_input_stanza_names():
        data = str(random.randint(0,100))
        event = helper.new_event(source=input_type, index=helper.get_output_index(stanza_name), sourcetype=helper.get_sourcetype(stanza_name), data=data)
        ew.write_event(event)
    '''
