"""
@file: random_key.py
@brief: 
@author: feihu1996.cn
@date: 18-7-11 下午7:12
@version: 1.0
"""
import random


class RandomKey:
    """
    生成符合要求的随机密码
    """
    def __init__(self, length=8, has_lowercase=True, has_capital=True, has_digit=True, has_symbol=True):
        # 指定随机字符串的长度
        self.length = length
        # 指定随机字符串中是否含有小写字母
        self.has_lowercase = self.convert_to_bool(has_lowercase)
        # 指定随机字符串中是否含有大写字母
        self.has_capital = self.convert_to_bool(has_capital)
        # 指定随机字符串是否含有数字
        self.has_digit = self.convert_to_bool(has_digit)
        # 指定随机字符串中是否符号
        self.has_symbol = self.convert_to_bool(has_symbol)

        self.lowercase_pool = list("abcdefghijklmnopqrstuvwxyz")
        self.capital_pool = [str.upper(l) for l in self.lowercase_pool]
        self.digit_pool = [str(i) for i in range(0, 10)]
        self.symbol_pool = list("!@#$%^&*()_+")

        self.result = list()
        self.data = {
            "data": '',
            "code": 0,
            "msg": "ok"
        }

    def generate(self):
        # 如果参数不合法，则返回错误信息
        if not isinstance(self.length, int):
            try:
                self.length = int(self.length)
            except:
                self.data["code"] = 1
                self.data["msg"] = "parameter is not valid!"
                return self.data

        # 根据has参数不断向列表中添加元素，如果列表长度达到限制，则退出循环
        while True:
            # 如果has_参数均为False，则返回错误信息
            if self.has_lowercase==False and self.has_capital==False and self.has_digit==False and self.has_symbol==False:
                self.data["code"] = 1
                self.data["msg"] = "At least assign one 'has_' parameter, please!"
                break

            if self.has_lowercase:
                self.result.append(random.choice(self.lowercase_pool))
                if len(self.result) >= self.length:
                    break

            if self.has_capital:
                self.result.append(random.choice(self.capital_pool))
                if len(self.result) >= self.length:
                    break

            if self.has_digit:
                self.result.append(random.choice(self.digit_pool))
                if len(self.result) >= self.length:
                    break

            if self.has_symbol:
                self.result.append(random.choice(self.symbol_pool))
                if len(self.result) >= self.length:
                    break

        # 将结果随机排序
        random.shuffle(self.result)
        self.data["data"] = ''.join(self.result)

        return self.data

    def convert_to_bool(self, bool_str):
        if bool_str == "True" or bool_str == True:
            return True
        elif bool_str == "False" or bool_str == False:
            return False
        else:
            return False

if __name__ == "__main__":
    # 示例
    print(RandomKey(has_symbol=False).generate())
