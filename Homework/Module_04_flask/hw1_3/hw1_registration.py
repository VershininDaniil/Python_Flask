from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, Email, Optional, NumberRange
from hw2_validators import number_length, NumberLength

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"  # требуется для WTForms
app.config["WTF_CSRF_ENABLED"] = False


class RegistrationForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    phone = IntegerField(
        validators=[
            InputRequired(),
            number_length(min=10, max=10, message="Номер телефона должен содержать 10 цифр"),
            NumberLength(min=10, max=10, message="Номер телефона должен содержать 10 цифр")
        ]
    )
    name = StringField(validators=[InputRequired()])
    address = StringField(validators=[InputRequired()])
    index = IntegerField(validators=[InputRequired(), NumberRange(min=0, message="Индекс должен быть положительным числом")])
    comment = StringField(validators=[Optional()])


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data
        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.run(debug=True)