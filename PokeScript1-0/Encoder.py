import json
import platform
import hashlib
import time


class Encoder():
    def __init__(self):
        self.path = "./Data/password.json"
        self.cpu_info = platform.processor()

    def generate_key(self,date):
        # 将CPU信息和今日日期拼接后进行MD5加密

        md5 = hashlib.md5()
        md5.update((self.cpu_info +"poke_mmo"+date).encode('utf-8'))
        password = md5.hexdigest()
        return password

    def verify_key(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                password = data['password']
                if password == self.generate_key(data['initial_date']):
                    return True
        except:
            print("密钥文件不存在！")
            return False

    def store_key(self,date,password):
        # 将加密的密文存储到指定文件中
        data = {
            "initial_date": date,
            "cpu_info": self.cpu_info,
            "password": password
        }

        # 将数据写入 JSON 文件
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)