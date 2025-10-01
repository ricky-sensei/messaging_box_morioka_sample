from flask import Flask, flash, redirect, render_template, request  
from flask_login import LoginManager, login_user # ログイン関連
from werkzeug.security import generate_password_hash, check_password_hash  # 入力されたｐｗとＤＢ上のｐｗを比較
from config import User

app = Flask(__name__)
app.secret_key = "secret"

# LoginManagerの設定
login_manager = LoginManager()  # LoginManagerのインスタンス化
login_manager.init_app(app)     # appのログイン情報を初期化

# ユーザー情報を取得するためのメソッド
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)





@app.route("/register", methods=["GET", "POST"])  
def register():
    
    if request.method == "POST":
        
        if not request.form["name"] or request.form["password"] or request.form["email"]:
            flash("未入力の項目があります。")
            return redirect(request.url)
        
        
        if User.select().where(User.name == request.form["name"]):  
            
            flash("その名前はすでに使われています。")
            return redirect(request.url)

        if User.select().where(User.email == request.form["email"]):  
            
            flash("そのメールアドレスはすでに使われています。")
            return redirect(request.url)

        
        User.create(
            name=request.form["name"],
            email=request.form["email"],
            password=generate_password_hash(request.form["password"])
        )
        return render_template("index.html")

    
    return render_template("register.html")


# login用のルーティングを作成
@app.route('/login', methods=["GET", "POST"])
def login():
    # postリクエストのときに
    if request.method == "POST":
        # 未入力処理
        if not request.form["password"] or not request.form["email"]:
            flash("未入力の項目があります")
            return redirect(request.url)
        
        # ユーザー認証
        user = User.select().where(User.email == request.form["email"]).first()  # メールアドレスが合致するユーザーの最初のレコード
        if user is not None and check_password_hash(user.password, request.form["password"]):  # 合致するレコードが存在していて、パスワードがＤＢのものと合致した場合
            login_user(user)  # ログイン処理
            flash(f"ようこそ！{user.name}さん")  # フラッシュメッセージ
            return redirect("/")  # index.htmlを表示

        # 認証失敗のときのフラッシュメッセージ
        flash("認証に失敗しました")
        
        
    return render_template('login.html')


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
