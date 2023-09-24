from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import phonenumbers


class LoginForm(FlaskForm):
    phone = StringField('phone', validators=[DataRequired()],
                        render_kw={'placeholder': 'Phone format is '
                                                  '+7XXXXXXXXXX'})
    password = PasswordField('password', validators=[DataRequired()],
                             render_kw={'placeholder': 'Password'})
    submit = SubmitField('Войти')


class ProfileForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()],
                        render_kw={'placeholder': 'First_name'}),
    login = StringField('login', validators=[DataRequired()],
                        render_kw={'placeholder': 'Login '}),
    phone = StringField('phone', validators=[DataRequired()],
                        render_kw={'placeholder': 'Phone format is '
                                                  '+7XXXXXXXXXX'})


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()],)
    text = StringField('text', validators=[DataRequired()],)
    phone = StringField('phone', validators=[DataRequired()])
    submit = SubmitField('Отправить')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
