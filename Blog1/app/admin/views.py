import json

from app import fapp
from app.db.mongo import blogAdminField
from app.db import mongo
from app.admin import forms
from app.admin import db
from app.admin import forms
from app.db import blog as blogfunc
from app.db import mongo
from app.db import blogclass
from flask import render_template
from flask import session
from flask import redirect
from flask import flash
from flask import request
import json
import os


@fapp.route("/xxxx/admin/login/", methods=["GET", "POST"])
def AdminLoginView():
    loginform = forms.AdminLoginForm()
    data = {}
    if loginform.validate_on_submit():
        data["name"] = loginform.name.data
        data["password"] = loginform.password.data
        if db.checkadmin(loginform.name.data, loginform.password.data):
            session["adminid"] = db.getAdminID(loginform.name.data)
            fapp.logger.info("后台登录成功 IP:{}".format(request.remote_addr))
            return redirect("/" + db.getAdminSecretRoute() + "/home/")
        else:
            return render_template(
                "admin/login.html",
                loginform=loginform
            )
    return render_template(
        "admin/login.html",
        loginform=loginform
    )


@fapp.route("/<secret_route>/home/")
@db.checkAdmin
def AdminHomeView(secret_route):
    if secret_route == db.getAdminSecretRoute():
        adminsite = db.adminsite("home")
        fapp.logger.info("后台首页访问！ IP:{}".format(request.remote_addr))
        return render_template(
            "admin/home.html",
            adminsite=adminsite,
            adminname=db.getAdminName()
        )
    else:
        return redirect("/errorpage")


