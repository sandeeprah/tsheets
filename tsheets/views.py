from flask import request, render_template, jsonify, abort, make_response, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

from application import app, db
from application.models import User
