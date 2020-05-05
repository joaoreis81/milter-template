import logging as log
import sys
import os


log.basicConfig(stream=sys.stderr, level=os.environ.get("LOG_LEVEL", "WARNING"))

runconfigurator = False
# Actual startup script
if runconfigurator:
    pass

os.system("/usr/libexec/postfix/post-install meta_directory=/etc/postfix create-missing")
os.system("postfix start-fg")