@fapp.route("/<secret_route>/post-manager/")
@db.checkAdmin
def AdminPostHomeView(secret_route):
    if secret_route == db.getAdminSecretRoute():
        adminsite = db.adminsite("post")
        blog = db.adminPostManager()
        fapp.logger.info("后台文章主页访问！ IP:{}".format(request.remote_addr))
        return render_template(
            "admin/post/post.html",
            adminsite=adminsite,
            adminname=db.getAdminName(),
            blog=blog
        )
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/post-manager/post/<int:pages>/")
@db.checkAdmin
def AdminPostManagerView(secret_route, pages):
    if secret_route == db.getAdminSecretRoute():
        adminsite = db.adminsite("post")
        blog = db.adminPostList(pages)
        fapp.logger.info("后台 IP:{}".format(request.remote_addr))
        return render_template(
            "admin/post/postlist.html",
            adminsite=adminsite,
            blog=blog
        )
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/post-manager/post/new/", methods=["GET", "POST"])
@db.checkAdmin
def AdminPostNewView(secret_route):
    if secret_route == db.getAdminSecretRoute():
        adminsite = db.adminsite("post")
        fapp.logger.info("后台文章新建界面访问 IP:{}".format(request.remote_addr))
        return render_template(
            "admin/post/newpost.html",
            adminsite=adminsite,
            category=forms.category(),
            tag=forms.tag()
        )
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/post-manager/post/addpost/", methods=["GET", "POST"])
@db.checkAdmin
def AdminPostNewData(secret_route):
    if secret_route == db.getAdminSecretRoute():
        try:
            fapp.logger.info("后台文章新建API访问 IP:{}".format(request.remote_addr))
            bdatajs = request.data
            bdatajs = bdatajs.decode("utf-8")
            datajs = json.loads(str(bdatajs))
            title = datajs["title"]
            desc = datajs["desc"]
            categoryid = int(datajs["category"])
            tagidlist = datajs["tag"]
            image = datajs["image"]
            content = datajs["content"]
            blogfunc.blogContentsNew(
                str(content),
                title,
                db.turnaTagNameList(tagidlist),
                categoryid,
                str(image),
                desc,
                0
            )
            return json.dumps(dict(code=1))
        except Exception as e:
            return json.dumps(dict(code=0))
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/post-manager/post/edit/<int:postid>/", methods=["GET", "POST"])
@db.checkAdmin
def AdminPostEditView(secret_route, postid):
    if secret_route == db.getAdminSecretRoute():
        adminsite = db.adminsite("post")
        postcontext = ""
        for i in mongo.blogField.objects(blogid=postid):
            postcontext = i.blogcontents
        fapp.logger.info("后台文章编辑界面访问 IP:{}".format(request.remote_addr))
        return render_template(
            "admin/post/editpost.html",
            adminsite=adminsite,
            category=db.turnaCateEditList(),
            tag=db.turnaTagEditList(),
            post=db.adminPostClass(postid),
            postcontext=postcontext
        )
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/post-manager/post/editpost/", methods=["GET", "POST"])
@db.checkAdmin
def AdminPostEditData(secret_route):
    if secret_route == db.getAdminSecretRoute():
        try:
            fapp.logger.info("后台文章编辑API访问 IP:{}".format(request.remote_addr))
            bdatajs = request.data
            bdatajs = bdatajs.decode("utf-8")
            datajs = json.loads(str(bdatajs))
            title = datajs["title"]
            desc = datajs["desc"]
            categoryid = int(datajs["category"])
            tagidlist = datajs["tag"]
            image = datajs["image"]
            content = datajs["content"]
            blogid = datajs["postid"]
            blogfunc.blogContentsRestore(
                blogid,
                str(content),
                title,
                db.turnaTagNameList(tagidlist),
                categoryid,
                str(image),
                desc,
                0
            )
            return json.dumps(dict(code=1))
        except Exception as e:
            print(str(e))
            return json.dumps(dict(code=0, e=str(e)))
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/post-manager/post/delete/<int:postid>", methods=["GET", "POST"])
@db.checkAdmin
def AdminPostDeleteView(secret_route, postid):
    if secret_route == db.getAdminSecretRoute():
        adminsite = db.adminsite("post")
        flash("虽说可以删，但指不定会出现什么bug，最好别删，要删也要将程序和数据库的文件备份后在试着去删")
        postname = ""
        for i in mongo.blogField.objects(blogid=postid):
            postname = i.blogtitle
        if request.method == "POST":
            try:
                bdatas = request.data
                datas = bdatas.decode("utf-8")
                jdata = json.loads(str(datas))
                fapp.logger.info("后台文章删除API访问 IP:{}".format(request.remote_addr))
                if str(jdata["isok"]) == "1":
                    mongo.blogField.objects(blogid=postid).delete()
                    return json.dumps(dict(isok=1))
                else:
                    return json.dumps(dict(isok=0, msg="你的isok不是1呀，你是不是啥输错了？"))
            except Exception as e:
                print(str(e))
                return json.dumps(dict(isok=0, msg=str(e)))
        fapp.logger.info("后台文章删除界面删除 IP:{}".format(request.remote_addr))
        return render_template(
            "admin/post/deletepost.html",
            postname=postname,
            postid=postid,
            adminsite=adminsite
        )
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/post-manager/post/recommend/<int:postid>/", methods=["GET", "POST"])
@db.checkAdmin
def AdminPostRecommendView(secret_route, postid):
    if secret_route == db.getAdminSecretRoute():
        form = forms.AdminPostRecommendForm()
        adminsite = db.adminsite("post")
        thisisre = ""
        for i in mongo.blogField.objects(blogid=postid):
            if i.blog_is_recommend == 1:
                thisisre = True
        for i in mongo.blogField.objects(blogid=postid):
            posttitle = i.blogtitle
        if request.method == "POST":
            bdata = request.data
            jdata = json.loads(bdata.decode("utf-8"))
            fapp.logger.info("后台文章推荐API访问 IP:{}".format(request.remote_addr))
            if str(jdata["isre"]) == "1":
                post = mongo.blogField.objects(blogid=postid).get()
                post.blog_is_recommend = 1
                post.save()
                return json.dumps(dict(ok=1))
            return json.dumps(dict(ok=0, msg=str("abab")))
        fapp.logger.info("后台文章推荐界面访问 IP:{}".format(request.remote_addr))
        return render_template(
            "admin/post/repostwatch.html",
            title=posttitle,
            form=form,
            adminsite=adminsite,
            postid=postid,
            thisisre=thisisre
        )
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/tag-manager/")
@db.checkAdmin
def AdminTagListView(secret_route):
    if secret_route == db.getAdminSecretRoute():
        tagset = mongo.blogTagField.objects().all()
        adminsite = db.adminsite("tag")
        fapp.logger.info("后台标签界面访问 IP:{}".format(request.remote_addr))
        return render_template(
            "admin/tag/tag.html",
            tagset=tagset,
            adminsite=adminsite
        )
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/tag-manager/tag/<int:tagid>/")
@db.checkAdmin
def AdminTagView(secret_route, tagid):
    if secret_route == db.getAdminSecretRoute():
        tag = blogclass.tagclass(tagid)
        adminsite = db.adminsite("tag")
        return render_template(
            "admin/tag/watchtag.html",
            tag=tag,
            adminsite=adminsite
        )
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/tag-manager/tag/new/", methods=["GET", "POST"])
@db.checkAdmin
def AdminTagNewView(secret_route):
    if secret_route == db.getAdminSecretRoute():
        form = forms.AdminTagNewForm()
        adminsite = db.adminsite("tag")
        if request.method == "POST":
            bdata = request.data
            jdata = json.loads(bdata.decode("utf-8"))
            blogfunc.blogNewTag(str(jdata["newtagname"]))
            return json.dumps(dict(code=1))
        return render_template(
            "admin/tag/newtag.html",
            form=form,
            adminsite=adminsite
        )
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/tag-manager/tag/edit/<int:tagid>/", methods=["GET", "POST"])
@db.checkAdmin
def AdminTagEditView(secret_route, tagid):
    if secret_route == db.getAdminSecretRoute():
        form = forms.AdminTagEditForm()
        tag = blogclass.tagclass(tagid)
        adminsite = db.adminsite("tag")
        if request.method == "POST":
            tagclass = mongo.blogTagField.objects().get(tagid=tagid)
            bdata = request.data
            jdata = json.loads(bdata.decode("utf-8"))
            tagclass.tagname = jdata["tagname"]
            tagclass.save()
            return json.dumps(dict(code=1))
        return render_template(
            "admin/tag/tagedit.html",
            form=form,
            tag=tag,
            adminsite=adminsite
        )
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/tag-manager/tag/delete/<int:tagid>/", methods=["GET", "POST"])
@db.checkAdmin
def AdminTagDeleteView(secret_route, tagid):
    if secret_route == db.getAdminSecretRoute():
        form = forms.AdminTagDeleteForm()
        tag = blogclass.tagclass(tagid)
        adminsite = db.adminsite("tag")
        if request.method == "POST":
            mongo.blogTagField.objects(tagid=tagid).delete()
            return json.dumps(dict(code=1))
        return render_template(
            "admin/tag/deletetag.html",
            tag=tag,
            adminsite=adminsite
        )
    else:
        return redirect("/" + db.getAdminSecretRoute() + "/tag-manager/")


