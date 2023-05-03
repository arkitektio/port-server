from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

def download_logo(url: str) -> File:
    img_tmp = NamedTemporaryFile(delete=True)
    with urlopen(url) as uo:
        assert uo.status == 200
        img_tmp.write(uo.read())
        img_tmp.flush()
    return File(img_tmp)