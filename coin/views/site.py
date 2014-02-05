from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_user, current_user, login_required, logout_user
import json

site = Blueprint('site', __name__)

@site.route('/')
def index():
  return render_template('index.html')

@site.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('site.index'))

@site.route('/<path:path>')
@login_required
def logged_in_view(path):
  return render_template('index.html', user=json.dumps(current_user.get_public_data()))

