
from kadena_sdk.kadena_sdk import KadenaSdk
from kadena_sdk.key_pair import KeyPair

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p') # Contract path
parser.add_argument('-i') # Init, providing a value means it's true
args = parser.parse_args()

# Setup Endpoint and Keys
CONTRACT_PATH = args.p
init = args.i != None

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

print(f'Deploying contract located at {CONTRACT_PATH}. Initialize: {init}')

contract_content = ''
with open(CONTRACT_PATH, 'r') as f:
  contract_content = f.read()

payload = {
  "exec": {
    "data": {
      "gov": { "keys": ["86f16edfb6d0535248c354557ec663cc44b06f5bfa10d034994cfddcddb00ec0"], "pred": "keys-all"},
      "ops": { "keys": ["86f16edfb6d0535248c354557ec663cc44b06f5bfa10d034994cfddcddb00ec0"], "pred": "keys-all"},
      "init": init
    },
    "code": contract_content,
  }
}
signers = [
  {
    "pubKey": key_pair.get_pub_key(),
    # Unrestricted signing key!
  }
]

print()
cmd = sdk.build_command(f'k:{key_pair.get_pub_key()}', payload, signers)
# result = sdk.local(cmd)
result = sdk.send_and_listen(cmd)
print(result.text)

print()