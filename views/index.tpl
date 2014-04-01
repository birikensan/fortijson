<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
  <meta charset="UTF-8">
  <title>FortiGate parameter-sheet generator</title>
  <link href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css" rel="stylesheet">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
</head>
<body>
    <h1>FortiGate parameter-sheet generator</h1>
    <form action='/forti' method='post' enctype='multipart/form-data'>
    <input type='file' name='file'>
    <input type='submit' value='Convert'>
    </form>
    {% if filename %}
        <p>Link to parameter-sheet is as below</p>
        <a href="./forti/static/{{filename}}.csv">{{ filename}}.csv</a>
    {% endif %}
    <h2>概要</h2>
    <p>　コンフィグファイルをCSV形式のパラメータシートに変換するツールです。現在はFWポリシー（config firewall policy）にのみ対応しています。</p>
    <h2>使い方</h2>
    <ol>
        <li>[参照]ボタンを押下して、パラメータシートに変換したいコンフィグファイルを選びます。</li>
        <li>[Convert]ボタンを押下します。すると、パラメータシートのリンクが表示されます。</li>
        <li>表示されたリンクを選択して、変換後のパラメータシートを入手します。</p>
    </ol>
    <h2>注意</h2>
    <ol>
        <li>以下のコンフィグは非対応です。</li>
            <ul>
                <li>VDOMを利用しているコンフィグ。（コンフィグをそれぞれのFWに分けたファイルをご利用下さい。）</li>
            </ul>
    </ol>
</body>
</html>
