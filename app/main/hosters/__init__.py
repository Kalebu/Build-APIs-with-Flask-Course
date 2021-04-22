from flask import Blueprint, request
from main.models import db

hosters_bp = Blueprint(
    "hosters_bp",
    __name__,
    url_prefix='/'
)


@hosters_bp.route('hosters')
def hosters():
    return {
        'response': "This hosters bp"
    }
