import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from db.py import(
    get_resident_info_name,get_resident_info_identity,get_resident_info_region
)
bp = Blueprint('CDC', __name__)