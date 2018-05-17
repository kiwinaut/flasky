import subprocess as sp
from os.path import splitext
from config import CONFIG

apps = {
    # '.mkv': Mime.VIDEO,
    # '.mp4': Mime.VIDEO,
    # '.mpg': Mime.VIDEO,
    # '.mpeg': Mime.VIDEO,
    # '.mov': Mime.VIDEO,
    # '.mov': Mime.VIDEO,
    # '.avi': Mime.VIDEO,
    # '.wmv': Mime.VIDEO,
    # '.lib.tar': Mime.LIBIMAGE,
    '.tar': ('tar', '-tvf'),
    # '.tar.gz': Mime.ARCHIVE,
    '.zip': ('unzip', '-l'),
    # '.rar': Mime.ARCHIVE,
    # '.jpg': Mime.Image,
    # '.jpeg': Mime.Image,
    # '.jpg-large': Mime.Image,
    # '.png': Mime.Image,
    # '.gif': Mime.Image,
}

def get_info(filepath):
	fp = CONFIG['mount']+'/'+filepath
	_, ext = splitext(fp)
	cmd = apps.get(ext)
	if cmd:
		c = sp.run([*cmd, fp], stdout = sp.PIPE)
		return c.stdout
	else:
		return 'no info cmd'
