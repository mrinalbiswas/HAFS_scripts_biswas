import os
import sys
import subprocess


if len(sys.argv) < 3:
    print("Must specify exactly one dir name, branch name")
    sys.exit(1)

dirname   = os.path.expandvars(sys.argv[1])
branch_name = sys.argv[2]

# Read the input file as the first argument
dirname   = os.path.expandvars(sys.argv[1])
print(dirname)
branch_name = sys.argv[2]
print(branch_name)
subprocess.call(['git', 'clone', '-b', branch_name, '--recursive', 'https://github.com/hafs-community/HAFS.git', dirname])
os.chdir(dirname + '/sorc')
print("Changed diectory to: ", dirname + '/sorc')
subprocess.call(['./install_hafs.sh'])
subprocess.call(['./link_fix.sh'])
os.chdir('../parm')
print("Changed diectory to: ", dirname + '/parm')
sys_conf = open("system.conf", "rt")
data = sys_conf.read()
data = data.replace('hwrfv3', 'dtc-hwrf')
sys_conf.close()
sys_conf = open("system.conf", "wt")
sys_conf.write(data)
sys_conf.close()
