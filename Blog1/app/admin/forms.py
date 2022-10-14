from typing import List

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField, \
    TextAreaField
from wtforms.validators import DataRequired
from app.db.blogclass import tagclass, categoryclass
from app.db import mongo


def category():
    # lista = []
    '''
    for x in mongo.blogCategoryField.objects.all():
        print(str(x)+"xcate")
        for i in x:
            print(str(i)+"cate")
            category = categoryclass(i.categoryid)
            lista.append(category)
    '''
    lista = mongo.blogCategoryField.objects.all()
    return lista


def tag():
    # lista = []
    """
    for x in mongo.blogTagField.objects().all():
        for i in x:
            print(str(i))
            tag = tagclass(i.tagid)
            lista.append(tag)
            print(i.tagname)
    print(str(lista))
    """
    lista = mongo.blogTagField.objects.all()
    return lista


def postCategoryForm():
    lista = []
    numa = 0
    for i in mongo.blogCategoryField.objects():
        lista.append((i.categoryid, i.categoryname))
    turpleab = (x for x in lista)
    turpleac = tuple(turpleab)
    return turpleac


def postTagForm():
    lista = []
    numa = 0
    for i in mongo.blogTagField.objects():
        lista.append((i.tagid, i.tagname))
    turpleab = (x for x in lista)
    turpleac = tuple(turpleab)
    return turpleac


class AdminLoginForm(FlaskForm):
    name = StringField('用户名', validators=[DataRequired("请填写用户名！")])
    password = PasswordField("密码", validators=[DataRequired("请填写密码！")], )
    submit = SubmitField("登录")


class AdminPostForm(FlaskForm):
    post_title = StringField(validators=[DataRequired("请填写标题!")],
                             render_kw={'class': "form-control", 'placeholder': "请输入文章名"})
    post_desc = StringField(validators=[DataRequired("请填写简介!")],
                            render_kw={'class': "form-control", 'placeholder': "请输入简介"}
                            )
    post_category = SelectField(validators=[DataRequired("请选择一项!")], choices=postCategoryForm(),
                                render_kw={'class': "form-control select-category", 'style': "width:100%",
                                           "title": "分类"}
                                )
    post_tag = SelectMultipleField(validators=[DataRequired("请选择一项!")], choices=postTagForm(),
                                   render_kw={'class': "from-control select-tag", 'multiple': "multiple",  # select2bs4
                                              'data-placeholder': "请选择标签", 'style': "width: 100%;", "title": "标签"}
                                   )
    post_image = StringField(validators=[DataRequired("请填写图片地址！")],
                             render_kw={'class': "form-control", 'placeholder': "请输入图片地址"}
                             )
    """postcontext = TextAreaField(validators=[DataRequired("你写点东西呀！")],
                                render_kw={'class': "form-control", 'placeholder': "请输入内容"}
                                )"""
    submit = SubmitField(label="提交", render_kw={'class': "btn btn-default", 'value': "提交"})


class AdminPostDeleteForm(FlaskForm):
    post_name = StringField(validators=[DataRequired("你要删就删，浪费资源和时间对你和服务器都没好处")],
                            render_kw={"class": "form-control", "placeholder": "请输入文章名进行确认"})
    submit = SubmitField(render_kw={"class": "btn btn-primary btn-block"})


class AdminPostRecommendForm(FlaskForm):
    postcheck = BooleanField(render_kw={"id":"checkboxPrimary3"})
    submit = SubmitField(render_kw={"class":"btn btn-block btn-outline-primary"})

class AdminTagNewForm(FlaskForm):
    tagname = StringField(validators=[DataRequired("你写点东西呀")],render_kw={"class":"form-control","id":"tagNameEdit"})
    submit = SubmitField(render_kw={"class":"btn btn-primary"})

class AdminTagEditForm(FlaskForm):
    tagname = StringField(validators=[DataRequired("你写点东西呀")],render_kw={"class":"form-control","id":"tagNameEdit","placeholder":"标签名"})
    submit = SubmitField(render_kw={"class":"btn btn-primary"})

class AdminTagDeleteForm(FlaskForm):
    tagname = StringField(validators=[DataRequired("你写点东西呀")],render_kw={"class":"form-control","id":"tagNameEdit","placeholder":"标签名"})
    submit = SubmitField(render_kw={"class":"btn btn-primary btn-block"})

class AdminCateNewForm(FlaskForm):
    catename = StringField(validators=[DataRequired("你写点东西呀")],render_kw={"class":"form-control","id":"tagNameEdit","placeholder":"分类名"})
    submit = SubmitField(render_kw={"class":"btn btn-primary"})

class AdminCateEditForm(FlaskForm):
    catename = StringField(validators=[DataRequired("你写点东西呀")],render_kw={"class":"form-control","id":"tagNameEdit","placeholder":"分类名"})
    submit = SubmitField(render_kw={"class":"btn btn-primary"})

class AdminCateDeleteForm(FlaskForm):
    catename = StringField(validators=[DataRequired("你写点东西呀")],render_kw={"class":"form-control","id":"tagNameEdit","placeholder":"分类名"})
    submit = SubmitField(render_kw={"class":"btn btn-primary"})