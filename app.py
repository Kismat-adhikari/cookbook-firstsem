from flask import Flask, render_template,session,request,url_for, redirect

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup', methods = ['GET','POST'])
def signup():
    # this takeas the data from the user from the form
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        nickname = request.form.get('nickname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        experience = request.form.get('experience')
        cook_type = request.form.get('cook_type')


  
        return redirect(url_for("welcome"))


    return render_template('signup.html')

@app.route('/welcome')
def welcome():
    # this takes the data from the user or thier info to later print it out in the respective pages
    name = session.get('name')
    nickname = session.get('nickname')
    email = session.get('email')
    phone = session.get('phone')
    experience = session.get('experience')
    cook_type = session.get('cook_type')

    return render_template('welcome.html', name=name,email=email,nickname=nickname,experience=experience,cook_type=cook_type)


if __name__ == '__main__':
    app.run(debug=True)