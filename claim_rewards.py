import os
from beem import Steem
from beem.account import Account

# 1. Configuration variables
MY_ACCOUNT = "bnwt"  
PROXY_URL = "https://steem-proxy.gikunju.workers.dev"  

# 2. Extract configuration from GitHub Secrets
MY_PRIVATE_POSTING_KEY = os.getenv("STEEM_POSTING_KEY")

if not MY_PRIVATE_POSTING_KEY:
    print("Error: STEEM_POSTING_KEY secret is missing!")
    exit(1)

try:
    print(f"Connecting to node via Cloudflare proxy: {PROXY_URL}")
    stm = Steem(node=[PROXY_URL], keys=[MY_PRIVATE_POSTING_KEY])
    
    account = Account(MY_ACCOUNT, blockchain_instance=stm)
    
    # Extract pending balances
    reward_steem = account["reward_steem_balance"]
    reward_sbd = account["reward_sbd_balance"]
    reward_vests = account["reward_vesting_balance"]
    
    print(f"Pending Rewards -> STEEM: {reward_steem}, SBD: {reward_sbd}, VESTS: {reward_vests}")
    
    # Check if there is anything to claim (balances are strings like '0.000 STEEM')
    has_steem = float(reward_steem.split()[0]) > 0
    has_sbd = float(reward_sbd.split()[0]) > 0
    has_vests = float(reward_vests.split()[0]) > 0
    
    if has_steem or has_sbd or has_vests:
        print("Claiming accumulated rewards...")
        # Broadcast claim operation to the blockchain
        stm.claim_reward_balance(
            account=MY_ACCOUNT,
            reward_steem=reward_steem,
            reward_sbd=reward_sbd,
            reward_vests=reward_vests
        )
        print("Rewards successfully claimed!")
    else:
        print("No pending rewards found to claim.")

except Exception as e:
    print(f"CRITICAL ERROR: Reward claim operation failed: {e}")
    exit(1)
