from app.db.mongo import *
from app.db.blogclass import *
from werkzeug.security import generate_password_hash,check_password_hash
from mongoengine.queryset.visitor import Q
import datetime
import markdown2



def blogContentsNew(blog_context,blog_title,blog_tag,blog_category_id,blog_img,blog_desc,blog_is_recommend=0):
    newblog = blogField()
    newblogid = blogNewMaxID()
    newblog.blogid = int(newblogid)
    newblog.blogtitle = str(blog_title)
    newblog.blogcontents = str(blog_context)
    newblog.blogtag = turnaTagIdList(blog_tag)
    #assetsobjects = blogAssetsField.objects(assetsid=id).get()
    newblog.blogimg = blog_img
    newblog.blogdate = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    newblog.blog_is_recommend = int(blog_is_recommend)
    newblog.blogcategory = blog_category_id
    newblog.blogdesc = str(blog_desc)
    newblog.save()
    return newblogid

def blogContentsRestore(postid,blog_context,blog_title,blog_tag,blog_category_id,blog_img,blog_desc,blog_is_recommend=0):
    newblog = blogField.objects().get(blogid=postid)
    newblog.blogtitle = str(blog_title)
    newblog.blogcontents = str(blog_context)
    newblog.blogtag = turnaTagIdList(blog_tag)
    newblog.blogimg = blog_img
    newblog.blogdate = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    newblog.blog_is_recommend = int(blog_is_recommend)
    newblog.blogcategory = blog_category_id
    newblog.blogdesc = str(blog_desc)
    newblog.save()
    return postid

def blogNewAssets(route,place):
    id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    newassets = blogAssetsField()
    newassets.assetsid = int(id)
    newassets.assetstime = str(time)
    newassets.assetsroute = str(route)
    newassets.assetsplace = str(place)
    return id

def blogNewTag(name):
    id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    newtag = blogTagField()
    newtag.tagid = int(id)
    newtag.tagname = str(name)
    newtag.tagtime = str(time)
    newtag.save()

def blogNewCategory(name):
    newcategory = blogCategoryField()
    id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    newcategory.categoryid = int(id)
    newcategory.categoryname = str(name)
    newcategory.categorytime = str(time)
    newcategory.save()
    return id

def blogNewAdmin(name,pwd):
    newadmin = blogAdminField()
    id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    newadmin.adminid = int(id)
    newadmin.adminname = str(name)
    pwdhash = generate_password_hash(pwd)
    newadmin.adminpwd = str(pwdhash)
    newadmin.admintime = str(time)
    newadmin.save()

def blogNewMaxID():
    newblogid = 1
    for docsobjects in siteContentsField.objects(objectsid=1):
        maxblogid = docsobjects.BLOG_MAX_ID
        newblogid = int(maxblogid) + 1
    docsobjects = siteContentsField.objects.get(objectsid=1)
    docsobjects.BLOG_MAX_ID = newblogid
    docsobjects.save()
    return maxblogid

def blogtestsitecontents():
    desc = siteContentsField()
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
    return 1

def turnaTagIdList(tagname_list):
    tagidlist = []
    for i in tagname_list:
        for tag in blogTagField.objects(tagname=i):
            tagidlist.append(tag.tagid)
    return tagidlist

def queryBlogList(page=1):#默认每个列表装9个
    a = 9 * int(page) #要查询的最小
    b = a - 1
    maxid = 1
    for docsobjects in siteContentsField.objects(objectsid=1):#不用.first()是因为出现了一个奇怪的bug
        maxid = docsobjects.BLOG_MAX_ID
    blogpagelist = []
    willquerymins = maxid - b #最小id
    willquerymaxs = willquerymins + 8
    for blog in blogField.objects(Q(blogid__lte=willquerymaxs) & Q(blogid__gte=willquerymins)):
        tagclasslist = []
        for aq in blog.blogtag:
            tagclasslist.append(tagclass(aq))
        ablog = blogdetial(id=blog.blogid,taglist=tagclasslist,category=categoryclass(blog.blogcategory),date=blog.blogdate,title=blog.blogtitle,contents=blog.blogcontents,img=blog.blogimg,desc=blog.blogdesc)
        blogpagelist.append(ablog)
    blogpagelist.reverse()
    return blogpagelist

def querycategoryblog(category_id):
    bloglist = []
    for blog in blogField.objects(blogcategory=category_id):
        tagclasslist = []
        for aq in blog.blogtag:
            tagclasslist.append(tagclass(aq))
        ablog = blogdetial()
        ablog = blogdetial(id=blog.blogid,taglist=tagclasslist,category=categoryclass(blog.blogcategory),date=blog.blogdate,title=blog.blogtitle,contents=blog.blogcontents,img=blog.blogimg,desc=blog.blogdesc)
        bloglist.append(ablog)
    return bloglist


def queryapost(id):
    ablog = 1
    for blog in blogField.objects(blogid=id):
        tagclasslist = []
        for aq in blog.blogtag:
            tagclasslist.append(tagclass(aq))
        ablog = blogdetial(blog.blogid,tagclasslist,categoryclass(blog.blogcategory),blog.blogdate,blog.blogtitle,markdown2.markdown(blog.blogcontents),blog.blogimg,blog.blogdesc,)
        ablog.bid = blog.blogid
        ablog.btag = tagclasslist
        ablog.bdesc = blog.blogdesc
        ablog.bcategory = categoryclass(blog.blogcategory)
        ablog.bdate = blog.blogdate
        ablog.btitle = blog.blogtitle
        ablog.bcontents = markdown2.markdown(blog.blogcontents)
        ablog.bimg = blog.blogimg
        ablog.bclick_count = blog.blog_click_count
    return ablog

