from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"

def create_db():
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS links
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, content TEXT, expire_at DATETIME)''')
    conn.commit()
    conn.close()



def add_link(category, content, expire_at):
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    c.execute('''INSERT INTO links (category, content, expire_at) VALUES (?, ?, ?)''', (category, content, expire_at))
    conn.commit()
    conn.close()

def get_active_links():
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    c.execute('''SELECT category, content FROM links WHERE expire_at > ?''', (datetime.datetime.now(),))
    active_links = c.fetchall()
    conn.close()

    categorized_links = {}
    for category, content in active_links:
        if category in categorized_links:
            categorized_links[category].append(content)
        else:
            categorized_links[category] = [content]
    return categorized_links



def delete_expired_links():
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    c.execute('''DELETE FROM links WHERE expire_at <= ?''', (datetime.datetime.now(),))
    conn.commit()
    conn.close()


@app.route('/')
def home():
    delete_expired_links() 
    active_links = get_active_links()
    return render_template('index.html', active_links=active_links)


@app.route('/add', methods=['POST'])
def add():
    category = request.form['category']
    content = request.form['content']
    expire_at = datetime.datetime.now() + datetime.timedelta(days=2) 
    add_link(category, content, expire_at)
    return redirect(url_for('home'))

if __name__ == '__main__':
    create_db() 
    app.run(debug=True)
