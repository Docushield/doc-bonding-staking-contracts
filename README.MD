# NFT Bonding and Staking

Made for DOC bonding and staking.

For information on each piece, see the readme in the folder.

# Setup Process

1. Setup `keys.json` file by following instructions in scripts > README.MD
2. Deploy contracts using `contract_deploy.py` script
3. Create pools using the `create_pools.py` script, you will need to change the parameters to match what you need.
4. Fund the banks for each of the three pools created. These can be retrieved using chainweaver, or through my `run_pact.py` script. Just need to call the `get-pool-bank` function and pass in the `pool-name` you have given it.

# Notes

For each script, you will need to change the contract to mainnet when you deploy.  
Also, if you wish, you can change the name of the contract itself to more reflect DOC. The names I have chosen are generic.