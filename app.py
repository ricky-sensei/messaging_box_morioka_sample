from flask import Flask, flash, redirect, render_template, request, url_for  # url_forを追加
from flask_login import LoginManager, current_user, login_required, login_user, logout_user # ログインが必要な処理に対するラッパー
from werkzeug.security import generate_password_hash, check_password_hash  
from peewee import IntegrityError  # ユーザー登録エラー
from config import User

app = Flask(__name__)
app.secret_key = "secret"


login_manager = LoginManager()  
login_manager.init_app(app)     


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


# ログインせずログイン必須のページに飛ぼうとしたとき
@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login"))  # login.htmlにリダイレクト url_forに変更


@app.route("/register", methods=["GET", "POST"])  
def register():
    if request.method == "POST":
        if not request.form["name"] or not request.form["password"] or not request.form["email"]:
            flash("未入力の項目があります。")
            return redirect(request.url)
        if User.select().where(User.name == request.form["name"]):
            flash("その名前はすでに使われています。")
            return redirect(request.url)
        if User.select().where(User.email == request.form["email"]):
            flash("そのメールアドレスはすでに使われています。")
            return redirect(request.url)

        try:  # ユーザー登録エラーの例外処理
            User.create(  # エラーになりうる処理
                name=request.form["name"],
                email=request.form["email"],
                password=generate_password_hash(request.form["password"])
            )
        except IntegrityError as e:  # IntegrityError(整合性エラー)が出たとき
            flash(f"{e}")
        return render_template("index.html")  # url_forに変更
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not request.form["password"] or not request.form["email"]:
            flash("未入力の項目があります")
            return redirect(request.url)
        user = User.select().where(User.email == request.form["email"]).first()  
        if user is not None and check_password_hash(user.password, request.form["password"]):  
            login_user(user)
            flash(f"ようこそ！{user.name}さん")  
            return redirect(url_for("index")) # url_forに変更
        flash("認証に失敗しました")
    return render_template('login.html')


# ログアウト処理
@app.route('/logout')
@login_required  # ログインしていないとログアウトできない
def logout():
    logout_user()
    flash("ログアウトしました!")
    return redirect(url_for("index"))  # url_forに変更


# ユーザー削除処理
@app.route('/unregister')
@login_required  # ログインしていないとユーザー削除できない
def unregister():
    current_user.delete_instance()
    logout_user()
    return redirect(url_for("index"))  # url_forに変更


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
