from flask import render_template, flash, redirect,request,session,url_for
from app import accounts
from app import app
# index view function suppressed for brevity
@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if(request.args):
        id = request.args['id']
        pw = request.args['pw']
        if(accounts.login_Check(id,pw)):
            flash('Login Successful!')
            session['id'] = request.args['id']
            session['name'] = accounts.login_Check(id,pw)['name']
            if session.get('id'):
                user={'id':session.get('id'),
                      'name': session.get('name')}
            else:
                user={'id':'','name':''}
            return render_template("index.html",
                title = 'Home',
                user = user)
        else:
            user = {'id': '', 'name': ''}
            flash('Login Failed!')
            return render_template('login.html',
                                   title='Sign In',
                                   user=user)
    else:
        if session.get('id'):
            user = {'id': session.get('id'),
                    'name': session.get('name')}
        else:
            user = {'id': '', 'name': ''}
        return render_template("index.html",
                               title='Home',
                               user=user)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    user = {'id': '', 'name': ''}
    return render_template('login.html',
                title = 'Sign In',
                user=user)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if (request.args):
        id = request.args['id']
        name = request.args['name']
        pw = request.args['pw']
        if (accounts.Register(id, name,pw)==True):
            flash('Register Successful!')
            user = {'id': '', 'name': ''}
            return render_template("login.html",
                                   title='Sign In',
                                   user=user)
        else:
            user = {'id': '', 'name': ''}
            flash('Register Failed!'+str(accounts.Register(id, name,pw)))
            return render_template('register.html',
                                   title='Register',
                                   user=user)
    else:
        if session.get('id'):
            user = {'id': session.get('id'),
                    'name': session.get('name')}
        else:
            user = {'id': '', 'name': ''}
        return render_template('register.html',
                title = 'Register',
                user=user)

@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('name', None)
    return redirect(url_for('index'))

@app.route('/directory')
def directory():
    articles = accounts.getPost()
    if session.get('id'):
        user = {'id': session.get('id'),
                'name': session.get('name')}
    else:
        user = {'id': '', 'name': ''}
    return render_template("directory.html",
        title = 'Directory',
        user = user,
        articles=articles)



@app.route("/directory/<art_name>")
def art(art_name):
        articles = accounts.getPost()
        comments = accounts.getComment(art_name)
        if session.get('id'):
            user = {'id': session.get('id'),
                    'name': session.get('name')}
        else:
            user = {'id': '', 'name': ''}
        for article in articles:
            if article['name']==art_name:
                return render_template("article.html",
                        title = art_name,
                        user = user,
                        article=article,
                        comments=comments)
        flash('No such article!')
        return render_template("directory.html",
                                       title='Directory',
                                       user=user,
                                       articles=articles)


@app.route('/post', methods = ['GET', 'POST'])
def post():
        if (request.args):
            if session.get('id') and session.get('id') == 'Driver':
                user = {'id': session.get('id'),
                        'name': session.get('name')}
                name = request.args['name']
                content = request.args['content']
                if (accounts.Post(name,content) == True):
                    flash('Post Successful!')
                    return render_template("post.html",
                                           title='Post',
                                           user=user)
                else:
                    flash('Post Failed!')
                    return render_template('post.html',
                                           title='Post',
                                           user=user)
            else:
                if session.get('id'):
                    user = {'id': session.get('id'),
                            'name': session.get('name')}
                else:
                    user = {'id': '', 'name': ''}
                flash("You don't have permission!")
                return render_template('post.html',
                                       title='Post',
                                       user=user)
        else:
            if session.get('id'):
                user = {'id': session.get('id'),
                'name': session.get('name')}
            else:
                user={'id':'','name':''}
            return render_template('post.html',
                    title = 'Post',
                    user=user)


@app.route('/directory/<art_name>/delete')
def delete(art_name):
        articles = accounts.getPost()
        if session.get('id') and session.get('id') == 'Driver':
                user = {'id': session.get('id'),
                        'name': session.get('name')}
                if (accounts.delete_Post(art_name) == True):
                    flash('Delete Successful!')
                    articles = accounts.getPost()
                    return render_template("directory.html",
                                           title='Directory',
                                           user=user,
                                           articles=articles)
                else:
                    flash('Delete Failed!')
                    return render_template("directory.html",
                                           title='Directory',
                                           user=user,
                                           articles=articles)
        else:
                if session.get('id'):
                    user = {'id': session.get('id'),
                            'name': session.get('name')}
                else:
                    user = {'id': '', 'name': ''}
                flash("You don't have permission!")
                return render_template("directory.html",
                                       title='Directory',
                                       user=user,
                                       articles=articles)


@app.route('/directory/<art_name>/comment', methods = ['GET','POST'])
def comment(art_name):
            if session.get('id'):
                user = {'id': session.get('id'),
                        'name': session.get('name')}
                name = session.get('name')
                content = request.args['comment']
                if (accounts.Comment(art_name,name,content) == True):
                    flash('Comment Successful!')
                    return art(art_name)
                else:
                    flash('Comment Failed!')
                    return art(art_name)
            else:
                flash("You don't have permission!")
                user = {'id': '', 'name': ''}
                return render_template('login.html',
                                       title='Sign In',
                                       user=user)
@app.route('/directory/<art_name>/edit', methods = ['GET', 'POST'])
def edit(art_name):
        if (request.args):
            if session.get('id') and session.get('id') == 'Driver':
                user = {'id': session.get('id'),
                        'name': session.get('name')}
                content = request.args['content']
                if (accounts.Edit(art_name,content) == True):
                    flash('Edit Successful!')
                    return art(art_name)
                else:
                    flash('Edit Failed!')
                    return art(art_name)
            else:
                if session.get('id'):
                    user = {'id': session.get('id'),
                            'name': session.get('name')}
                else:
                    user = {'id': '', 'name': ''}
                flash("You don't have permission!")
                return art(art_name)
        else:
            if session.get('id'):
                user = {'id': session.get('id'),
                'name': session.get('name')}
            else:
                user={'id':'','name':''}
            return render_template('edit.html',
                    title = 'Edit-'+art_name,
                    user=user,
                    art_name=art_name)