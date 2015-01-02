"""
Forked from https://en.bitcoin.it/wiki/Mini_private_key_format

To run make sure that pybitcointools is installed.

    sudo pip install pybitcointools

No you can run the script

    python hidden_bits.py <hiddenbits-secret> <api-key>

It will create a db directory and a qr code directory full of files.
"""

from pybitcointools.main import encode_privkey, privkey_to_address, random_key, encode, decode, sha256
import requests
import subprocess
import hashlib
import sys

BASE58 = '23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def writeRecord(address, privateKey, minikey):
    path = "db/{}".format(address)
    subprocess.call(["mkdir", "-p", path])
    subprocess.call(["mkdir", "-p", "qr"])
    f = open("{}/record.txt".format(path), "w")
    f.write("Private Key: {}\n".format(privateKey))
    f.write("Mini AB Key: {}\n".format(minikey))
    f.write("Address: {}\n".format(address))
    f.close()

    uri = "hbits://{}".format(minikey)
    qrpath = "{}/qr_{}.png".format(path, address)
    subprocess.call(["qrencode", "-o", qrpath, uri])
    subprocess.call(["cp", qrpath, "qr"])

    if not postNewPromo(address, minikey):
        subprocess.call(["rm", "-rf", path])

def postNewPromo(address, minikey):
    token=address[-4:]
    data={
        'token': token,
        'message': 'Congratulations! You found some hidden bits. If you tweet, you can have some more!',
        'zero_message': 'Sorry. You are too late. The hidden bits have already been claimed. Would you like to tweet anyway?',
        'tweet': 'I love Airbitz! Feed me! #airbitz #{}'.format(token),
    }
    headers={"Authorization": "Token {}".format(API_KEY)}
    r = requests.post('https://api.airbitz.co/api/v1/promo/new/',
                        headers=headers,
                        data=data)
    return r.status_code == 201

def generateCandidate():
    minikey = '%s%s' % ('S', ''.join(random_key()[:29]))
    return minikey, obfuscate(minikey)

def validPrivKey(key):
    try:
        privkey_to_address(key)
    except:
        return False
    return True

def generateKeys(numKeys=1):
    keysGenerated = 0
    totalCandidates = 0
    while keysGenerated < numKeys:
        try:
            (cand, privateKey) = generateCandidate()
            # Do typo check
            t = '%s!' % cand
            # Take one round of SHA256
            candHash = hashlib.sha256(t).digest()
            # Check if the first eight bits of the hash are 0
            if candHash[0] == '\x00' and validPrivKey(privateKey):
                compressed = encode_privkey(privateKey, 'bin_compressed')
                address = privkey_to_address(compressed)
                writeRecord(address, privateKey, cand)
                print('\nMini: %s\nSecret: %s\nAddress: %s\nsha256(!): %s' %
                      (cand,
                       privateKey,
                       address,
                       candHash.encode('hex_codec')))
                if checkShortKey(cand):
                    print('Validated.')
                else:
                    print('Invalid!')
                keysGenerated += 1
            totalCandidates += 1
        except KeyboardInterrupt:
            break
    print('\n%s: %i\n%s: %i\n%s: %.1f' %
          ('Keys Generated', keysGenerated,
           'Total Candidates', totalCandidates,
           'Reject Percentage',
           100*(1.0-keysGenerated/float(totalCandidates))))
 
def checkShortKey(shortKey):
    if len(shortKey) != 30:
        return False
    t = '%s!' % shortKey
    tHash = hashlib.sha256(t).digest()
    # Check to see that first byte is \x00
    if tHash[0] == '\x00':
        return True
    return False

def obfuscate(shortkey):
    t1 = [decode(c, 16) for c in sha256(shortkey)]
    t2 = [decode(c, 16) for c in HBITZ_KEY]
    k = ''.join([encode(c1 ^ c2, 16) for (c1,c2) in zip(t1, t2)])
    return k

if __name__ == '__main__':
    global HBITZ_KEY, API_KEY
    HBITZ_KEY = sys.argv[1]
    API_KEY = sys.argv[2]
    generateKeys()
