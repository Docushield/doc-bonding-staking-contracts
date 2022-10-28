
from kadena_sdk.kadena_sdk import KadenaSdk
from kadena_sdk.key_pair import KeyPair
import json

# Code to run


MAINNET = {
  'base_url': 'https://api.chainweb.com',
  'network_id': 'mainnet01',
  'chain_id': '8',
}
TESTNET = {
  'base_url': 'https://api.testnet.chainweb.com',
  'network_id': 'testnet04',
  'chain_id': '1',
}
NETWORK = TESTNET

key_pair = KeyPair('keys.json')
sdk = KadenaSdk(key_pair, 
  NETWORK['base_url'], 
  NETWORK['network_id'], 
  NETWORK['chain_id'])

PACT_CODE = '''
[
(free.marmalade-nft-staking.set-pool-bonus "test-locked" 5.0)
(free.marmalade-nft-staking.set-pool-bonus "test-unlocked" 0.0)
]
'''
# f'''
# (namespace "free")
# (module test-keyset-gov GOV
#   (defcap GOV ()
#     (enforce-guard (read-keyset "gov"))
#   )

#   (defun hello:string (input:string)
#     (format "hello {{}}!" [input])
#   )
# )
# '''
# f'''
# (marmalade.ledger.transfer-create 
# "swag-token" 
# "k:{key_pair.get_pub_key()}" 
# "k:aeecd476ad8a4842ec84f3fbdad39b73fe7329fb4feaa3ea4367314a29a7e42b"
# (read-keyset "to-keyset")
# 100.0)
# '''

payload = {
  "exec": {
    "data": {
      "gov": { "keys": [key_pair.get_pub_key()], "pred": "keys-all"},
      "to-keyset": { "keys": ["aeecd476ad8a4842ec84f3fbdad39b73fe7329fb4feaa3ea4367314a29a7e42b"], "pred": "keys-all" }
    },
    "code": PACT_CODE,
  }
}
signers = [
  {
    "pubKey": key_pair.get_pub_key(),
    "clist": [
      {
        "name": f"free.marmalade-nft-staking.OPS",
        "args": []
      },
      {
        "name": "coin.GAS",
        "args": []
      },
    ],
  }
]

print()
cmd = sdk.build_command(f'k:{key_pair.get_pub_key()}', payload, signers)
# result = sdk.local(cmd)
result = sdk.send_and_listen(cmd)
print(result.text)

# jason = json.dumps(cmd)
# print(jason)
# print(json.loads(jason))

print()