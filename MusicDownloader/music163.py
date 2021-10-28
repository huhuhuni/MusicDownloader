import requests
import execjs
import base64, codecs
from Crypto.Cipher import AES
from bs4 import BeautifulSoup
import re
import json

header = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'Host': 'music.163.com',
    'origin': 'https://music.163.com',
    'referer': 'https://music.163.com',
    'content-type': 'application/x-www-form-urlencoded',
    'Agent': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    }
download_header = {
    'Host': 'm701.music.126.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}
url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=a15c851be507e69bdd2cdd0252f03540'

b = "010001"
c = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = '0CoJUm6Qyw8W8jud'


class music163_:
    def __init__(self):
        self.i = self.get_i.call('a', 16)

    def to_16(self, key):
        while len(key) % 16 != 0:
            key += '\0'
        return str.encode(key)

    get_i = execjs.compile(r"""
        function a(a) {
        var d,
        e,
        b = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        c = '';
        for (d = 0; a > d; d += 1) e = Math.random() * b.length,
        e = Math.floor(e),
        c += b.charAt(e);
        return c
      }
    """)

    def AES_encrypt(self, text, key, iv):  # text为密文，key为公钥，iv为偏移量
        bs = AES.block_size
        pad2 = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
        encryptor = AES.new(self.to_16(key), AES.MODE_CBC, self.to_16(iv))
        encrypt_aes = encryptor.encrypt(str.encode(pad2(text)))
        encrypt_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
        return encrypt_text

    def get_params(self, id, g):  # id为歌曲id
        iv = "0102030405060708"
        # csrf_token: ""
        # encodeType: "aac"
        # ids: "[1840238019]"
        # level: "standard"
        encText = str({'csrf_token': "", 'encodeType': "aac", 'ids': "[" + str(id) + "]", 'level': "standard"})  # i7b
        return self.AES_encrypt(self.AES_encrypt(encText, g, iv), self.i, iv)

    def RSA_encrypt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def get_encSecKey(self):
        global b
        global c
        return self.RSA_encrypt(self.i, b, c)

    def download(self, id):
        fname = 'default'
        with requests.get('https://music.163.com/song?id=' + id, timeout=10,
                          allow_redirects=False) as response:
            html = response.content
            # html.decode('utf-8')
            bs = BeautifulSoup(html, "html.parser")
            title = bs.select("title")[0].text
            fname = re.sub(r"[\/\\\:\*\?\"\<\>\| \$\^\+\-\!]", '_', title)
        # m = music163()
        # print(m.get_params(id, g))
        payload = {'params': self.get_params(id, g), 'encSecKey': self.get_encSecKey()}
        try:
            with requests.post(url, headers=header, data=payload) as response:
                text = response.content
                print(response.content)
                response_json = json.loads(response.content)
                data = response_json.get('data', "[{}]")
                dowload_url = data[0].get('url', "")
                print(dowload_url)
                if dowload_url == None or dowload_url == "":
                    raise Exception("can not find download_URL")
                dowload_host = dowload_url.split('/')[2]
                print(dowload_host)
                download_header['host'] = dowload_host
            if dowload_url.endswith(".m4a") or dowload_url.endswith(".mp3"):
                with requests.get(dowload_url, headers=download_header, timeout=10, stream=True) as response:
                    text = response.content
                    with open(fname + '.mp3', 'wb') as f:
                        f.write(text)
                        f.flush()
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print(e)
            print("Download Error...下载出错")


if __name__ == '__main__':
    m = music163_()
    m.download("571854148")





