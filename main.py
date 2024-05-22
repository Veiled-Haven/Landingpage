import os
from flask import Flask, render_template, request, redirect, url_for
from discord_webhook import DiscordWebhook, DiscordEmbed
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange

webhook_url = os.environ.get('DISCORD_WEBHOOK_URL', "")

app = Flask(__name__,static_url_path='',static_folder='static/',template_folder='templates/')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap4(app)

class ApplicationForm(FlaskForm):
    minecraft_username = StringField("What is your Minecraft username?*",description="We need this information to eventually Whitelist you on the Server!", validators=[DataRequired()])
    discord_username = StringField("What is your Discord username?*", description="<b>Please make sure you accept Friend Requests</b>, Discord is where we will get in touch with you!", validators=[DataRequired()])
    why_would_you_like_to_join = TextAreaField("Why would you like to join?*", validators=[DataRequired()])
    favorite_aspect = TextAreaField("What is your favorite aspect of playing Minecraft online?*", validators=[DataRequired()])
    how_long_have_you_played = TextAreaField("How long have you been playing Minecraft?", validators=[DataRequired()])
    have_you_been_part_of_an_smp = TextAreaField("Have you been part of any SMP's before, if so why did you leave?", validators=[DataRequired()])
    age = IntegerField("What is your age?*", validators=[DataRequired(),NumberRange(min=16,max=200,message="Sorry, you are to Young to play with us :(")])
    rules_accepted = BooleanField("Do you accept the Rules?", validators=[DataRequired()])
    submit = SubmitField()


@app.route("/", methods=["GET", "POST"])
def home():
    form = ApplicationForm()
    if request.method == "POST" and form.validate_on_submit(): #on form submission
        webhook = DiscordWebhook(url=webhook_url)
        embed = DiscordEmbed(title='Form Submission')
        print(form.data)
        for form_field in form.data:
            print(f"{form_field}: {form.data[form_field]}")
            embed.add_embed_field(name=form_field, value=form.data[form_field])
               # add embed object to webhook
        webhook.add_embed(embed)
        if webhook_url != "":
            response = webhook.execute()
        return redirect(location=url_for("success"),code=302)
    else:
        return render_template("index.html", form=form,anchor='application')


@app.route("/success")
def success():
    return render_template("success.html")

app.run(host='0.0.0.0', port=5000)
