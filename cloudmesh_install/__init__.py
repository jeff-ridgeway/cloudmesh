import sys
sys.path.append("..")

from cloudmesh_common.bootstrap_util import path_expand

__config_dir__ = path_expand("~/.futuregrid")

def config_file(filename):
    return __config_dir__ + filename 
