from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Posts, User
from app.postinfo.forms import Emptyform, Postform

''' 
# todo turn into a database why is there no post number like 1st post ever posted in general etc?
posts = {   
    "username": "author",
    "author": "Bobby Bobson",
    "Title": "Hello World",
    "Content": "This is a post content 1",
    "date_posted": "March 17 2021" 
}
'''
postinfo = Blueprint('postinfo', __name__, template_folder='templates')

@postinfo.route("/post/new", methods = ['POST', 'GET'])
@login_required
# I need to link to the name of the function in the html. Ex new_post 
def new_post(): 
    form = Postform()
    if form.validate_on_submit():
        title_form = form.title.data
        content_form = form.content.data
        date_posted_form = datetime.now()
        # user.id is used in the FK in the Post database. You need to manually add FK's.   
        user_db = db.session.execute(db.select(User).filter_by(username=current_user.username)).scalar_one_or_none()
        user_db_id = user_db.id
        posts = Posts(title=title_form, content=content_form, date_posted=date_posted_form, fk_user_id=user_db_id )  
        db.session.add(posts)  
        db.session.commit()          
        flash('You have posted successfully') 
        # redirect to the post after complete because you want to see the posted post. 
        return redirect(url_for('main.home'))
    return render_template('new_post.html',title='new post', form=form)



# gives you the ability to click on a post and view it 
# get the unique post from the post id
@postinfo.route("/post/<int:post_id_db>", methods = ['POST', 'GET'])
@login_required
def post(post_id_db):
    post_db = db.get_or_404(Posts, post_id_db)
    post_id_db = post_db.id

    user_db = db.one_or_404(db.select(User).filter_by(username=current_user.username))
    form = Emptyform()    
    # Do I need to pass on post_id 
    return render_template('post.html', title='post', form=form,post_db=post_db, post_id_db=post_id_db, user_db=user_db)





# The reason you have post_id is because you only want to edit 1 post at a time. 
# If you leave out post_id you would edit every posts. 
@postinfo.route("/post/edit/<int:post_id_db>", methods = ['POST', 'GET'])
# edit/update posts
@login_required
def edit_post(post_id_db): 
    # get request
    post_db = db.one_or_404(db.select(Posts).filter_by(id=post_id_db))  
    form = Postform()
    if form.validate_on_submit():
        # delete the current columns in db
        delete_post = post_db
         
        db.session.delete(delete_post)  
        db.session.commit()
        # add/edit the current forms in the db
        title_form = form.title.data
        content_form = form.content.data 
        posts = Posts(title=title_form, content=content_form ,fk_user_id=current_user.id)
        db.session.add(posts)  
        db.session.commit()
        flash('You have edited your post successfully')
        return redirect(url_for('main.home'))
      # put this below the if statement so for ex "form.title.data" doesn't interfere with above ex "form.title.data
    elif request.method == 'GET':        
       
        post_title_db = post_db.title
        post_content_db = post_db.content
        # the code below renders a form with text already in the form
        form.title.data =  post_title_db 
        form.content.data = post_content_db
        return render_template('edit_post.html', title='edit post', form=form) 






# Can I go ("/post/<int:post_id>/delete") instead of below? No
@postinfo.route("/post/delete/<int:post_id_db>", methods = ['POST'])
@login_required
def delete_post(post_id_db): 
    if request.method == 'POST':       
        post_db = db.one_or_404(db.select(Posts).filter_by(id=post_id_db))  
        delete_post = post_db
        db.session.delete(delete_post)
        db.session.commit()
        flash('You have deleted your post')
        return redirect(url_for('main.home'))
    





















