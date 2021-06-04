VsCode started using tabs all of a sudden
https://stackoverflow.com/questions/33974681/how-can-i-convert-tabs-to-spaces-and-vice-versa-in-an-existing-file

npx create-react-app frontend

yarn build

yarn start

https://stackoverflow.com/questions/54974483/flask-render-template-is-returning-a-string-instead-of-html-document

I have the same problem, none of the answers help. I am using Flask-Restful. I have tried each of the commented-out solutions below:

```
class Root(Resource):
  def get(self):
    # return send_file(filename_or_fp=settings.STATIC_FOLDER+'/index.html') 
    # return app.send_static_file('index.html')
    # return send_from_directory(app.static_folder, 'index.html')
    # return render_template('index.html')
    response = make_response(render_template('test.html'))
    response.headers['content-type'] = 'text/html'
    return response
```

When I replace 'index.html' with 'test.html' (another file in the same folder with it's only contents being ```text```). Each of these solutions works.

But when I try to return index.html I either get ```null``` or in the case of return render_template('index.html') I get the entire index.html as a string.


After trying to serve with nginx directly, html was sent, but got js/css error where all requests return the same index.html file:
The stylesheet https://tyeshutty.tk/static/css/main.8c8b27cf.chunk.css was not loaded because its MIME type, “text/html”, is not “text/css”.
