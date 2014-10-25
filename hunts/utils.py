from bitcoin import *

def getbountydetails (treasurehunt):
    # 1. Generate n private keys
    # 2. Generate multisig address basis m and n and above private keys
    # 3, Return object with all the above data
    m = treasurehunt.m
    n = treasurehunt.location_set.count()
    magicbyte = 111 if treasurehunt.istestnet else 0
    privkeys = []
    pubkeys = []
    for i in range(0,n):
        k = random_key()
        privkeys.append(k)
        pubkeys.append(privtopub(k))
    script = mk_multisig_script (pubkeys,m,n)
    bountyaddress = scriptaddr(script, magicbyte=magicbyte)
    treasurehunt.address = bountyaddress
    locations = treasurehunt.location_set.all()
    for i,location in enumerate(locations):
        location.payload = privkeys[i]
        location.save()
    return treasurehunt
