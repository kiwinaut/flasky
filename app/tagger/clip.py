from thumbnailer import clip
from thumbnailer.archive import Thumbnailer
from config import CONFIG

THUMB_SIZE = 300, 300
SCREENSHOT_SIZE = 1024, 768

def rethumb(item, media, value):
    fpath = '%s/%s' % (CONFIG['mount'], item.filepath)
    if media == 'videos':
        clp = clip.Clip(fpath)
        # time = duration_to_int(value)
        blob = clp.extract_frame(value, THUMB_SIZE[0])
    elif media == 'archives':
        t = Thumbnailer(size=THUMB_SIZE)
        blob = t.get_blob(fpath, infoname=value.strip())
    dest = '%s/%s/%s.jpg' % (CONFIG['mount'], 'persistent/1001/thumbs', item.sha)
    with open (dest, 'wb') as fp:
        fp.write(blob)


def new_screenshot(item):
    fpath = '%s/%s' % (CONFIG['mount'], item.filepath)
    clp = clip.Clip(fpath)
    blob = clp.screenshot(SCREENSHOT_SIZE[0], SCREENSHOT_SIZE[1])
    dest = '%s/%s/%s_s.jpg' % (CONFIG['mount'], 'persistent/1001/thumbs', item.sha)
    with open (dest, 'wb') as fp:
        fp.write(blob)

