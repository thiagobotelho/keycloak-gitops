"""Protege o contrato OIDC e a associação inicial sem administração global."""
from pathlib import Path
import copy
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]


def validate(realm):
    assert realm['registrationAllowed'] is False
    groups = {g['name'] for g in realm['groups']}
    assert {'openshift-viewers', 'openshift-project-admins', 'openshift-cluster-admins'} <= groups
    client = next(c for c in realm['clients'] if c['clientId'] == 'openshift')
    mapper = next(m for m in client['protocolMappers'] if m['protocolMapper'] == 'oidc-group-membership-mapper')
    config = mapper['config']
    assert config['claim.name'] == 'groups' and config['full.path'] == 'false'
    assert config['id.token.claim'] == config['userinfo.token.claim'] == 'true'
    admin = next(u for u in realm['users'] if u['username'] == 'observability-admin')
    assert '/openshift-project-admins' in admin['groups']
    assert {u['username'] for u in realm['users'] if '/openshift-cluster-admins' in u.get('groups', [])} == {'openshift-admin'}


cm = yaml.safe_load((ROOT/'base/keycloak-config-realm.yaml').read_text())
realm = json.loads(cm['data']['observability-realm.json'])
validate(realm)
print('PASS: claim de grupos e associação inicial de projeto')
for name, mutate in [
    ('cadastro público', lambda r: r.update(registrationAllowed=True)),
    ('administração global de conta indevida', lambda r: r['users'][0]['groups'].append('/openshift-cluster-admins')),
    ('nomes com caminho completo', lambda r: next(c for c in r['clients'] if c['clientId'] == 'openshift')['protocolMappers'][0]['config'].update({'full.path': 'true'})),
]:
    bad = copy.deepcopy(realm); mutate(bad)
    try:
        validate(bad)
    except AssertionError:
        print('PASS: rejeitado', name)
    else:
        raise AssertionError(name)
