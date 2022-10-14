import app.db.blog
from app.db import mongo

mongoconnectstr = "mongodb://taoyan:Qwe123./@127.0.0.1:27017/blog"
# mongodb://my_user:my_password@127.0.0.1:27017/my_db
# mongodb://127.0.0.1:27017/my_db
# 这是连接字符串，其它的去https://docs.mongoengine.org/guide/connecting.html看

#要在这里弄一个管理员，所以在app.py里写一句调用这个函数，在看到数据库里有信息后就行了。不要多次调用！！不能有同名的，别闲着没事弄好几个号

def newadmin():
    name = ""
    # 这是管理员名称
    pwd = ""
    # 这是管理员密码
    app.db.blog.blogNewAdmin(name,pwd)

def first():
    app.db.blog.blogNewAdmin("taoyan","qwe123./")
    desc = mongo.siteContentsField()
    desc.objectsid = 1
    desc.SITE_URL = "www.taoyan.xyz"
    desc.SITE_TITLE = "aPear"
    desc.BLOG_MAX_ID = 99999999
    desc.SITE_ICP = "沪ICP备2022003348号-1"
    desc.SITE_START_TIME = "2022/08/28?"
    desc.SITE_MAIL = "abab@ab.ab"
    desc.SITE_YEAR = "2022"
    desc.SITE_AVATAR = "https://s1.ax1x.com/2022/07/09/jrawb8.jpg"
    desc.BeautifulSentence = "Tears are words the heart can't say. 眼泪是心里无法诉说的言辞。"
    desc.SITE_TYPE_ENGLISH = "Delay is the deadliest form of denial. "
    desc.SITE_TYPE_CHINESE = "拖延是最彻底的拒绝。"
    desc.leanname = "Q2qlamaqqHqD868vvCknVS8N-9Nh9j0Va"
    desc.leankey = "x5pNoFp6xEVyjewAj2NeED19"
    desc.secret_route = "sssss1278asn91b"
    desc.save()