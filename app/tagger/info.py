import subprocess as sp
from os.path import splitext
from config import CONFIG

v = ('ffprobe',)
apps = {
    '.mkv': v,
    '.mp4': v,
    '.mpg': v,
    '.mpeg': v,
    '.mov': v,
    '.mov': v,
    '.avi': v,
    '.wmv': v,
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
		c = sp.run([*cmd, fp], stdout = sp.PIPE, stderr = sp.PIPE, encoding='utf-8')
		return c
	else:
		return 'no info cmd'
