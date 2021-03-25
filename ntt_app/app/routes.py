from flask import render_template,flash,redirect,url_for,request,abort
from app import app,db,login
from app.models import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required,login_manager,current_user,login_user,logout_user
from app.forms import LoginForm,RegistrationForm,PostForm,ApproveForm


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

login.login_view = 'login'




@app.route('/')
@app.route('/index')
@login_required
def index():
    role=Role.query.filter_by(name='Admin')
    if (role.count()>0):
        role=role.first()
        role_id=UserRoles.query.filter_by(user_id=current_user.id,role_id=role.id)
        admin=False
        if (role_id.count()>0):
            admin=True
            posts=Post.query.all()
        else:
            posts=Post.query.filter_by(user_id=current_user.id)
            
        return render_template('index.html', title='Home', posts=posts,admin=admin)
    abort(500)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form=PostForm()
    if request.method=='POST':
        post= Post(title=form.title.data,body=form.body.data,user_id=current_user.id)
        db.session.add(post)
        db.session.commit()       
        return (redirect(url_for('index'))) 
    else:
        return render_template('create.html', title='Create post', form=form)
    



@app.route('/view/<page_id>', methods=['GET', 'POST'])
@login_required
def view(page_id):
    role=Role.query.filter_by(name='Admin')
    if (role.count()>0):
        role=role.first()
        role_id=UserRoles.query.filter_by(user_id=current_user.id,role_id=role.id)
        admin=False
        if (role_id.count()>0):
            admin=True
    if request.method=='POST':
        form=ApproveForm()
        post=Post.query.filter_by(id=page_id).first()
        post.approved=form.approve.data
        db.session.commit()
        flash("Post " + str(post.title)+" has been approved")
        return (redirect(url_for('index'))) 
    else:
        form=ApproveForm()
        post=Post.query.filter_by(id=page_id)
        if post.count()==1:
            print (page_id)
            return render_template('view.html',post=post.first(),form=form,admin=admin)
        else:
            abort(404)
