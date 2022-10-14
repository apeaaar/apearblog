from flask import request
from app import fapp

fapp.config["SESSION_COOKIE_HTTPONLY"] = True

#检查请求
def checkRequest():
    cc = True
    if cc:
        hosts = str(request.headers.get("Host","")) #获取host
        ua = str(request.headers.get("User-Agent","")) #获取ua
        ualength = len(ua) #计算ua长度
        if 1 == 1:
            if ualength > 15:
                return True
            else:
                return False
        elif 2 == 2:
            if ualength > 15:
                return True
            else:
                return False #这两个都是用来判断host是否正确，正确且UA长度正常会返回True
        else:
            return True
    return True