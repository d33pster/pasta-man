"""
Upgrade module for pasta-man
"""

from pasta_man import pasta_man
from wrapper_bar.wrapper import Wrapper
import requests

class Version:
    def __init__(self, owner:str, repository:str):
        self.__response = requests.get(f"https://api.github.com/repos/{owner}/{repository}/releases/latest")
    
    @property
    def statuscode(self) -> int:
        return self.__response.status_code
    
    @property
    def latest(self) -> str | None:
        if self.statuscode == 200:
            return self.__response.json()['tag_name']
        else:
            return None

class VersionCheck:
    def __init__(self, system_version:str = pasta_man.__version__, fetched_version:str = Version('d33pster', 'pasta-man').latest, owner:str = 'd33pster', repo:str = 'pasta-man'):
        self.__fetched_version = fetched_version.replace('v', '')
        self.__system_version = system_version
        self.__owner = owner
        self.__repo = repo
        self.checkUpdateOrUpgrade()
    
    def __check(self) -> str:
        # check if __Fetched version is None
        if self.__fetched_version == None:
            return "latest"
        
        # check lengths ... they must be similar
        while((len(self.__fetched_version.split('.')))!=(len(self.__system_version.split('.')))):
            if len(self.__fetched_version.split('.')) < len(self.__system_version.split('.')):
                self.__fetched_version += '.0'
            elif len(self.__fetched_version.split('.')) > len(self.__system_version.split('.')):
                self.__system_version += '.0'
        
        __fetched = self.__fetched_version.split('.')
        __system = self.__system_version.split('.')
        
        for i in range(len(__fetched)):
            if int(__fetched[i])>int(__system[i]):
                return "not-latest"
        
        return "latest"
        
    @property
    def status(self) -> str:
        return self.__check()
    
    def checkUpdateOrUpgrade(self) -> None:
        if self.status == 'not-latest':
            if self.__fetched_version[0] == self.__system_version[0]:
                if self.__fetched_version[2] == self.__system_version[2]:
                    # return 'update'
                    self.__choice = 'update'
                else:
                    self.__choice = 'upgrade'
            elif self.__fetched_version[0] > self.__system_version[0]:
                # return 'upgrade'
                self.__choice = 'upgrade'
            else:
                # return ''
                self.__choice = ''
        else:
            # return ''
            self.__choice = ''
        
        self._action = self.__choice
    
    @property
    def action(self) -> str:
        return self._action
    
    @action.setter
    def action(self, value:str):
        self._action = value
    
    def biggerVersion(self, version1: str, version2: str) -> str:
        vv1 = version1
        vv2 = version2
        # check lengths ... they must be similar
        while len(vv1.split('.'))!=len(vv2.split('.')):
            if len(vv1.split('.')) < len(vv2.split('.')):
                vv1 += '.0'
            elif len(vv1.split('.')) > len(vv2.split('.')):
                vv2 += '.0'
        
        v1 = vv1.split('.')
        v2 = vv2.split('.')
        
        for i in range(len(v1)):
            if int(v1[i])>int(v2[i]):
                return version1
            elif int(v1[i])<int(v2[i]):
                return version2
    
    ## check update/upgrade version
    def __checkVersion(self, action:str) -> (str | None):
        if self.action!='':
            allreleases = requests.get(f"https://api.github.com/repos/{self.__owner}/{self.__repo}/releases").json()
            if action=='update':
                firstvalue = self.__system_version[0]
                secondvalue = self.__system_version[2]
                thirdvalue = self.__system_version[4]
                # print(thirdvalue)
                finalversion = '0'
                # for all releases
                for x in allreleases:
                    # get tag
                    tag = x['tag_name'].replace('v','')
                    # if tag's first val is same to what system has
                    if tag[0] == firstvalue:
                        # second level
                        if tag[2]==secondvalue:
                            # third level
                            if tag[4] == thirdvalue:
                                continue
                            # find bigger, if the tag is bigger then update finalversion
                            if self.biggerVersion(self.__system_version, tag) == tag:
                                finalversion = self.biggerVersion(finalversion, tag)
                
                return finalversion
            elif action=='upgrade':
                if self.__fetched_version != None and self.__fetched_version!=self.__system_version and self.biggerVersion(self.__fetched_version, self.__system_version) != self.__system_version:
                    if self.__system_version[0] == self.__fetched_version[0]:
                        if self.__system_version[2] == self.__fetched_version[2]:
                            # if first two digits are same then only update can be done.
                            return None
                        elif self.__fetched_version[2] > self.__system_version[2]:
                            return self.__fetched_version
                    elif self.__fetched_version[0] > self.__system_version[0]:
                        return self.__fetched_version
        else:
            return None
        
        return None
    
    @property
    def actionversion(self) -> (str | None):
        return self.__checkVersion(self.action)

class Update:
    def __init__(self):
        self.__networkstatus = requests.get("https://google.com").status_code
        self.__status = False
        
    def __updateSequence(self):
        wrap = Wrapper()
        vc = VersionCheck()
        vc.action = 'update'
        
        codes =[
            f"""subprocess.Popen(['pip', 'install', '--upgrade', 'pasta-man=={vc.actionversion}'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL).wait()""",
            """
if platform.system()=='Windows':
    path = jPath(str(Path.home()), '.pastaman')
    remove(jPath(path, 'pasta-man.exe'))
            """
        ]
        
        dependencies = [
            """import subprocess""",
            """import platform""",
            """from os import remove""",
            """from os.path import join as jPath""",
            """from pathlib import Path"""
        ]
        
        wrap.pyShellWrapper(codes, dependencies, "upgrading:", 0.008, 65, timer='ElapsedTime')
        
        import platform
        if platform.system()=='Windows':
            from pasta_man.self_launch_thread.Launcher import makePasta
            makePasta()
    
        self.__status = True
    
    def update(self):
        self.__updateSequence()
    
    @property
    def status(self) -> bool:
        return self.__status
    
    @property
    def connectivity(self) -> bool:
        if self.__networkstatus==200:
            return True
        else:
            return False