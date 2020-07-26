from key import Key
from cryptography.fernet import Fernet

class Encry:

    key = Key.keyline
    cipher_suite=Fernet(key)
    with open('passwd.bin', 'rb') as file_object:
        for line in file_object:
                encryptedpwd=line


    unc = (cipher_suite.decrypt(encryptedpwd))
    pl = bytes(unc).decode("utf=8")


#print(Encry.pl)
