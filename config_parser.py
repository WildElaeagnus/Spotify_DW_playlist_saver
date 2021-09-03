"""This function will initialize the ConfigParser object and initialize the config object .
"""
import configparser
import os
from typing import ClassVar

class ConfigParser(object):
    """This method is used to initialize the ConfigParser class .

    kwargs:
        filename = "config.txt"
        config_header = "Config_section"
        configs_list = ['config_1', 'congfig_2']

    """

    def __init__(self, **kwargs):
        """This method is called by the ConfigParser class to initialize the config file .

        Raises:
            Exception: [FileNotFoundError]
        """      
        super(ConfigParser, self).__init__()
        self.filename = kwargs.pop('filename')
        self.config_header = kwargs.pop('config_header')
        self.configs_list = kwargs.pop('configs_list')
        try:        
            with open(self.filename, "r+") as f:
                self.config = configparser.ConfigParser()
                self.config.read(self.filename)
        
        except FileNotFoundError:
            with open(self.filename, "w+") as f:
                f.write(f'[{self.config_header}]\n')
                for i in self.configs_list:
                    f.write(f'{i}: \n')
            if os.path.isfile(self.filename):
                raise Exception(f'File {self.filename} created')

    
    def get_configs(self,):
        """Get configuration values from the header .

        Returns:
            [dict]: [configs]
        """    
        return dict(self.config.items(self.config_header))




if __name__ == '__main__':
    c = ConfigParser(
        filename = "config.txt",
        config_header="Config_section",
        configs_list = ['config_1', 'congfig_2']
    )
    print(c.get_configs())
