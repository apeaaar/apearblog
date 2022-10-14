from app.db import mongo
from flask import session
from flask import redirect
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import blogclass
from app.db import blog as blogfunc
from mongoengine import *
import functools


def checkadmin(name, pwd):
    try:
        for tmp in mongo.blogAdminField.objects(adminname=str(name)):
            pwdhash = tmp.adminpwd
        return check_password_hash(pwdhash, pwd)
    except Exception as e:
        return False


def getAdminSecretRoute():
    d = ""
    for i in mongo.siteContentsField.objects(objectsid=1):
        d = i.secret_route
    return str(d)


def getAdminID(name):
    id = 1
    for i in mongo.blogAdminField.objects(adminname=name):
        id = i.adminid
    return id


def idInAdmin(id):
    try:
        for i in mongo.blogAdminField.objects(adminid__in=[id]):
            return True
    except Exception:
        return False


def checkAdmin(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if "adminid" not in session:
            return redirect("/xxxx/admin/login/")
        return func(*args, **kwargs)
    return inner


def getAdminName():
    name = ""
    for i in mongo.blogAdminField.objects(adminid=session["adminid"]):
        name = i.adminname
    return name

def turnaTagNameList(tagidlist):
    namelist = []
    for i in tagidlist:
        for x in mongo.blogTagField.objects(tagid=int(i)):
            namelist.append(str(x.tagname))
    return namelist

def turnaTagEditList():
    return mongo.blogTagField.objects.all()

def turnaCateEditList():
    return mongo.blogCategoryField.objects.all()

def turnaTagListViewList():
    alist = []
    tag = mongo.blogTagField.objects().all()
    num = 0
    for i in tag:
        alist.append(blogclass.tagclass(i.tagid))
    return alist

def turnaCategoryViewList():
    list = []
    for i in mongo.blogCategoryField.objects().all():
        list.append(blogclass.categoryclass(i.categoryid))
    return list



class adminsite:
    def __init__(self, where):
        for i in mongo.siteContentsField.objects(objectsid=1):
            self.sitename = i.SITE_TITLE
            self.secret_route = i.secret_route
            self.year = i.SITE_YEAR
        if where == "home":
            self.page_home = True
        elif where == "post":
            self.page_post = True
        elif where == "tag":
            self.page_tag = True
        elif where == "category":
            self.page_category = True
        elif where == "admin":
            self.page_admin = True
        elif where == "other":
            self.page_admin = True
        else:
            self.page_other = True


class adminPostManager:
    def __init__(self):
        """之前的
        self.all_post = mongo.blogField.objects.all().count()
        self.all_recommend_post = mongo.blogTagField.objects(blog_is_recommend=1).count()
        taglista = []
        for i in mongo.blogTagField.objects.all():
            taglista.append(i.tagname)
        self.taglist = taglista
        categorylista = []
        for i in mongo.blogCategoryField.objects.all():
            categorylista.append(i.categoryname)
        self.categorylist = categorylista
        """
        re = 0
        all = 0
        for i in mongo.blogField.objects.all():
            all = all + 1
        for i in mongo.blogField.objects(blog_is_recommend=1):
            re = re + 1
        self.all_post = all
        self.all_recommend_post = re


class adminPostClass:
    def __init__(self, postid):
        for i in mongo.blogField.objects(blogid=postid):
            self.postnum = i.blogid - 99999999
            self.postname = i.blogtitle
            self.postdate = i.blogdate
            postag = []
            for z in i.blogtag:
                postag.append(blogclass.tagclass(z))
            self.posttag = postag
            self.posttagidlist = i.blogtag
            self.postcategory = blogclass.categoryclass(i.blogcategory)
            self.postid = i.blogid
            self.allpost = i.blogid - 99999999
            self.postimage = i.blogimg
            self.postdesc = i.blogdesc
            self.postid = i.blogid


class adminPostList:
    def __init__(self, pages):
        a = 9 * int(pages)  # 要查询的最小
        b = a - 1
        maxid = 1
        pages = int(pages)
        for docsobjects in mongo.siteContentsField.objects(objectsid=1):  # 不用.first()是因为出现了一个奇怪的bug
            maxid = docsobjects.BLOG_MAX_ID
        blogpagelist = []
        willquerymins = maxid - b  # 最小id
        willquerymaxs = willquerymins + 8
        for blog in mongo.blogField.objects(Q(blogid__lte=willquerymaxs) & Q(blogid__gte=willquerymins)):
            tagclasslist = []
            for aq in blog.blogtag:
                tagclasslist.append(blogclass.tagclass(aq))
            ablog = adminPostClass(blog.blogid)
            blogpagelist.append(ablog)
        blogpagelist.reverse()
        self.postlist = blogpagelist
        self.page_now_num = pages
        blogpages = int(blogfunc.getBlogPages())
        self.post_page = blogpages
        if pages == blogpages:
            self.has_next = False
            self.has_previous = True
        if pages == 1 and blogpages == 1:
            self.has_next = False
            self.has_previous = False
        if pages == 1 and blogpages != 1:
            self.has_next = True
            self.has_previous = False
        if pages < blogpages:
            self.has_next = True
            if pages == 1:
                self.has_previous = False
            else:
                self.has_previous = True
        page_list = []
        if blogpages <= 7:
            for i in range(1, 8):
                page_list.append(i)
        elif blogpages <= 8:
            for i in range(1, 9):
                if i == 7:
                    page_list.append("anymore")
                else:
                    page_list.append(i)
        else:
            for i in range(1, blogpages + 1):
                if i < 8:
                    page_list.append(i)
                elif i == 8:
                    page_list.append("anymore")
                else:
                    if page_list[-1] == blogpages:
                        page_list[-1] = blogpages
                    else:
                        page_list.append(blogpages)

class siteclass:
    #SITE_URL = ""
    #STIE_TITLE = ""
    #SITE_ICP = ""
    #SITE_START_TIME = ""
    #SITE_MAIL = ""
    #SITE_YEAR = ""
    #SITE_AVATAR = ""
    #BeautifulSentence = ""
    #SITE_TYPE_ENGLISH = ""
    #SITE_TYPE_CHINESE = ""
    def __init__(self):
        for i in mongo.siteContentsField.objects(objectsid=1):
            siteclass.SITE_URL = i.SITE_URL
            siteclass.SITE_TITLE = i.SITE_TITLE
            siteclass.SITE_ICP = i.SITE_ICP
            siteclass.SITE_START_TIME = i.SITE_START_TIME
            siteclass.SITE_MAIL = i.SITE_MAIL
            siteclass.SITE_YEAR = i.SITE_YEAR
            siteclass.SITE_AVATAR = i.SITE_AVATAR
            siteclass.BeautifulSentence = i.BeautifulSentence
            siteclass.SITE_TYPE_ENGLISH = i.SITE_TYPE_ENGLISH
            siteclass.SITE_TYPE_CHINESE = i.SITE_TYPE_CHINESE
            siteclass.leanname = i.leanname
            siteclass.leankey = i.leankey
            siteclass.secret_route = i.secret_route

def getAdminTagList():
    taglista = []
    tagcount = mongo.blogTagField.objects.all().count()
    s = tagcount / 9
    d = tagcount // 9
    if s > d:
        s = d + 1
    # for i in range(0,)
    for i in mongo.blogTagField.objects.all():
        taglista.append(blogclass.tagclass(i.tagid))
