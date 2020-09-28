import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation
import mailroom

app = Flask(__name__)
# app.secret_key = b'\x9d\xb1u\x08%\xe0\xd0p\x9bEL\xf8JC\xa3\xf4J(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'
app.secret_key = os.environ.get('SECRET_KEY').encode()
# print(app.secret_key)


@app.route('/')
def home():
    """
    Function to display homepage
    """
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    """
    Function to display all donations, extended from homepage
    """
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    """
    Function to add donor and donation
    """
    if request.method == 'POST':
        mailroom.check_donor(request.form['donor'], request.form['value'])
        return redirect(url_for('all'))
    else:
        return render_template('create.jinja2')


@app.route('/single_donor/', methods=['GET', 'POST'])
def single_donor():
    """
    Function to display donations for a single donor
    """
    if request.method == 'POST':
        view_single_donor = mailroom.view_donations(request.form['donor'])
        if view_single_donor is False:
            return render_template('single_donor.jinja2')
        return render_template('donations.jinja2', donations=view_single_donor)
    else:
        return render_template('single_donor.jinja2')
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port, debug=True)

