import json
import os
import platform
import hashlib
import wmi

class Encoder():
    def __init__(self,type,name):
        computer = wmi.WMI()
        self.type = type
        self.path = f"config/Password_{name}.json"
        self.cpu_info = platform.processor()
        self.SKUNumber = computer.Win32_ComputerSystem()[0].SystemSKUNumber
        self.DNSHostName = computer.Win32_ComputerSystem()[0].DNSHostName
        self.base_key = self.generate_key(self.cpu_info, self.SKUNumber, self.DNSHostName)
        self.type_key = self.generate_key('pokemmo',self.type)
        self.Key = self.generate_key(self.base_key,self.type_key)

    def generate_key(self, *args):
        # 将所有参数拼接后进行MD5加密
        all_args = [str(arg) for arg in args]  # 将所有参数转换为字符串
        combined_string = ''.join(all_args)  # 拼接所有参数
        md5 = hashlib.md5()
        md5.update(combined_string.encode('utf-8'))
        password = md5.hexdigest()
        return password

    def verify_key(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                key_1 = data['key_1']
                key_2 = self.generate_key('pokemmo',self.type)
                Key = data['Key']
                if Key == self.generate_key(self.base_key,key_2):
                    return True
                if key_1 != self.base_key:
                    print("设备发生更改")
                return False
        except:
            print("密钥文件不存在！")
            return False

    def store_key(self):
        # 将加密的密文存储到指定文件中
        data = {
            "key_1":self.base_key,
            "Key": self.Key,
        }
        # 将数据写入 JSON 文件
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True

    def is_run(self):
        if not os.path.exists(self.path):
            # 文件不存在 ，则认为是首次运行
            print("烦请将>>" + str(self.base_key) + "<<内的信息发送给我，待我收到后，会将密钥提供给您。")
            a = input("请将我提供的密钥输入到这里>>>")
            if self.Key == a:
                return self.store_key()
        else:
            # 文件存在，则直接验证是否相等
            return self.verify_key()



