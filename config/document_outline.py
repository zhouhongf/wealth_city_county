import time
import farmhash


class DocumentOutline(object):
    """
    用于保存 产品说明书PDF文件，成立公告PDF，到期公告PDF等文件的类
    """

    def __init__(self, ukey: str, content: str):
        self._ukey = ukey
        words = ukey.split('=')
        self._bank_name = words[0]
        self._content = content

    def __repr__(self):
        return f"【ukey: {self._ukey}】"

    def do_dump(self):
        elements = [one for one in dir(self) if not (one.startswith('__') or one.startswith('_') or one.startswith('do_'))]
        data = {}
        for name in elements:
            data[name] = getattr(self, name, None)
        data['_id'] = str(farmhash.hash64(self.ukey))
        data['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        return data

    @property
    def ukey(self):
        return self._ukey

    @ukey.setter
    def ukey(self, value):
        self._ukey = value

    @property
    def bank_name(self):
        return self._bank_name

    @bank_name.setter
    def bank_name(self, value):
        self._bank_name = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value


