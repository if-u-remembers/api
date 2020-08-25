from apis import reApi

url_api = 'https://sandboxdnac2.cisco.com'
path1 = '/dna/intent/api/v1/template-programmer/project'


class new_func_two:
    def __init__(self, url, path):
        user = 'admin'
        pwd = ' Cisco12345!'
        self.urls = url + path
        self.reapi = reApi.reapis(self.urls, user, pwd)

    def mkdir(self):
        body = {'name': 'cheshi1'}
        return self.reapi.putapi(body)


a = new_func_two(url_api, path1).mkdir()
print(a)