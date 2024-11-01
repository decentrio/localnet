import json
import sys
import subprocess

def get_bash_command_output(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result.stdout.strip()

def address_to_hex(address):
    json_output = get_bash_command_output(f"dymd keys parse {address} --output json --keyring-backend test --home v1")
    return "0x" + json.loads(json_output)['bytes']

def update_genesis_file(input_file, output_file, key1, key2, key3, key4, god):

    '''
    Parameters:
    input_file: The input genesis file. This file contains the initial state and configurations of the blockchain.
    output_file: The output genesis file. This file will be the modified version of the input file with necessary updates.
    key_name: The name of the key used to sign the genesis file. This key is used in the validator's signing information.
    '''
    # Retrieving the consensus address, validator address, and public key using bash commands

    distribution_module_address = "dym1jv65s3grqf6v6jl3dp4t6c9t9rk99cd84zg6v3"
    bonded_module_address = "dym1fl48vsnmsdzcv85q5d2q4z5ajdha8yu38x9fue"
    distribution_offset = 4

    consensus_address_1 = get_bash_command_output(f"dymd tendermint show-address --home {key1}")
    consensus_address_2 = get_bash_command_output(f"dymd tendermint show-address --home {key2}")
    consensus_address_3 = get_bash_command_output(f"dymd tendermint show-address --home {key3}")
    consensus_address_4 = get_bash_command_output(f"dymd tendermint show-address --home {key4}")

    validator_address_1 = json.loads(get_bash_command_output(f"dymd keys show {key1} --bech val --output json --keyring-backend test --home {key1}"))["address"]
    validator_address_2 = json.loads(get_bash_command_output(f"dymd keys show {key2} --bech val --output json --keyring-backend test --home {key2}"))["address"]
    validator_address_3 = json.loads(get_bash_command_output(f"dymd keys show {key3} --bech val --output json --keyring-backend test --home {key3}"))["address"]
    validator_address_4 = json.loads(get_bash_command_output(f"dymd keys show {key4} --bech val --output json --keyring-backend test --home {key4}"))["address"]

    account_address_1 = json.loads(get_bash_command_output(f"dymd keys show {key1} --bech acc --output json --keyring-backend test --home {key1}"))["address"]
    account_address_2 = json.loads(get_bash_command_output(f"dymd keys show {key2} --bech acc --output json --keyring-backend test --home {key2}"))["address"]
    account_address_3 = json.loads(get_bash_command_output(f"dymd keys show {key3} --bech acc --output json --keyring-backend test --home {key3}"))["address"]
    account_address_4 = json.loads(get_bash_command_output(f"dymd keys show {key4} --bech acc --output json --keyring-backend test --home {key4}"))["address"]

    validator_pubkey_1 = json.loads(get_bash_command_output(f"dymd tendermint show-validator --home {key1}"))["key"]
    validator_pubkey_2 = json.loads(get_bash_command_output(f"dymd tendermint show-validator --home {key2}"))["key"]
    validator_pubkey_3 = json.loads(get_bash_command_output(f"dymd tendermint show-validator --home {key3}"))["key"]
    validator_pubkey_4 = json.loads(get_bash_command_output(f"dymd tendermint show-validator --home {key4}"))["key"]

    account_pubkey_1 = json.loads(json.loads(get_bash_command_output(f"dymd keys show {key1} --bech acc --output json --keyring-backend test --home {key1}"))["pubkey"])["key"]
    account_pubkey_2 = json.loads(json.loads(get_bash_command_output(f"dymd keys show {key2} --bech acc --output json --keyring-backend test --home {key2}"))["pubkey"])["key"]
    account_pubkey_3 = json.loads(json.loads(get_bash_command_output(f"dymd keys show {key3} --bech acc --output json --keyring-backend test --home {key3}"))["pubkey"])["key"]
    account_pubkey_4 = json.loads(json.loads(get_bash_command_output(f"dymd keys show {key4} --bech acc --output json --keyring-backend test --home {key4}"))["pubkey"])["key"]

    account_pubkey_god = json.loads(json.loads(get_bash_command_output(f"dymd keys show {god} --bech acc --output json --keyring-backend test --home {key1}"))["pubkey"])["key"]
    account_address_god = json.loads(get_bash_command_output(f"dymd keys show {god} --bech acc --output json --keyring-backend test --home {key1}"))["address"]

    # Printing the consensus address, validator address, and public key
    print(f"Consensus Address 1: {consensus_address_1}")
    print(f"Address 1: {validator_address_1}")
    print(f"Account Address 1: {account_address_1}")
    print(f"Validator Public Key 1: {validator_pubkey_1}")
    print(f"Account Public Key 1: {account_pubkey_1}")

    print(f"Consensus Address 2: {consensus_address_2}")
    print(f"Address 2: {validator_address_2}")
    print(f"Account Address 2: {account_address_2}")
    print(f"Validator Public Key 2: {validator_pubkey_2}")
    print(f"Account Public Key 2: {account_pubkey_2}")

    print(f"Consensus Address 3: {consensus_address_3}")
    print(f"Address 3: {validator_address_3}")
    print(f"Account Address 3: {account_address_3}")
    print(f"Validator Public Key 3: {validator_pubkey_3}")
    print(f"Account Public Key 3: {account_pubkey_3}")

    print(f"Consensus Address 4: {consensus_address_4}")
    print(f"Address 4: {validator_address_4}")
    print(f"Account Address 4: {account_address_4}")
    print(f"Validator Public Key 4: {validator_pubkey_4}")
    print(f"Account Public Key 4: {account_pubkey_4}")

    print(f"God Address: {account_address_god}")
    print(f"God Public Key: {account_pubkey_god}")

    with open(input_file, 'r') as file:
        data = json.load(file)
        
    '''
    Account Section
    '''

    counter = 0
    # Give the validator address some balance. The balance should first be taken from the not_bonded_tokens_pool. if it's not found than 
    # take it from a random account with more than 1000000 udym
    not_bonded_tokens_account = next(acc for acc in data['app_state']['auth']['accounts'] if acc.get('name') == 'not_bonded_tokens_pool')
    print(not_bonded_tokens_account)
    not_bonded_tokens_balance = next(balance for balance in data['app_state']['bank']['balances'] if balance['address'] == not_bonded_tokens_account['base_account']['address'])
    not_bonded_tokens_balance['address'] = account_address_god

    for balance in data['app_state']['bank']['balances']:
        if balance['coins' ][0]['denom'] == 'adym' and int(balance['coins'][0]['amount']) > 1000000000000000000:
            counter += 1
            if (counter == 1):
                balance['address'] = account_address_1
            elif (counter == 2):
                balance['address'] = account_address_2
            elif (counter == 3):
                balance['address'] = account_address_3
            elif (counter == 4):
                balance['address'] = account_address_4
                counter = 0
                break

    # Iterate over the account and change the first account from type /ethermint.types.v1.EthAccount to 
    # have the address as the account_address and the key is the public key
    for account in data['app_state']['auth']['accounts']:
        if account.get('@type') == '/ethermint.types.v1.EthAccount' and account["base_account"]["sequence"] != "0":
            counter += 1
            if (counter == 1):
                previous_address_1 = account['base_account']['address']
                account['base_account']['address'] = account_address_1
                account['base_account']['pub_key'] = {
                    "@type": "/ethermint.crypto.v1.ethsecp256k1.PubKey",
                    "key": account_pubkey_1
                }
                print(f"ETH account: {account['base_account']}")
            elif (counter == 2):
                previous_address_2 = account['base_account']['address']
                account['base_account']['address'] = account_address_2
                account['base_account']['pub_key'] = {
                    "@type": "/ethermint.crypto.v1.ethsecp256k1.PubKey",
                    "key": account_pubkey_2
                }
                print(f"ETH account: {account['base_account']}")
            elif (counter == 3):
                previous_address_3 = account['base_account']['address']
                account['base_account']['address'] = account_address_3
                account['base_account']['pub_key'] = {
                    "@type": "/ethermint.crypto.v1.ethsecp256k1.PubKey",
                    "key": account_pubkey_3
                }
                print(f"ETH account: {account['base_account']}")
            elif (counter == 4):
                previous_address_4 = account['base_account']['address']
                account['base_account']['address'] = account_address_4
                account['base_account']['pub_key'] = {
                    "@type": "/ethermint.crypto.v1.ethsecp256k1.PubKey",
                    "key": account_pubkey_4
                }
                print(f"ETH account: {account['base_account']}")
            elif (counter == 5):
                previous_address_god = account['base_account']['address']
                account['base_account']['address'] = account_address_god
                account['base_account']['pub_key'] = {
                    "@type": "/ethermint.crypto.v1.ethsecp256k1.PubKey",
                    "key": account_pubkey_god
                }
                print(f"ETH account: {account['base_account']}")
                counter = 0
                break

    # Turn previous_address to hex and find that hex in the app_state.evm.accounts and change the address to account_address hex
    previous_address_1_hex = address_to_hex(previous_address_1)
    previous_address_2_hex = address_to_hex(previous_address_2)
    previous_address_3_hex = address_to_hex(previous_address_3)
    previous_address_4_hex = address_to_hex(previous_address_4)
    previous_address_god_hex = address_to_hex(previous_address_god)
    for account in data['app_state']['evm']['accounts']:
        if account['address'].lower() == previous_address_1_hex.lower():
            account['address'] = address_to_hex(account_address_1)
            counter += 1
        elif account['address'].lower() == previous_address_2_hex.lower():
            account['address'] = address_to_hex(account_address_2)
            counter += 1
        elif account['address'].lower() == previous_address_3_hex.lower():
            account['address'] = address_to_hex(account_address_3)
            counter += 1
        elif account['address'].lower() == previous_address_4_hex.lower():
            account['address'] = address_to_hex(account_address_4)
            counter += 1

        elif account['address'].lower() == previous_address_god_hex.lower():
            account['address'] = address_to_hex(account_address_god)
            counter += 1
        if counter == 5:
            break
        


    '''
    Staking Section
    abcsedsf sdf asdf asdf dasf
    '''
    # Updating app_state
    data['validators'] = []
    
    # Deleting specific sections in staking
    staking_sections = ['delegations', 'redelegations', 'unbonding_delegations']
    for section in staking_sections:
        data['app_state']['staking'][section] = []

    # Update last_validator_powers
    last_total_power = int(data['app_state']['staking']['last_total_power'])
    val_power = int(last_total_power / 4)
    data['app_state']['staking']['last_validator_powers'] = [
        {
            'address': validator_address_1,
            'power': str(val_power)
        },
        {
            'address': validator_address_2,
            'power': str(val_power)
        },
        {
            'address': validator_address_3,
            'power': str(val_power)
        },
        {
            'address': validator_address_4,
            'power': str(last_total_power - 3 * val_power)
        }
    ]
    
    # Update the last validator in staking.validators
    bonded_tokens_account = next(acc for acc in data['app_state']['auth']['accounts'] if acc.get('name') == 'bonded_tokens_pool')
    bonded_tokens_balance = next(balance for balance in data['app_state']['bank']['balances'] if balance['address'] == bonded_tokens_account['base_account']['address'])
    bonded_tokens = int(bonded_tokens_balance['coins'][0]['amount'])
    bonded_token = int(bonded_tokens / 4)

    if data['app_state']['staking']['validators']:
        validator_1 = data['app_state']['staking']['validators'][0]
        validator_1['consensus_pubkey']['key'] = validator_pubkey_1
        validator_1['operator_address'] = validator_address_1
        validator_1['tokens'] = str(bonded_token)
        validator_1['status'] = "BOND_STATUS_BONDED"

        validator_2 = data['app_state']['staking']['validators'][1]
        validator_2['consensus_pubkey']['key'] = validator_pubkey_2
        validator_2['operator_address'] = validator_address_2
        validator_2['tokens'] = str(bonded_token)
        validator_2['status'] = "BOND_STATUS_BONDED"

        validator_3 = data['app_state']['staking']['validators'][2]
        validator_3['consensus_pubkey']['key'] = validator_pubkey_3
        validator_3['operator_address'] = validator_address_3
        validator_3['tokens'] = str(bonded_token)
        validator_3['status'] = "BOND_STATUS_BONDED"

        validator_4 = data['app_state']['staking']['validators'][3]
        validator_4['consensus_pubkey']['key'] = validator_pubkey_4
        validator_4['operator_address'] = validator_address_4
        validator_4['tokens'] = str(bonded_tokens - 3 * bonded_token)
        validator_4['status'] = "BOND_STATUS_BONDED"

        data['app_state']['staking']['validators'] = [validator_1, validator_2, validator_3, validator_4]
      
    
    
    '''
    Distribution section
    
    '''
    # Distribution module fix
    # for balance in data['app_state']['bank']['balances']:
    #     if balance['address'] == distribution_module_address:
    #         # Find adym
    #         for coin in balance['coins']:
    #             if coin['denom'] == "adym":
    #                 coin["amount"] = str(int(coin["amount"]) - 2)
    #                 break
    #         break
        
    # Update data['app_state']['distribution']['delegator_starting_infos'] on operator address
    data['app_state']['distribution']['delegator_starting_infos'].extend([
        {
          "delegator_address": account_address_1,
          "starting_info": {
            "height": "23619",
            "previous_period": "646",
            "stake": f"{bonded_token}.000000000000000000"
          },
          "validator_address": validator_address_1
        },
        {
          "delegator_address": account_address_2,
          "starting_info": {
            "height": "23256",
            "previous_period": "638",
            "stake": f"{bonded_token}.000000000000000000"
          },
          "validator_address": validator_address_2
        },
        {
          "delegator_address": account_address_3,
          "starting_info": {
            "height": "815111",
            "previous_period": "2825",
            "stake": f"{bonded_token}.000000000000000000"
          },
          "validator_address": validator_address_3
        },
        {
          "delegator_address": account_address_4,
          "starting_info": {
            "height": "713448",
            "previous_period": "2627",
            "stake": f"{bonded_tokens - 3 * bonded_token}.000000000000000000"
          },
          "validator_address": validator_address_4
        }
    ])
    
    data['app_state']['distribution']['validator_current_rewards'].extend([
        {
          "rewards": {
            "period": "2834",
            "rewards": []
          },
          "validator_address": validator_address_1
        },
        {
          "rewards": {
            "period": "2834",
            "rewards": []
          },
          "validator_address": validator_address_2
        },        
        {
          "rewards": {
            "period": "2834",
            "rewards": []
          },
          "validator_address": validator_address_3
        },        
        {
          "rewards": {
            "period": "2834",
            "rewards": []
          },
          "validator_address": validator_address_4
        },
    ])
    
    data['app_state']['distribution']['validator_historical_rewards'].extend([
        {
            "period": "2833",
            "rewards": {
                "cumulative_reward_ratio": [
                    {
                        "amount": "0.014287418351608899",
                        "denom": "adym"
                    }
                ],
                "reference_count": 1
            },
          "validator_address": validator_address_1
        },                {
            "period": "2833",
            "rewards": {
                "cumulative_reward_ratio": [
                    {
                        "amount": "0.014287418351608899",
                        "denom": "adym"
                    }
                ],
                "reference_count": 1
            },
          "validator_address": validator_address_2
        },                
        {
            "period": "2833",
            "rewards": {
                "cumulative_reward_ratio": [
                    {
                        "amount": "0.014287418351608899",
                        "denom": "adym"
                    }
                ],
                "reference_count": 1
            },
          "validator_address": validator_address_3
        },                
        {
            "period": "2833",
            "rewards": {
                "cumulative_reward_ratio": [
                    {
                        "amount": "0.014287418351608899",
                        "denom": "adym"
                    }
                ],
                "reference_count": 1
            },
          "validator_address": validator_address_4
        }
    ])
    
    # Update bank balance 
    # for supply in data['app_state']['bank']['supply']:
    #     if supply["denom"] == "adym":
    #         supply["amount"] = str(int(supply["amount"]) - 2)
    #         break
        
    # Update the last element in app_state.slashing_signing_infos
    if data['app_state']['slashing']['signing_infos']:
        data['app_state']['slashing']['signing_infos'][-1]['address'] = consensus_address_1
        data['app_state']['slashing']['signing_infos'][-1]['validator_signing_info']['address'] = consensus_address_1

        data['app_state']['slashing']['signing_infos'][-2]['address'] = consensus_address_2
        data['app_state']['slashing']['signing_infos'][-2]['validator_signing_info']['address'] = consensus_address_2

        data['app_state']['slashing']['signing_infos'][-3]['address'] = consensus_address_3
        data['app_state']['slashing']['signing_infos'][-3]['validator_signing_info']['address'] = consensus_address_3
    
        data['app_state']['slashing']['signing_infos'][-4]['address'] = consensus_address_4
        data['app_state']['slashing']['signing_infos'][-4]['validator_signing_info']['address'] = consensus_address_4

    # Update voting params and min deposit
    data['app_state']['gov']['voting_params']['voting_period'] = "180s"
    data['app_state']['staking']['params']['unbonding_time'] = "86400s"
    data['app_state']['gov']['deposit_params']['min_deposit'][0]['amount'] = "10"
    data['chain_id'] = "dymension_1405-1"

    # Writing the updated data to the output file
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    input_file, output_file, key1, key2, key3, key4, god = sys.argv[1:8]
    update_genesis_file(input_file, output_file, key1, key2, key3, key4, god)

