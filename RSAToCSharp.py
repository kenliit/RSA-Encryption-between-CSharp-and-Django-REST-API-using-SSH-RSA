import base64

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


class RSAToCSharp:
    pem_file = None
    publicKey = None
    privateKey = None

    def __init__(self, private_key_path):
        key = open(private_key_path, 'rb').read()
        self.privateKey = RSA.importKey(key)
        self.publicKey = self.privateKey.publickey()

    def make_sharp_public_key_file(self, public_key_file_name='./public.xml'):
        exp = self.convert_python_to_sharp(self.publicKey.e, 3)
        module = self.convert_python_to_sharp(self.publicKey.n, 256)
        xml = open(public_key_file_name, 'wb')
        xml.write(b'<RSAKeyValue><Exponent>')
        xml.write(exp)
        xml.write(b'</Exponent><Modulus>')
        xml.write(module)
        xml.write(b'</Modulus></RSAKeyValue>')

    def decrypt(self, cipher_text):
        random_generator = Random.new().read
        sentinel = random_generator(20)
        cipher = PKCS1_v1_5.new(self.privateKey)
        plain_text = cipher.decrypt(base64.b64decode(cipher_text.encode('ASCII')), sentinel)
        return plain_text

    @staticmethod
    def convert_python_to_sharp(key, length):
        key = key.to_bytes(length, 'big')
        return base64.b64encode(key)


# Sample Code to use
rsa = RSAToCSharp('id_rsa')
rsa.make_sharp_public_key_file()
print(rsa.decrypt("Ds6ktP10zV/wnjPijJVrl12h1IHfCt0/huTnAVQ7xw9FR1vMndBTlFrlqAWmbM2mA4p0V/TQBZf5gy5xrXyLZNOYZbbsobZeFu5BdsigOBo1ORsKedKRsALjexYB6AsCG7JALm2ddIv8nndofhMlbib5nyLqQRtKQJl8U6JGVyBjkRwhdprPFah2JZHsJSBzFPw5VH9SsKHi3KsazzkS0UiEFDCiQgit4L1yZfjxcMatzERrxe6niCOSQi3Eit5R445CIRhRNVyygp+cWnoNrnamzR+RKrGe89TheRQQ/FPwNyj4Meo5F8q7ouXDst/Vcry0T7CgnXity0Sc2dTUhg=="))

