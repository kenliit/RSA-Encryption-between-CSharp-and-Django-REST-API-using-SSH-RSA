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

    # for exporting the public key file, then you would move the file to C#, put it in the base folder of the project
    def make_sharp_public_key_file(self, public_key_file_name='./public.xml'):
        exp = self.convert_python_to_sharp(self.publicKey.e, 3)
        module = self.convert_python_to_sharp(self.publicKey.n, 256)
        xml = open(public_key_file_name, 'wb')
        xml.write(b'<?xml version="1.0" encoding="utf-16"?><RSAParameters xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><Exponent>')
        xml.write(exp)
        xml.write(b'</Exponent><Modulus>')
        xml.write(module)
        xml.write(b'</Modulus></RSAParameters>')

    # this method used to decrypt the text that encrypted in C#
    def decrypt(self, cipher_text):
        random_generator = Random.new().read
        sentinel = random_generator(20)
        cipher = PKCS1_v1_5.new(self.privateKey)
        plain_text = cipher.decrypt(base64.b64decode(cipher_text.encode('ASCII')), sentinel)
        return plain_text

    # public key file modifier
    @staticmethod
    def convert_python_to_sharp(key, length):
        key = key.to_bytes(length, 'big')
        return base64.b64encode(key)


# Code Sample
rsa = RSAToCSharp('id_rsa')
rsa.make_sharp_public_key_file()
print(rsa.decrypt("aQbrG83V98lvJkcaR7Tp2RzNp5hdafoxNIeU5ejXiG1cAyZQm/98veiZxz+V1l53q1s63lUVhhSgBHc4b25rvwV1T1jXlO4YcQUBeOrHCORAtBiDjB5H/Bim5au56ROQ5KNPTzqROwEosX+eGmfys5mQGCRpbr8UtjNnF0sZ/9MngUdKYTDqlM6wNuMzxCdUhgZtS+370ZG15rqrSYTbPJWn08HyA3p1/riaQVc/SImHqcnebqQoKhKmDvt9cxAp6tGhAMJSV8jkyrgQEW0xSBTvZ0UMaSX+15steNC/9jCHsVOdKcncCvwI6rStQaPh75OPXizVymQD/blW2Lz7RA=="))