def queryrecommendblog():
    topblog = []
    for blog in blogField.objects(blog_is_recommend=1):
        ablog = blogdetial(blog.blogid,blog.blogtag,categoryclass(blog.blogcategory),blog.blogdate,blog.blogtitle,blog.blogdesc, blog.blogcontents,blog.blogimg)
        topblog.append(ablog)
    return topblog

def addclick(blogid):
    i = blogField.objects(blogid=blogid)
    bcount = int(i.blog_click_count)
    wcount = bcount + 1
    p = i.get()
    p.blog_click_count = wcount
    p.save()
        

def getBS():
    bs = ""
    for i in siteContentsField.objects.first():
        bs = i.BeautifulSentence
    return bs

def getSITETITLE():
    SITETITLE = ""
    for i in siteContentsField.objects.first():
        SITETITLE = i.SITE_TITLE
    return SITETITLE

def getSITEURL():
    SITEURL = ""
    for i in siteContentsField.objects.first():
        SITEURL = i.SITE_URL
    return SITEURL

def getSITEICP():
    SITEICP = ""
    for i in siteContentsField.objects.first():
        SITEICP = i.SITE_ICP
    return SITEICP

def getSITESTARTTIME():
    SITESTARTTIME = ""
    for i in siteContentsField.objects.first():
        SITESTARTTIME = i.SITE_START_TIME
    return SITESTARTTIME

def getSITEMAIL():
    SITEMAIL = ""
    for i in siteContentsField.objects.first():
        SITEMAIL = i.SITE_MAIL
    return SITEMAIL

def getSITEYEAR():
    SITEYEAR = ""
    for i in siteContentsField.objects.first():
        SITETEAR = i.SITE_YEAR
    return SITEYEAR

def getSITEAVATAR():
    SITEAVATAR = ""
    for i in siteContentsField():
        SITEAVATAR = i.SITE_AVATAR
    return SITEAVATAR

def getBlogPages():
    maxid = 1
    for i in siteContentsField.objects(objectsid=1):
        maxid = i.BLOG_MAX_ID
    maxids = maxid - 99999999
    mo = maxids / 9
    mt = maxids // 9
    if maxid < 100000009:
        return 1
    else:
        if mo > mt:
            return mt + 1
        else:
            return mt

def getSite():
    site = siteclass()
    return site

def getaTagList():
    taglist = []
    tagset = blogTagField.objects().all()
    counta = 0
    for i in tagset:
        tagida = i.tagid
        tag = tagclass(int(tagida))
        taglist.append(tag)
        print(taglist[counta].tagid)
        counta += 1
    for i in taglist:
        print("ss")
        print(str(i.tagid))
    print(str(taglist))
    return taglist

def getaCategoryList():
    categorylist = []
    for i in blogCategoryField.objects().all():
        categorylist.append(categoryclass(i.categoryid))
    return categorylist

def queryBlogListFromTag(tagid,page): #每个列表默认9个
    bloglist = []
    a = [tagid]
    tagclasslist = []
    for blog in blogField.objects(tagid__in=a):
        for aq in blog.blogtag:
            tagclasslist.append(tagclass(aq))
        ablog = blogdetial(id=blog.blogid,taglist=tagclasslist,category=categoryclass(blog.blogcategory),date=blog.blogdate,title=blog.blogtitle,contents=blog.blogcontents,img=blog.blogimg,desc=blog.blogdesc)
        bloglist.append(ablog)
    lengtha = len(bloglist)#整个tag文章的列表的长度
    if lengtha<=9:
        bloglist.reverse()
        return bloglist
    else:
        lengthb = 9 * page
        lengthc = lengthb - 1
        lengthd = lengthc - 9
        lengthe = lengthc + 1
        lengthf = lengthd - 1
        bloglist.reverse()
        bloglista = bloglist[lengthf:lengthe]
        bloglista.insert(0,bloglist[lengthf])
        return bloglista

#def getTagBlogPages(id):
    #a = blogField.objects(blogtag__in=lisa).all().count()

def queryBlogListFromCate(cateid,page): #每个列表默认9个
    bloglist = []
    tagclasslist = []
    for blog in blogField.objects(blogcategory=cateid):
        for aq in blog.blogtag:
            tagclasslist.append(tagclass(aq))
        ablog = blogdetial(id=blog.blogid,taglist=tagclasslist,category=categoryclass(blog.blogcategory),date=blog.blogdate,title=blog.blogtitle,contents=blog.blogcontents,img=blog.blogimg,desc=blog.blogdesc)
        bloglist.append(ablog)
    lengtha = len(bloglist)
    if lengtha<=9:
        bloglist.reverse()
        return bloglist
    else:
        lengthb = 9 * page
        lengthc = lengthb - 1
        lengthd = lengthc - 9
        lengthe = lengthc + 1
        lengthf = lengthd - 1
        bloglist.reverse()
        bloglista = bloglist[lengthf:lengthe]
        bloglista.insert(0,bloglist[lengthf])
        return bloglista

