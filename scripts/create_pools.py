
from kadena_sdk.kadena_sdk import KadenaSdk
from kadena_sdk.key_pair import KeyPair

# Code to run
PACT_CODE = '''
(free.marmalade-nft-bonding.create-bonded-nft
  "test"
  "swag-token"
  coin
  100.0
  (time "2022-12-25T00:00:00Z")
)
(free.marmalade-nft-staking.create-unlocked-nft-pool
  "test-unlocked"
  "swag-token"
  coin
  0.5
  100.0
  (time "2022-10-31T00:00:00Z")
)
(free.marmalade-nft-staking.create-locked-nft-pool
  "test-locked"
  "swag-token"
  coin
  0.5
  100.0
  (time "2022-10-31T00:00:00Z")
  5184000.0 ;; 60 days of lock time
  2.0
)
'''

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

payload = {
  "exec": {
    "data": {
      "nft-staker-admin": { "keys": [key_pair.get_pub_key()], "pred": "keys-all"}
    },
    "code": PACT_CODE,
  }
}
signers = [
  {
    "pubKey": key_pair.get_pub_key(),
    "clist": [
      {
        "name": f"free.marmalade-nft-bonding.OPS",
        "args": []
      },
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

print()