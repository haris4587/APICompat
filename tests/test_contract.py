"""Local tests use explicit VM/web/model doubles; live evidence is separate."""
import unittest,sys,types,json,copy,importlib.util,pathlib
class UserError(Exception):pass
class Return:
    def __init__(self,x):self.calldata=x
class TreeMap:
    def __class_getitem__(cls,x):return dict
class VM:
    UserError=UserError;Return=Return;tamper=None
    def run_nondet_unsafe(self,leader,validator):
        value=leader();proposed=copy.deepcopy(value)
        if self.tamper:proposed.update(self.tamper)
        if not validator(Return(proposed)):raise UserError('consensus rejected')
        return value
vm=VM();message=types.SimpleNamespace(sender_address='owner')
model={'verdict':'COMPATIBLE','quote':'Existing cursor clients work unchanged.','reason':'Preserves behavior; optional input is additive.'}
def prompt(task,**kwargs):return {'supported':True} if task.startswith('Verify this') else copy.deepcopy(model)
def web(url):
    name=url.rsplit('/',1)[-1];body=pathlib.Path('public/evidence',name).read_bytes();return types.SimpleNamespace(status=200,body=body)
gl=types.SimpleNamespace(Contract=object,message=message,vm=vm,public=types.SimpleNamespace(write=lambda f:f,view=lambda f:f),nondet=types.SimpleNamespace(exec_prompt=prompt,web=types.SimpleNamespace(get=web)))
stub=types.ModuleType('genlayer');stub.gl=gl;stub.TreeMap=TreeMap;stub.u256=int;sys.modules['genlayer']=stub
spec=importlib.util.spec_from_file_location('contract','contracts/apicompat.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
fixtures=json.load(open('public/fixtures.json'))
class Tests(unittest.TestCase):
    def setUp(self):
        self.c=m.APICompat();self.c.cases={};self.c.receipts={};message.sender_address='owner';vm.tamper=None;gl.nondet.web.get=web;gl.nondet.exec_prompt=prompt
    def b(self,kind='compatible'):return copy.deepcopy(next(f['bundle'] for f in fixtures if f['id']==kind))
    def create(self,b=None):
        raw=m.canonical(b or self.b());rid=m.digest(raw);self.c.create_review(raw,rid);return rid
    def assess(self,kind='compatible'):
        rid=self.create(self.b(kind));self.c.lock_review(rid);self.c.assess_review(rid);return rid,json.loads(self.c.get_receipt(rid,1))
    def test_compatible(self):self.assertEqual(self.assess()[1]['verdict'],'COMPATIBLE')
    def test_source_verified(self):self.assertTrue(self.assess()[1]['source_verified'])
    def test_structural_breaking(self):self.assertEqual(self.assess('breaking')[1]['verdict'],'BREAKING')
    def test_unsupported(self):self.assertEqual(self.assess('unsupported')[1]['verdict'],'INCONCLUSIVE')
    def test_hash_mismatch(self):
        with self.assertRaises(UserError):self.c.create_review(m.canonical(self.b()),'0'*64)
    def test_duplicate(self):
        self.create()
        with self.assertRaises(UserError):self.create()
    def test_owner_lock(self):
        rid=self.create();message.sender_address='other'
        with self.assertRaises(UserError):self.c.lock_review(rid)
    def test_lock_before_assess(self):
        with self.assertRaises(UserError):self.c.assess_review(self.create())
    def test_double_lock(self):
        rid=self.create();self.c.lock_review(rid)
        with self.assertRaises(UserError):self.c.lock_review(rid)
    def test_conclusive_no_retry(self):
        rid,_=self.assess()
        with self.assertRaises(UserError):self.c.assess_review(rid)
    def test_bounded_retries(self):
        rid,_=self.assess('unsupported');self.c.assess_review(rid);self.c.assess_review(rid)
        with self.assertRaises(UserError):self.c.assess_review(rid)
    def test_independent_challenge(self):
        rid,_=self.assess()
        with self.assertRaises(UserError):self.c.challenge_review(rid,'Please inspect the pagination preservation promise.')
    def test_challenge_and_linked_receipts(self):
        rid,first=self.assess();message.sender_address='challenger';self.c.challenge_review(rid,'Please inspect the pagination preservation promise.');self.c.assess_review(rid);second=json.loads(self.c.get_receipt(rid,2));self.assertEqual(second['previous'],first['receipt_sha256']);h=second.pop('receipt_sha256');self.assertEqual(h,m.digest(m.canonical(second)));self.assertEqual(first,json.loads(self.c.get_receipt(rid,1)))
    def test_only_one_challenge(self):
        rid,_=self.assess();message.sender_address='challenger';self.c.challenge_review(rid,'Please inspect the pagination preservation promise.');self.c.assess_review(rid)
        with self.assertRaises(UserError):self.c.challenge_review(rid,'Please inspect this a second time for the same claim.')
    def test_short_challenge(self):
        rid,_=self.assess();message.sender_address='challenger'
        with self.assertRaises(UserError):self.c.challenge_review(rid,'short')
    def test_missing_review(self):
        with self.assertRaises(UserError):self.c.get_review('missing')
    def test_tampered_verdict(self):
        rid=self.create(self.b('breaking'));self.c.lock_review(rid);vm.tamper={'verdict':'COMPATIBLE'}
        with self.assertRaises(UserError):self.c.assess_review(rid)
    def test_tampered_quote(self):
        rid=self.create();self.c.lock_review(rid);vm.tamper={'quote':'This quotation does not occur anywhere in the artifacts.'}
        with self.assertRaises(UserError):self.c.assess_review(rid)
    def test_invalid_model_quote(self):
        gl.nondet.exec_prompt=lambda *a,**k:{'verdict':'COMPATIBLE','quote':'A fabricated sentence with no supporting evidence.','reason':'bad'}
        self.assertEqual(self.assess()[1]['verdict'],'INCONCLUSIVE')
    def test_model_failure(self):
        def fail(*a,**kw):raise RuntimeError('provider unavailable')
        gl.nondet.exec_prompt=fail;self.assertEqual(self.assess()[1]['verdict'],'INCONCLUSIVE')
    def test_source_digest_mismatch(self):
        b=self.b();b['sources'][0]['sha256']='0'*64;rid=self.create(b);self.c.lock_review(rid);self.c.assess_review(rid);self.assertFalse(json.loads(self.c.get_receipt(rid,1))['source_verified'])
    def test_source_size_mismatch(self):
        b=self.b();b['sources'][0]['bytes']+=1;rid=self.create(b);self.c.lock_review(rid);self.c.assess_review(rid);self.assertEqual(json.loads(self.c.get_receipt(rid,1))['verdict'],'INCONCLUSIVE')
    def test_source_pack_mismatch(self):
        b=self.b();b['notes']+=' Edited.';rid=self.create(b);self.c.lock_review(rid);self.c.assess_review(rid);self.assertEqual(json.loads(self.c.get_receipt(rid,1))['verdict'],'INCONCLUSIVE')
    def test_source_retrieval_failure(self):
        gl.nondet.web.get=lambda u: (_ for _ in ()).throw(RuntimeError());self.assertEqual(self.assess()[1]['verdict'],'INCONCLUSIVE')
    def test_source_allowlist(self):
        for u in ['http://localhost/a','https://example.com/a','https://raw.githubusercontent.com/x/y/main/a','https://raw.githubusercontent.com/x/y/'+'a'*40+'/../a']:
            b=self.b();b['sources'][0]['url']=u
            with self.assertRaises(UserError):self.create(b)
    def test_sources_optional_but_labeled(self):
        b=self.b();b['sources']=[];rid=self.create(b);self.c.lock_review(rid);self.c.assess_review(rid);r=json.loads(self.c.get_receipt(rid,1));self.assertFalse(r['source_verified']);self.assertEqual(r['evidence_scope'],'SUBMITTER_SUPPLIED')
    def test_empty_paths(self):
        with self.assertRaises(UserError):m.structural({'openapi':'3.0.3','paths':{}},{'openapi':'3.0.3','paths':{}})
    def test_removed_operation(self):
        b=self.b();b['candidate']['paths']['/parcels']={};self.assertTrue(m.structural(b['baseline'],b['candidate'])['breaks'])
    def test_removed_response_field(self):
        b=self.b();b['candidate']['paths']['/parcels']['get']['responses']['200']['content']['application/json']['schema']['required']=[];self.assertTrue(m.structural(b['baseline'],b['candidate'])['breaks'])
    def test_unchanged_path_ref_conservative(self):
        b=self.b();b['baseline']['paths']['/parcels']['parameters']=[{'$ref':'#/components/parameters/Foo'}];b['candidate']=copy.deepcopy(b['baseline']);self.assertTrue(m.structural(b['baseline'],b['candidate'])['unsupported'])
    def test_request_enum_narrowing(self):
        b=self.b();b['baseline']['paths']['/parcels']['get']['parameters'][0]['schema']['enum']=['A','B'];b['candidate']['paths']['/parcels']['get']['parameters'][0]['schema']['enum']=['A'];self.assertTrue(m.structural(b['baseline'],b['candidate'])['breaks'])
    def test_response_enum_widening(self):
        b=self.b();a=b['baseline']['paths']['/parcels']['get']['responses']['200']['content']['application/json']['schema']['properties']['next_cursor'];a['enum']=['A'];n=b['candidate']['paths']['/parcels']['get']['responses']['200']['content']['application/json']['schema']['properties']['next_cursor'];n['enum']=['A','B'];self.assertTrue(m.structural(b['baseline'],b['candidate'])['breaks'])
    def test_documentation_named_properties_are_real_fields(self):
        for name in ['description','summary','example','examples','externalDocs','properties']:
            b=self.b();schema=b['baseline']['paths']['/parcels']['get']['responses']['200']['content']['application/json']['schema'];schema['properties'][name]={'type':'string'}
            self.assertTrue(m.structural(b['baseline'],b['candidate'])['breaks'],name)
    def test_description_changes_still_reach_semantic_review(self):
        b=self.b('behavioral');result=m.structural(b['baseline'],b['candidate']);self.assertFalse(result['breaks']);self.assertFalse(result['unsupported'])
    def test_unknown_schema_maps_preserve_documentation_named_data(self):
        b=self.b();schema=b['candidate']['paths']['/parcels']['get']['responses']['200']['content']['application/json']['schema'];schema['dependentSchemas']={'description':{'type':'integer'}}
        self.assertTrue(m.structural(b['baseline'],b['candidate'])['unsupported'])
    def test_enum_object_fields_are_data(self):
        value={'type':'object','enum':[{'description':'A'}]};self.assertEqual(m.clean(value),value)
if __name__=='__main__':unittest.main()
