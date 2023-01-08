import json
from urllib.request import urlopen
from random import shuffle
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    """初期画面を表示します."""
    return render_template("index.html")

@app.route("/api/recommend_article")
def api_recommend_article():
    #  Get a html.
    with urlopen( "http://feeds.feedburner.com/hatena/b/hotentry" ) as res:
        html = res.read().decode( "utf-8")
    # 2. Load a html by BeautifulSoup.
    soup = BeautifulSoup(html, "html.parser" )

    # 3. Get items you want.
    # 記事一覧を取得する
    items = soup.select( "item")
    #  ランダムに1件取得する
    shuffle(items)
    item = items[0]
    # 5. 以下の形式で返却する.
                # {
                #     "content" : "記事のタイトル",
                #     "link" : "記事のURL"
                # }
    print(item)
    return json.dumps({
            "content" : item.find("title").string,
            "link" : item.get('rdf:about')
    })

if __name__ == "__main__":
    app.run(debug=True, port=5004)
