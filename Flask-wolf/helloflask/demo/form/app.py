from flask import Flask, render_template, flash, redirect, url_for, request, session, send_from_directory
from forms import LoginForm, FortyTwoForm, UploadForm, MultiUploadForm, RichTextForm, NewPostForm, RegisterForm, SigninForm
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
import os
import uuid
from flask_ckeditor import CKEditor
app = Flask(__name__)
app.secret_key = 'guess'
ckeditor = CKEditor(app)
app.config['CKEDITOR_SERVER_LOCAL'] = True
'''
设置错误信息的中文提示
1.配置WTF_I18N_ENABLED 为False
2.配置FlaskForm的Meta类中的locals属性
'''
app.config['WTF_I18N_ENABLED'] = False
'''
配置可以上传的文件的大小
'''
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024  # 3M


@app.route('/basic', methods=['GET', 'POST'])
def basic():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Welcome,' + form.username.data)
        return redirect(url_for('basic'))
    return render_template('basic.html', form=form)


'''
获取验证成功后的数据:
form.username.data
获取验证失败的错误提示：
1.
form.errors
2.
form.username.errors
'''
@app.route('/validate_test', methods=['GET', 'POST'])
def validate_test():
    form = FortyTwoForm()
    if form.validate_on_submit():
        return redirect(url_for('validate_test'))

    return render_template('validate_test.html', form=form)


'''
文件上传
一定到设置form标签的属性 enctype="multipart/form-data"
'''
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config.get('UPLOAD_PATH'), filename))
        flash('upload success')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))
        return 'success'
    return render_template('upload.html', form=form)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# 这个配置是多文件上传中需要用到的
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'gif']


@app.route('/multi-upload', methods=['GET', 'POST'])
def multi_upload():
    form = MultiUploadForm()
    if request.method == 'POST':
        filenames = []
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CSRF token error')
            return redirect(url_for('multi-upload'))
        if 'photo' not in request.files:
            flash('This field is required')
            return redirect(url_for('multi-upload'))

        for f in request.files.getlist('photo'):
            if f and allowed_file(f.filename):
                filename = random_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                filenames.append(filename)
            else:
                flash('Invalid file type.')
                return redirect(url_for('multi_upload'))
        flash('Upload success.')
        session['filenames'] = filenames
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)


# 显示图片
@app.route('/uploads/<path:filename>')
def get_file(filename):
    re = send_from_directory(app.config['UPLOAD_PATH'], filename)
    return re


@app.route('/show_images')
def show_images():
    return render_template('loaded.html')


@app.route('/richtext')
def richtext():
    form = RichTextForm()
    return render_template('ckeditor.html', form=form)


'''
多Submit按键
当你点击提交按钮时，所有submit按钮都被提交，
其结果被bool表示，点击了的为True其他为False，可通过True判断点击了谁
'''
@app.route('/twobutton', methods=['GET', 'POST'])
def twobutton():
    form = NewPostForm()
    if form.validate_on_submit():
        print(form.data)
        if form.save.data:
            flash('You clicked Save')
        elif form.publish.data:
            flash('You clicked Publish')
    return render_template('2button.html', form=form)


'''
同一页面多表单提交
Flask-WTF根据请求方法判断表单是否提
交，但并不判断是哪个表单被提交，所以我们需要手动判断
需要分别判断submit跟不同表单的验证，否则提交其中一个时会出现另一个表单也被提交了
'''
@app.route('/manyform', methods=['GET', 'POST'])
def manyform():
    register_form = RegisterForm()
    login_form = SigninForm()
    # if register_form.validate_on_submit():
    if register_form.submit2.data and register_form.validate():
        flash('you just submit the register Form.')
        print(register_form.data)
        print(login_form.data)
    # if login_form.validate_on_submit():
    if login_form.submit1.data and login_form.validate():
        flash('you just submit the Login Form.')
        print(register_form.data)
        print(login_form.data)
    return render_template('manyform.html',
                           register_form=register_form,
                           login_form=login_form)
