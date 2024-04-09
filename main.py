from flask import Flask, render_template

app = Flask('App')

@app.route('/')
def home():
    return render_template('page.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


app.run(debug=True)