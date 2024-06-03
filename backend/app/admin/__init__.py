from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

# @admin_bp.route('/')
# def index():
#     return 'admin'

from ..auth.login import *
from ..auth.logout import *
from .blockUser import *
from .listUsers import *
from .listBooks import *
from .newBook import *
from .getBook import *
from .editBook import *
from .deleteBook import *