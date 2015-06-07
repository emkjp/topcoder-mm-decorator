# topcoder-mm-decorator
マラソンマッチのStandingを加工して出力します。

## 必要なもの

+ python 2.7+

## 依存ライブラリ

`pip` または `easy_install` で以下のモジュールをインストールしてください。

+ lxml
+ mako
+ mpmath
+ urllib2

## 使い方（サンプル）

```
usage: tc_mm_decorater.py [-h] [-u] [-t REFRESH_TIME] [-r ROUND_ID] [-T TITLE] [-d DIR]
```

最初の実行は Coder のデータをFeedから取得するため、やや時間がかかります。

デフォルトで ./{ROUND_ID} ディレクトリにHTMLが出力されます。

### TCO2015 Round2 Standing を加工する場合

デフォルトで 1800 秒毎にHTMLが更新されます。

```
python tc_mm_decorater.py -r 16471 --title "TCO2015 Round2"
```

