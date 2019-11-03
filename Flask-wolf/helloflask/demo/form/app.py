from flask import Flask, render_template, flash, redirect, url_for
from forms import LoginForm, FortyTwoForm
app = Flask(__name__)
app.secret_key = 'guess'
'''
设置错误信息的中文提示
1.配置WTF_I18N_ENABLED 为False
2.配置FlaskForm的Meta类中的locals属性
'''
app.config['WTF_I18N_ENABLED'] = False


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
