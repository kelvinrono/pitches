from flask import Blueprint
auth=Blueprint('auth',__name__)
from . import auth
from . import views, forms
