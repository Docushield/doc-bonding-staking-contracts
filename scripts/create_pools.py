
from kadena_sdk.kadena_sdk import KadenaSdk
from kadena_sdk.key_pair import KeyPair

CONTRACT_NAME_BONDING = 'free.marmalade-nft-bonding'
CONTRACT_NAME_STAKING = 'free.marmalade-nft-staking'
BONDING_POOL_NAME = 'test'
UNLOCKED_POOL_NAME = 'test-unlocked'
LOCKED_POOL_NAME = 'test-locked'
TOKEN_ID = 'swag-token'
PAYOUT_COIN = 'coin'
APY = '0.5'
BOND_VALUE = '100.0'
START_TIME = '2022-10-31T00:00:00Z'
MATURE_TIME = '2022-12-25T00:00:00Z'
LOCK_TIME_SECONDS = '5184000.0' # 60 days of lock time
BONUS = '2.0'

# Code to run
PACT_CODE = f'''
({CONTRACT_NAME_BONDING}.create-bonded-nft
  "{BONDING_POOL_NAME}"
  "{TOKEN_ID}"
  {PAYOUT_COIN}
  {BOND_VALUE}
  (time "{MATURE_TIME}")
)
({CONTRACT_NAME_STAKING}.create-unlocked-nft-pool
  "{UNLOCKED_POOL_NAME}"
  "{TOKEN_ID}"
  {PAYOUT_COIN}
  {APY}
  {BOND_VALUE}
  (time "{START_TIME}")
)
({CONTRACT_NAME_STAKING}.create-locked-nft-pool
  "{LOCKED_POOL_NAME}"
  "{TOKEN_ID}"
  {PAYOUT_COIN}
  {APY}
  {BOND_VALUE}
  (time "{START_TIME}")
  {LOCK_TIME_SECONDS}
  {BONUS}
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