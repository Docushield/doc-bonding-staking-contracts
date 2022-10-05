#### Creating Your Keyring

This library relies on python [keyring](https://pypi.org/project/keyring/) to pull in your private keys.

To setup your private key in the keyring:
`keyring set kadena deploy`
Then paste in your private key.

You will also need to create your own `keys.json` file. An example has been created for you, simply copy it and fill in your public key. `keys.json` is in the gitignore. It will not be pushed to the repo or any repo.

##### contract_deploy.py

Use this to deploy your contracts simply.

`python3 contract_deploy.py -p ../marmalade-nft-staking.pact -n marmalade-nft-staking -i yes`
Will deploy the contract and call init on it.
You will need to modify the file to have the proper keysets. By default, GOV and OPS will be whatever you define in the `keys.json` file.

If you wish to do a local send, comment out `send_and_listen` and comment in `local`.
