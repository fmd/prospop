### Django Imports ###
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import Template, Context
from django.http import HttpResponse

import logging
logger = logging.getLogger(__name__)

### Our Imports ###
from prospapp.models import *
from docker import *