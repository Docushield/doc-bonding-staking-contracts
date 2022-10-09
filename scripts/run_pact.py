
from kadena_sdk.kadena_sdk import KadenaSdk
from kadena_sdk.key_pair import KeyPair
import json

# Code to run


MAINNET = {
  'base_url': 'https://api.chainweb.com',
  'network_id': 'mainnet01',
  'chain_id': '1',
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

PACT_CODE = f'''(marmalade.ledger.transfer-create 
"swag-token" 
"k:{key_pair.get_pub_key()}" 
"k:aeecd476ad8a4842ec84f3fbdad39b73fe7329fb4feaa3ea4367314a29a7e42b"
(read-keyset "to-keyset")
100.0)
'''

payload = {
  "exec": {
    "data": {
      "nft-staker-admin": { "keys": [key_pair.get_pub_key()], "pred": "keys-all"},
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
        "name": 'marmalade.ledger.TRANSFER',
        "args": ["swag-token", f"k:{key_pair.get_pub_key()}", "k:aeecd476ad8a4842ec84f3fbdad39b73fe7329fb4feaa3ea4367314a29a7e42b", 100.0]
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
cmd = {
      "cmd": "{\"networkId\":\"testnet04\",\"payload\":{\"exec\":{\"data\":{\"ks\":{\"keys\":[\"aeecd476ad8a4842ec84f3fbdad39b73fe7329fb4feaa3ea4367314a29a7e42b\"],\"pred\":\"keys-all\"}},\"code\":\"(free.marmalade-nft-staking.stake \\\"test-locked\\\" \\\"k:aeecd476ad8a4842ec84f3fbdad39b73fe7329fb4feaa3ea4367314a29a7e42b\\\" 5.0 (read-keyset \\\"ks\\\"))\"}},\"signers\":[{\"clist\":[{\"name\":\"marmalade.ledger.TRANSFER\",\"args\":[\"k:aeecd476ad8a4842ec84f3fbdad39b73fe7329fb4feaa3ea4367314a29a7e42b\",\"u:free.marmalade-nft-staking.require-WITHDRAW:y3ypWBoBlBCAGDEg9pv_vsMEFeMGfqEv0pfWV-Nner0\",5]},{\"name\":\"free.marmalade-nft-staking.STAKE\",\"args\":[\"test-locked\",\"k:aeecd476ad8a4842ec84f3fbdad39b73fe7329fb4feaa3ea4367314a29a7e42b\",5]}],\"pubKey\":\"aeecd476ad8a4842ec84f3fbdad39b73fe7329fb4feaa3ea4367314a29a7e42b\"}],\"meta\":{\"creationTime\":1665287450,\"ttl\":600,\"gasLimit\":15000,\"chainId\":\"1\",\"gasPrice\":0.00001,\"sender\":\"k:aeecd476ad8a4842ec84f3fbdad39b73fe7329fb4feaa3ea4367314a29a7e42b\"},\"nonce\":\"\\\"\\\\\\\"2022-10-09T03:52:20.828Z\\\\\\\"\\\"\"}",
      "hash": "nLGnoHqy4nV9CpIgDQm6r9Oy3oCUNqyEunsgxsRk2Og",
      "sigs": [
          {
              "sig": "e13580bb7c777f157fc760cd65973659bd12cd17275f70def3607df9eaf8b8cb02f90acc20c812cdbac52cf724341e9b95b3ff77c41f6337454308be07f08007"
          }
      ]
  }
result = sdk.send_and_listen(cmd)
print(result.text)

# jason = json.dumps(cmd)
# print(jason)
# print(json.loads(jason))

print()