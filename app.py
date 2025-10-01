# postリクエストを受け取れるようにrequestをついか
# 不正な値を入力した場合にリダイレクトするためにredirectを追加
# フラッシュメッセージを出すためにflash,  を追加
from flask import Flask, flash, redirect, render_template, request  
from werkzeug.security import generate_password_hash  # パスワードのハッシュ化
from config import User

app = Flask(__name__)
# flashメッセージ表示のためのシークレットキー
app.secret_key = "secret"



# ユーザー登録フォームのルーティングを作成
@app.route("/register", methods=["GET", "POST"])  # postリクエストを受け取れるようにする
def register():
    # リクエストメソッドがPOSTだったとき->index.html
    if request.method == "POST":
        # 空のデータが入力された場合
        if not request.form["name"] or request.form["password"] or request.form["email"]:
            # フラッシュメッセージをregisterテンプレートに送る
            flash("未入力の項目があります。")
            return redirect(request.url)
        
        # データの重複があった場合(name, email)
        if User.select().where(User.name == request.form["name"]):  # dbに同じ名前が存在したら
            # フラッシュメッセージをregisterテンプレートに送る
            flash("その名前はすでに使われています。")
            return redirect(request.url)

        if User.select().where(User.email == request.form["email"]):  # dbに同じemailが存在したら
            # フラッシュメッセージをregisterテンプレートに送る
            flash("そのメールアドレスはすでに使われています。")
            return redirect(request.url)

        # ユーザーをデータベースに追加:Create
        User.create(
            name=request.form["name"],
            email=request.form["email"],
            password=generate_password_hash(request.form["password"]),  # パスワードのハッシュ化
        )
        return render_template("index.html")

    # リクエストメソッドがGETだったとき->register.html
    return render_template("register.html")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
