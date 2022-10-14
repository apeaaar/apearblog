from mongoengine import *
connect("blog",host="localhost",port=27017,name="taoyan",password="Qwe123./")
#连接mongo


class blogField(Document): #博客内容的综合类，库中会出现一个collection，任何博客类都可以基于这个类，什么视频播客也可以用这个类s'da
    blogid = IntField(min_value=100000000,max_value=205509722,required=True)#max_value是我的原神UID,天空岛
    blogtag = ListField(field=IntField())
    blogcategory = IntField()
    blogdate = StringField()
    blogtitle = StringField(max_length=50)
    blogcontents = StringField()
    blogimg = StringField() #ReferenceField(blogAssetsField)
    blogdesc = StringField()
    blog_is_recommend = IntField(default=0) #1为推荐，0就不是了
    blog_click_count = IntField()

class blogTagField(Document): #博客的标签Model类
    tagid = IntField()
    tagname = StringField()
    tagtime = StringField()

class blogCategoryField(Document):
    categoryid = IntField()
    categoryname = StringField()
    categorytime = StringField()

class blogAssetsField(Document): #各种资源(如标题图片，文件什么的。只保存索引)
    assetsid = IntField()
    assetstime = StringField()
    assetsroute = StringField(max_length=10000)
    assetsplace = StringField(max_length=20)#这个是保存的地方，如有的是放在了static/staticfile,有的是标题图片，有的是博客里的图片。Mongo只保存存储位置，并不存储数据

class blogAdminField(Document): #博客的管理员信息
    adminname = StringField()
    admintime = StringField()
    adminpwd = StringField()
    adminid = IntField()


class siteContentsField(Document):
    objectsid = IntField()
    SITE_URL = StringField()
    SITE_TITLE = StringField()
    BLOG_MAX_ID = IntField()
    SITE_ICP = StringField()
    SITE_START_TIME = StringField()
    SITE_MAIL = StringField()
    SITE_YEAR = StringField()
    SITE_AVATAR = StringField()
    BeautifulSentence = StringField()
    SITE_TYPE_ENGLISH = StringField()
    SITE_TYPE_CHINESE = StringField()
    secret_route = StringField()
    leanname = StringField()
    leankey = StringField()


class siteContents: #杂项信息
    SITE_URL = "www.taoyan.xyz"
    STIE_TITLE = "梨子"
    BLOG_MAX_ID = 205509722
    ICP_CODE = "沪ICP备2022003348号-1"
    SITE_START_TIME = "2022-02-09 15:06"
    
