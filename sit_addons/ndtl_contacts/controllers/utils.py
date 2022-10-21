from datetime import datetime, date, timedelta

def validate_request(request):
    ''' Valid request header
        params:
            request: objects odoo.http.request
        output:
            err,msg
    '''
    headers = request.httprequest.environ
    if not headers.get('HTTP_AUTHORIZATION'):
        return True,responseMessage(1,'Authorization header missing',None)
    valid_auth_header = headers.get('HTTP_AUTHORIZATION').startswith('Bearer ')
    if not valid_auth_header:
        return True,responseMessage(1,'Authorization header format wrong!!',None)
    if request.uid is None:
        return True,responseMessage(1,'Access Denined!!',None)
    return None,False

def responseMessage(code,msg,data):
    ''' Response Message follow ndtl's format 
        params:
            code : integer error code
            msg:   string error message
            data:   object  data return
        output:
            JSON objects
    '''
    return {
        'error_code': code,
        'error_msg': msg,
        'data':data,
        'create_at':datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    }