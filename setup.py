from setuptools import find_packages,setup
from typing import List

ignore='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    This will return a list of requirements

    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        [req.replace('\n', '') for req in requirements]
    
    if(ignore in requirements):
        requirements.remove(ignore)
    
    return requirements

setup(
    name='SmartestEnergy',
    version = "0.0.1",
    author="Neil",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)