
from os import system, environ
from os.path import exists, join, expanduser
from ende import EncrypterDecrypter
from getpass import getpass
from argpi import ArgumentDescription, Arguments, FetchType
import sys

class Installer:
    def __init__(self, package: str = "", packages_: list[str] = []):
        self.package = package
        self.__runner = system
        self.packages = packages_

        # maintain ~/.gemfury_auth
        if not exists(join(expanduser('~'), '.gemfury')):
            print("Paste your gemfury auth token below:")
            token = input().replace('\n', '')
            user = input("gemfury username: ").replace('\n', '')
            if token != "" or token != None:
                with open(join(expanduser('~'), '.gemfury'), 'w+') as authfile:
                    authfile.write(user + '\n' + token)
            else:
                sys.exit(1)
                
            # encrypter
            # choose a password
            p = getpass("choose a password for secure saving of creds: ")
            enc = EncrypterDecrypter(['-enc', join(expanduser('~'), '.gemfury'), p])
            enc.analyseTask()
            enc.carryOutTask()
        else:
            # decrypter
            # enter password
            p = getpass("password: ")
            dec = EncrypterDecrypter(['-dec', join(expanduser('~'), '.gemfury'), p])
            dec.analyseTask()
            dec.carryOutTask()

            with open(join(expanduser('~'), '.gemfury'), 'r+') as authfile:
                parts = authfile.read().split('\n')
                user = parts[0]
                token = parts[1]
                # print(user, token)
            
            # encrypt again
            enc = EncrypterDecrypter(['-enc', join(expanduser('~'), '.gemfury'), p])
            enc.analyseTask()
            enc.carryOutTask()

        environ['AUTH'] = token
        environ['USER_'] = user
    
    @property
    def run(self):
        # print(f"pip install {self.package} --index-url https://$AUTH@repo.furi.io/$USER_/")
        return self.__runner(f"pip install {self.package} --extra-index-url https://$AUTH@pypi.fury.io/$USER_/")
    
    @property
    def run_multiple(self):
        for file in self.packages:
            with open(file, 'r+') as packagefile:
                packages = packagefile.readlines()
                
            requirement_string = packages[0].replace('\n', '')
            for x in packages[1:]:
                requirement_string += " " + x.replace('\n', '')
            
            self.__runner(f"pip install {requirement_string} --extra-index-url https://$AUTH@pypi.fury.io/$USER_/")

def main():
    arguments = Arguments().__capture__()
    arguments.__add__(
        "--install",
        ArgumentDescription().shorthand('-i')
    )
    arguments.__add__(
        "--requirements",
        ArgumentDescription().shorthand("-r")
    )

    arguments.__analyse__()

    if arguments.__there__("--install"):
        if arguments.__there__("--requirements"):
            installer = Installer(packages_=arguments.__fetch__("--requirements", FetchType.TILL_LAST))
            installer.run_multiple
        else:
            installer = Installer(package=arguments.__fetch__("--install", FetchType.SINGULAR))
            installer.run
        
        sys.exit(0)
    else:
        print("Argument Error!")
        print("   Syntax: furypie --install/-i <package-name>")
        print("   for multiple from a file:")
        print("   Syntax: furypie --install -r <index-file>")