@fapp.route("/<secret_route>/category-manager/")
@db.checkAdmin
def AdminCategoryListView(secret_route):
    if secret_route == db.getAdminSecretRoute():
        catelist = mongo.blogCategoryField.objects().all()
        adminsite = db.adminsite("category")
        return render_template(
            "admin/category/category.html",
            adminsite=adminsite,
            categorylist=catelist
        )
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/category-manager/category/<int:categoryid>/")
@db.checkAdmin
def AdminCategoryView(secret_route, categoryid):
    if secret_route == db.getAdminSecretRoute():
        adminsite = db.adminsite("category")
        category = blogclass.categoryclass(categoryid)
        return render_template(
            "admin/category/watchcategory.html",
            adminsite=adminsite,
            category=category
        )
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/category-manager/category/new/", methods=["GET", "POST"])
@db.checkAdmin
def AdminCategoryNewView(secret_route):
    if secret_route == db.getAdminSecretRoute():
        adminsite = db.adminsite("category")
        if request.method == "POST":
            datajs = json.loads(str(request.data.decode("utf-8")))
            blogfunc.blogNewCategory(datajs["catename"])
            return json.dumps(dict(code=1,ok=1))
        return render_template(
            "admin/category/newcategory.html",
            adminsite=adminsite
        )
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/category-manager/category/edit/<int:cateid>/", methods=["GET", "POST"])
@db.checkAdmin
def AdminCategoryEditView(secret_route, cateid):
    if secret_route == db.getAdminSecretRoute():
        adminsite = db.adminsite("category")
        category = blogclass.categoryclass(cateid)
        if request.method == "POST":
            bdatajs = request.data.decode("utf-8")
            datajs = json.loads(str(bdatajs))
            categoryclass = mongo.blogCategoryField.objects(categoryid=cateid).get()
            categoryclass.categoryname = str(datajs["editname"])
            categoryclass.save()
            return json.dumps(dict(code=1))
        return render_template(
            "admin/category/categoryedit.html",
            adminsite=adminsite,
            category=category
        )
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/category-manager/delete/<int:cateid>/", methods=["GET", "POST"])
@db.checkAdmin
def AdminCategoryDeleteView(secret_route, cateid):
    if secret_route == db.getAdminSecretRoute():
        form = forms.AdminCateDeleteForm()
        adminsite = db.adminsite("category")
        category = blogclass.categoryclass(cateid)
        if request.method == "POST":
            mongo.blogCategoryField.objects(categoryid=cateid).delete()
            return json.dumps(dict(code=1,ok=1))
        return render_template(
            "admin/category/deletecategory.html",
            adminsite=adminsite,
            category=category
        )
    else:
        return redirect("/errorpage"), 404


