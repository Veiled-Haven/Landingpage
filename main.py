import os
import random
from flask import Flask, render_template, request

app = Flask(
    __name__, static_url_path="", static_folder="static/", template_folder="templates/"
)




def get_images(offset=0, per_page=9):
    """this is a demo function making use of lorempicsum."""
    # replace with actual logic!
    result= []
    for i in range(per_page):
        random.seed(i+offset+1337)
        result.append(f"https://picsum.photos/seed/{random.randint(1, 1000000000)}/1920/1080")
    return result

@app.route("/galery")
def galery():
     # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 9
    offset = (page - 1) * per_page

    # Fetching images for the current page
    images = get_images(offset, per_page)

    # Assuming you have a total of 100 images, modify this according to your data
    total_images = 100
    total_pages = (total_images + per_page - 1) // per_page

    return render_template(
        'galery.html',
        images=images,
        page=page,
        total_pages=total_pages
    )

@app.route("/")
def home():
    return render_template("index.html",images=get_images(0, 3))

app.run(host="0.0.0.0", port=5000)
