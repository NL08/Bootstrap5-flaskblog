# random number generator
import uuid
from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename
from app.main.forms import FileForm
from app.models import Posts, User

main = Blueprint('main', __name__, template_folder='templates')

 

@main.route("/")
@main.route("/home")
def home():  
    posts_db = db.session.scalars(db.select(Posts)).all()
    return render_template('home.html', posts_db=posts_db, title='home')  

@main.route("/about")
def about():
    return render_template('about.html', title='register')


@main.route('/profile/<string:username>', methods = ['GET'])
def profile(username): 
    user = db.one_or_404(db.select(User).filter_by(username=username))
    return render_template('profile.html', title='profile', user=user)

import os

from app import db


@main.route('/upload_picture', methods=['GET', 'POST'])
def upload_picture():
    if not current_user.is_authenticated:
        return redirect(url_for('main.home')) 
    
    form = FileForm()
    if form.validate_on_submit():
        picture_filename = form.image_filename.data     
        # Make file secure...         
        # This makes sure the filename is safe
        filename_is_secure = secure_filename(picture_filename.filename)
        # make the file unique incase someone uploads the same name
        # uuid is a random number generator
        unique_filename = str(uuid.uuid1()) + filename_is_secure
        upload = User(profile_pic_name=unique_filename)
        db.session.add(upload)
        db.session.commit()
        # save file to a secure location
        picture_filename.save((os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)))  
        flash("You have succesfully uploaded your profile picture.")
        return redirect(url_for('main.profile', username=current_user.username)) # double check this

    return render_template('upload_picture.html', form=form, title='upload Profile Picture') 


from app.main.forms import SearchForm
@main.route('/search', methods= ['GET', 'POST'])
def search():  
    # The variable name is "searchform" and not "form" because in the html I would have 2 "form" variables
    searchform = SearchForm()    
    if searchform.validate_on_submit():

        search_input = searchform.search_input.data      
        search_results = db.session.query(Posts).filter(Posts.content.ilike(f'%{search_input}%')).order_by(Posts.title).all()
        return render_template('search.html', searchform=searchform, search_results=search_results)
    




