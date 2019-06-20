from distutils.core import setup   
import py2exe,shutil
import glob
includes = ["encodings", "encodings.*"]   
options = {"py2exe":   
            {   "compressed": 1,   
                "optimize": 2,   
                "includes": includes,   
                "bundle_files": 1  
            }   
          }   
setup(      
    version = "1.0",   
    description = "pyllk",   
    name = "liangzi pyllk",   
    options = options,   
    zipfile=None,
    data_files=[("data",glob.glob("data/*.*"))],
    windows=[{"script": "newgui.py","icon_resources": [(1, "004.ico")] }],     
    )  
shutil.copytree('C:/Python25/share/pgu/themes/default','dist/default') 