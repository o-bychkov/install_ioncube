#!/usr/bin/python3
import os
import subprocess
import tarfile
import shutil
from urllib import request

os.getcwd()

php_version = subprocess.check_output("php --version", shell=True).decode('utf-8')[4:7]

# Download archive
request.urlretrieve("http://downloads3.ioncube.com/loader_downloads/ioncube_loaders_lin_x86-64.tar.gz", "ioncube_loaders_lin_x86-64.tar.gz")

# Unpack archive
tar = tarfile.open("ioncube_loaders_lin_x86-64.tar.gz")
tar.extractall()
tar.close()

extension_dir = subprocess.check_output("php -i", shell=True).decode('utf-8')
index = extension_dir.find("extension_dir")
extension_dir = extension_dir[index+17:index+38]

# Copy file
shutil.copyfile(r'./ioncube/ioncube_loader_lin_{}.so'.format(php_version, ), r'{}/ioncube_loader_lin_{}.so'.format(extension_dir, php_version))

# Edit config_file
with open(r'/etc/php/{}/fpm/php.ini'.format(php_version, ), 'a') as fpm_config_file:
    fpm_config_file.write("\nzend_extension = '{}/ioncube_loader_lin_{}.so'".format(extension_dir, php_version, ))
with open(r'/etc/php/{}/cli/php.ini'.format(php_version, ), 'a') as fpm_config_file:
    fpm_config_file.write("\nzend_extension = '{}/ioncube_loader_lin_{}.so'".format(extension_dir, php_version, ))

os.system("systemctl restart php{}-fpm.service".format(php_version, ))