@fapp.route("/<secret_route>/other/", methods=["GET", "POST"])
@db.checkAdmin
def AdminOtherView(secret_route):
    if secret_route == db.getAdminSecretRoute():
        siteclass = db.siteclass()
        adminsite = db.adminsite("other")
        return render_template(
            "admin/other.html",
            adminsite=adminsite,
            site=siteclass,
            siteclass=siteclass
        )
    else:
        return redirect("/errorpage"), 404

@fapp.route("/<secret_route>/otherdata/")
@db.checkAdmin
def AdminOther(secret_route):
    if secret_route == db.getAdminSecretRoute():
        try:
            bdatajs = request.data
            bdatajs = bdatajs.decode("utf-8")
            datajs = json.loads(str(bdatajs))
            s = mongo.siteContentsField.objects().get(objectsid=1)
            s.SITE_URL = str(datajs["url"])
            s.SITE_TITLE = str(datajs["title"])
            s.SITE_ICP = datajs["icp"]
            s.SITE_START_TIME = datajs["time"]
            s.SITE_MAIL = datajs["email"]
            s.SITE_AVATAR = datajs["avatar"]
            s.BeautifulSentence = datajs["avatar"]
            s.SITE_TYPE_ENGLISH = datajs["sten"]
            s.SITE_TYPE_CHINESE = datajs["stcn"]
            s.leanname = datajs["appname"]
            s.leankey = datajs["appkey"]
            return json.dumps(dict(code=1))
        except Exception as e:
            return json.dumps(dict(code=0, e=str(e)))
    else:
        return redirect("/errorpage"), 404

@fapp.route("/<secret_route>/backup/")
@db.checkAdmin
def AdminBackup(secret_route):
    if secret_route == db.getAdminSecretRoute():
        pass
    else:
        return redirect("/errorpage"), 404