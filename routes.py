from flask import render_template, Flask, request
from models import db
from forms import SignupForm
#import cv2
#from vad import visualize
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://localhost/lflask'
db.init_app(app)
app.secret_key="development_key"
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/button_callback")
def button_callback():
    return "Sorting"

@app.route("/hello")
def hello():
    return render_template("hello.html")
@app.route("/")
def post():
    return render_template("post.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        return "success"
    elif request.method == 'GET':
        return render_template("signup.html", form=form)



@app.route("/vad")
def vad():
    #from vad import images_list,images_list,classes_str_list,probability
    #cv2.imshow(visualize)
    from vad import visualize, res, b, c
    print(res,b,c)
    return ''

if __name__== "__main__":
    app.run(debug=True)