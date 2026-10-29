#!/usr/bin/env python3
"""Initialize missing lab passwords on CRC; never overwrite an existing password."""
import argparse,base64,json,resource,ssl,subprocess,sys,urllib.request,urllib.parse,urllib.error
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--initialize-missing',action='store_true');args=parser.parse_args()
OC=['oc','--request-timeout=20s'];URL='https://keycloak-dev.apps-crc.testing';token=None
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):raise RuntimeError('Unexpected redirect')
def secret(ns,name):
 p=subprocess.run(OC+['get','secret/'+name,'-n',ns,'-o','json'],capture_output=True,text=True,timeout=30)
 if p.returncode:raise RuntimeError('Required CRC Secret unavailable')
 return json.loads(p.stdout)['data']
def request(path,method='GET',data=None,form=False):
 body=(urllib.parse.urlencode(data).encode() if form else json.dumps(data).encode()) if data is not None else None
 headers={'Content-Type':'application/x-www-form-urlencoded' if form else 'application/json'}
 if token:headers['Authorization']='Bearer '+token
 try:
  with op.open(urllib.request.Request(URL+path,data=body,headers=headers,method=method),timeout=20) as response:
   b=response.read();return json.loads(b) if b else None
 except urllib.error.HTTPError as e:raise RuntimeError('Keycloak HTTP '+str(e.code)) from None
try:
 ca=base64.b64decode(secret('openshift-ingress-operator','router-ca')['tls.crt']).decode()
 op=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPSHandler(context=ssl.create_default_context(cadata=ca)),NoRedirect())
 admin=secret('keycloak-dev','keycloak-dev-initial-admin');form={'grant_type':'password','client_id':'admin-cli','username':base64.b64decode(admin['username']).decode(),'password':base64.b64decode(admin['password']).decode()}
 try:token=request('/realms/master/protocol/openid-connect/token','POST',form,form=True)['access_token']
 finally:admin.clear();form.clear()
 root='/admin/realms/observability';missing=[]
 for username,key in [('grafana-admin','GRAFANA_ADMIN_PASSWORD'),('zabbix-admin','ZABBIX_ADMIN_PASSWORD'),('observability-admin','OBSERVABILITY_ADMIN_PASSWORD'),('openshift-admin','OPENSHIFT_ADMIN_PASSWORD')]:
  users=request(root+'/users?'+urllib.parse.urlencode({'username':username,'exact':'true'}))
  if len(users)!=1:raise RuntimeError('Expected lab user missing or ambiguous')
  user=users[0];has_password=any(x['type']=='password' for x in request(root+'/users/'+user['id']+'/credentials'))
  if has_password:print(username+': existing password preserved');continue
  if not args.initialize_missing:missing.append(username);continue
  seeds=secret('keycloak-dev','keycloak-openshift-users' if username=='openshift-admin' else 'keycloak-observability-users');payload={'type':'password','temporary':False,'value':base64.b64decode(seeds[key]).decode()}
  try:request(root+'/users/'+user['id']+'/reset-password','PUT',payload)
  finally:seeds.clear();payload.clear()
  print(username+': missing initial password initialized without displaying value')
 token=None
 if missing:raise RuntimeError('Missing initial passwords; rerun with --initialize-missing after reviewing bootstrap intent')
 print('PASS: lab credentials initialized or preserved; TLS verified')
except Exception as e:
 token=None;print('FAIL: '+(str(e) if isinstance(e,RuntimeError) else type(e).__name__),file=sys.stderr);sys.exit(1)
