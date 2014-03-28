<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
  <meta charset="UTF-8">
  <title>FortiGate parameter-sheet generator</title>
  <link href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css" rel="stylesheet">
  <link href="//aimless.jp/gohan/static/style.css" rel="stylesheet">
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
        <p>is as below</p>
        <a href="./forti/static/{{filename}}.csv">{{ filename}}.csv</a>
    {% endif %}
</body>
</html>
