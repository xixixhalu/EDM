import shutil, errno
import os

def copyDirLink(src, dst):
    # os.link(src, dst)
    try:
    	if not os.path.exists(dst):    
        	shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise
