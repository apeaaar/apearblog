from flask import render_template
from flask import Request
from flask import redirect
from flask import url_for
from app import fapp
from app.db.blog import *
from app.db.blogclass import articles, randomclass
from app.db import mongo
from app.tools.request import *


@fapp.route("/")
@fapp.route("/home/")
def HomeView():
    if checkRequest():
        top_articles = queryrecommendblog()
        all_articles = articles(1)
        site = getSite()
        allpages = blog.getBlogPages()
        fapp.logger.info("首页访问 IP:%s" % request.remote_addr)
        return render_template(
            "index.html",
            site=site,
            all_articles=all_articles,
            top_articles=top_articles
        )
    else:
        return "sb"


@fapp.route("/archive/")
def ArchiveFView():
    if checkRequest():
        all_articles = articles(number=int(1))
        site = getSite()
        fapp.logger.info("文章列表 固定第一页 IP:%s" % request.remote_addr)
        return render_template(
            "archive.html",
            site=site,
            all_articles=all_articles
        )
    else:
        return "sb"


@fapp.route("/archive/page/<int:nowsnumber>/")
def ArchiveView(nowsnumber):
    if checkRequest():
        allpages = blog.getBlogPages()
        if allpages >= nowsnumber:
            all_articles = articles(number=int(nowsnumber))
            site = getSite()
            fapp.logger.info("文章列表 第%d页 IP:%s" % (nowsnumber, request.remote_addr))
            return render_template(
                "archive.html",
                site=site,
                all_articles=all_articles
            )
        else:
            return render_template("404.html"), 404
    else:
        return "sb"


@fapp.route("/article/id/<int:postid>/")
def ArticleView(postid):
    if checkRequest():
        site = getSite()
        article = queryapost(int(postid))
        for i in mongo.siteContentsField.objects(objectsid=1):
            leanname = i.leanname
            leankey = i.leankey
        fapp.logger.info("文章 ID:%d IP:%s" % (postid, request.remote_addr))
        return render_template(
            "article.html",
            site=site,
            article=article,
            leanname=leanname,
            leankey=leankey
        )
    else:
        return "sb"


@fapp.route("/tag/")
def TagView():
    if checkRequest():
        site = getSite()
        tags = getaTagList()
        fapp.logger.info("标签列表 固定第一页 IP:%s" % request.remote_addr)
        return render_template(
            "tag.html",
            site=site,
            tagset=tags,
            randomclass=randomclass
        )


@fapp.route("/tag/id/<int:tagid>/article/page/<pages>")
def TagArticleView(tagid, pages):
    site = getSite()
    tags = getaTagList()
    article = TagArticles(pages, tagid)
    fapp.logger.info("标签文章列表 第%d页 IP:%s" % (tagid, request.remote_addr))
    return render_template(
        "article_tag.html",
        site=site,
        tags=tags,
        randomclass=randomclass,
        article=article
    )


@fapp.route("/category/")
def CategoryView():
    if checkRequest():
        site = getSite()
        categories = getaCategoryList()
        fapp.logger.info("分类列表 IP:%s" % request.remote_addr)
        return render_template(
            "category.html",
            site=site,
            categories=categories
        )


@fapp.route("/category/id/<cateid>/article/page/<pages>/")
def CategoryArticleView(cateid, pages):
    site = getSite()
    categories = getaCategoryList()
    article = CateArticles(pages, cateid)
    fapp.logger.info("分类文章列表 第%d页 IP:%s" % (cateid, request.remote_addr))
    return render_template(
        "article_tag.html",
        site=site,
        categories=categories,
        article=article
    )


@fapp.route("/about/")
def AboutView():
    site = getSite()
    return render_template(
        "about.html"
    )
