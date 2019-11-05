from flask import render_template, url_for, redirect, flash
from sayhello import app, db
from sayhello.models import Message
from sayhello.forms import HelloForm


@app.route('/', methods=['GET', 'POST'])
def index():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(name=name, body=body)
        db.session.add(message)
        db.session.commit()
        flash('Your message have been sent to the world !')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, messages=messages)
