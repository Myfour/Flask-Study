from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError


class MyBaseForm(FlaskForm):
    class Meta:
        locals = ['zh']


class LoginForm(MyBaseForm):
    username = StringField('Username',
                           validators=[DataRequired()],
                           render_kw={'placeholder': 'Your Username'})
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


'''
为表单渲染的字段的HTML代码添加属性的两种方式：
1.在Form类设置某个属性时使用render_kw参数来设置

username = StringField('Username',
                           validators=[DataRequired()],
                           render_kw={'placeholder': 'Your Username'})


2.实例化表单类的某个属性字段时传入
loginform.username(style='width: 200px;', class_='bar')  # 注意class属性是关键字所以加了一个下划线
'''
'''
自定义行内验证器
就是在Form类中定义一个validate_开头后面是对应验证字段名的方法
'''

# class FortyTwoForm(FlaskForm):
#     answer = IntegerField('The Number')
#     submit = SubmitField()

#     def validate_answer(self, field):
#         if field.data != 42:
#             raise ValidationError('Must be 42')
'''
全局验证器
表单字段的validator参数传入的需要是可调用对象
'''


def is_42(message=None):
    if not message:
        message = 'Must be 42'

    def _is_42(form, field):
        print(form, field)
        if field.data != 42:
            raise ValidationError(message)

    return _is_42


class FortyTwoForm(FlaskForm):
    answer = IntegerField('The Number', validators=[is_42('必须是42')])
    submit = SubmitField()