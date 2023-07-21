from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import phonenumbers


class LoginForm(FlaskForm):
    phone = StringField('phone', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Войти')


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
