# kinoflix - v1.0.2
# author: nildontsleep
# description:
# this script sets up a flask-based video streaming web application named "kinoflix" usable in a local network

from flask import (
    Flask,
    request,
    send_file,
    redirect,
    url_for,
    session,
    send_from_directory,
    flash,
    Response,
    render_template,
)
from pystyle import Colorate, Colors, System, Center, Write, Anime
from webbrowser import open_new as open_browser
from socket import gethostname, gethostbyname
import os
import yaml
from werkzeug.utils import secure_filename
import secrets
from os import listdir, chdir
from os.path import isfile as file_exists

kinoflix_banner = """

 _    _             
| | _(_)_ __   ___  
| |/ / | '_ \ / _ \ 
|   <| | | | | (_) |
|_|\_\_|_| |_|\___/ 

 / _| (_)_  __      
| |_| | \ \/ /      
|  _| | |>  <       
|_| |_|_/_/\_\ 

"""
banner_image = """

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠸⠿⠿⠿⠿⠇⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⠿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⠉⠉⠉⠉⠉⠙⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⡿⠟⣹⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⡟⢿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⠟⠉⠀⢰⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⡀⠈⠻⢿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀
⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⣾⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⢠⣶⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⡇⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀
⠀⢠⣾⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣦⠀⠀
⣰⣿⣿⣿⣿⣿⣿⡁⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⣹⣿⣿⣿⣿⣿⣷⡄
⠈⠻⣿⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠉⠛⠿⠟⠛⠁⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⡏⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⡿⠟⠁
⠀⠀⠘⠻⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⢸⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⠁⠀⣀⣴⣾⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀
⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⢻⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣣⣴⣾⣿⣿⣿⣿⣿⣿⣿⠟⠉⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⢀⣀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠙⠛⠛⠛⠛⠛⠛⠛⠛⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⣶⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⢰⣶⣶⣶⣶⡶⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

"""

# initialize with random secrets, consider changing secrets if you plan on deploying it to a server
app = Flask(
    "kinoflix", static_url_path="/static", static_folder="img", template_folder="web"
)
app.secret_key = secrets.token_urlsafe(16)


# read file contents and return it
def read_file_contents(filename: str):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


# auth function using users.html and pyyaml
def auth(username, pwd):
    with open("users.yml", "r") as file:
        users = yaml.safe_load(file)
    for user in users["users"]:
        if user["username"] == username and user["password"] == pwd:
            print("Authenticated:", username)
            return True
    print("Failed to Authenticate:", username)
    return False


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        mid = "media_infos"
        mdir = "media"
        os.makedirs(mid, exist_ok=True)
        os.makedirs(mdir, exist_ok=True)
        max_cover_image_size = 25 * 1024 * 1024  # 25 MB
        max_title_length = 32
        max_genre_length = 32
        max_description_length = 256
        allowed_cover_extensions = {"png"}
        allowed_movie_extensions = {"mp4"}

        def allowed_file(filename, file_type):

            if file_type == "cover":
                return (
                    "." in filename
                    and filename.rsplit(".", 1)[1].lower() in allowed_cover_extensions
                )
            elif file_type == "movie":
                return (
                    "." in filename
                    and filename.rsplit(".", 1)[1].lower() in allowed_movie_extensions
                )
            return False

        title = request.form["title"]
        genre = request.form["genre"]
        year = request.form["year"]
        description = request.form["description"]

        if len(title) > max_title_length:
            flash("Title cannot be longer than 32 characters.")
            return redirect(request.url)
        if len(genre) > max_genre_length:
            flash("Genre cannot be longer than 32 characters.")
            return redirect(request.url)
        if len(description) > max_description_length:
            flash("Description cannot be longer than 256 characters.")
            return redirect(request.url)

        cover_image = request.files["cover_image"]
        if cover_image and allowed_file(cover_image.filename, "cover"):
            if len(cover_image.read()) > max_cover_image_size:
                flash("Cover image cannot be larger than 25 MB.")
                return redirect(request.url)
            cover_image.seek(0)
            cover_image_filename = secure_filename(
                f"{title.replace(' ', '_').lower()}.png"
            )
            cover_image_path = os.path.join(mid, cover_image_filename)
            cover_image.save(cover_image_path)
        else:
            flash("Invalid cover image. Only PNG files are allowed.")
            return redirect(request.url)
        movie_file = request.files["movie_file"]
        if movie_file and allowed_file(movie_file.filename, "movie"):
            movie_filename = secure_filename(f"{title.replace(' ', '_').lower()}.mp4")
            movie_path = os.path.join(mdir, movie_filename)
            movie_file.save(movie_path)
        else:
            flash("Invalid movie file. Only MP4 files are allowed.")
            return redirect(request.url)
        media_data = {
            "name": title,
            "category": genre if genre else "No Genre",
            "year": year,
            "description": description,
        }
        filename = os.path.join(mid, f"{title.replace(' ', '_').lower()}.yml")
        with open(filename, "w") as file:
            yaml.dump(media_data, file)

        flash("Movie uploaded successfully!")
        return redirect(url_for("upload"))

    return render_template("upload.html")


@app.route("/login", methods=["GET", "POST"])
def login_route():
    next_url = request.args.get("next", "/")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if auth(username, password):
            session["authenticated"] = True
            session.modified = True
            return redirect(next_url)

        return redirect(url_for("login_route"))

    return read_file_contents("web/login.html")


@app.route("/", methods=["GET"])
def index_route():
    if "authenticated" not in session or not session["authenticated"]:
        return redirect(url_for("login_route"))

    media_infos = [f for f in listdir("media_infos") if f.endswith(".yml")]

    movies = []

    for movie_info in media_infos:
        with open(f"media_infos/{movie_info}", "r", encoding="utf-8") as file:
            movie = yaml.safe_load(file)
            movie["filename"] = movie_info.split(".")[0]

            cover_image = f'{movie["name"].replace(" ", "_").lower()}.png'
            if os.path.exists(f"media_infos/{cover_image}"):
                movie["cover_image"] = f"/static/media_infos/{cover_image}"
            else:
                movie["cover_image"] = "img/kinoflix.png"

            movie_file = f'{movie["filename"]}.mp4'
            if not os.path.exists(f"media/{movie_file}"):
                movie_file = f'{movie["filename"]}.mkv'
                if not os.path.exists(f"media/{movie_file}"):
                    movie_file = f'{movie["filename"]}.avi'
                    if not os.path.exists(f"media/{movie_file}"):
                        movie_file = None

            movie["movie_file"] = movie_file

            movies.append(movie)

    dashboard_html = read_file_contents("web/dashboard.html")
    movie_cards = ""

    for movie in movies:
        if movie["movie_file"]:
            movie_cards += """
                <div class="card">
                    <div class="card-header" style="background-image: url('{}');">
                    <h2 class="card-title">{}</h2>
                    </div>
                    <div class="card-body">
                    <p class="sub-text">{} • {}</p>
                    <h4 class="mt-0 mb-1">Description</h4>
                    <p class="description">
                        {}
                    </p>
                    </div>
                    <a class="card-link-footer" href="/player/{}">Watch movie</a>
                </div>
            """.format(
                movie["cover_image"],
                movie["name"],
                movie["category"],
                movie["year"],
                movie["description"],
                movie["filename"],
            )

    dashboard_html = dashboard_html.replace("{{ movie_cards }}", movie_cards)

    return dashboard_html


@app.route("/player/<filename>")
def player(filename):
    return render_template("player.html", filename="/get/" + filename)


@app.route("/static/media_infos/<image>")
def serve_media_infos_image(image):
    return send_from_directory("media_infos", image)


@app.route("/get/<filename>", methods=["GET"])
def file_retrieval_route(filename):
    file_path = f"media/{filename}"

    if file_exists(file_path):
        return send_file(file_path, as_attachment=True)

    for file in listdir("media"):
        if filename == "".join(file.split(".")[:-1]):
            return send_file(f"media/{file}", as_attachment=True)

    for extension in [".mp4", ".mkv", ".avi"]:
        file_path = f"media/{filename}{extension}"
        if file_exists(file_path):
            return send_file(file_path, as_attachment=True)

    return send_file("img/kinoflix.png", as_attachment=True)


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").lower()

    def generate_movie_cards():
        cards = ""
        for filename in os.listdir("media_infos"):
            if filename.endswith(".yml"):
                with open(
                    os.path.join("media_infos", filename), "r", encoding="utf-8"
                ) as file:
                    movie_info = yaml.safe_load(file)
                    movie_name = movie_info["name"].lower()
                    movie_category = movie_info["category"].lower()
                    movie_year = str(movie_info["year"])

                    if (
                        query in movie_name
                        or query in movie_category
                        or query in movie_year
                    ):
                        cover_image = f'{movie_info["name"].replace(" ", "_").lower()}.png'
                        if not os.path.exists(f"media_infos/{cover_image}"):
                            cover_image = "img/kinoflix.png"

                        movie_file = movie_info.get("filename", "").replace(" ", "_")

                        cards += f"""
                        <div class="card">
                            <div class="card-header" style="background-image: url('/static/media_infos/{cover_image}');">
                                <h2 class="card-title">{movie_info["name"]}</h2>
                            </div>
                            <div class="card-body">
                                <p class="sub-text">{movie_info["category"]} • {movie_info["year"]}</p>
                                <h4 class="mt-0 mb-1">Description</h4>
                                <p class="description">{movie_info["description"]}</p>
                            </div>
                            <a class="card-link-footer" href="/player/{movie_info["name"]}">Watch movie</a>
                        </div>
                        """
        return cards

    return render_template("search.html", movie_cards=generate_movie_cards())


@app.route("/images/<image>", methods=["GET"])
def image_retrieval_route(image):
    return send_from_directory("img", image)


def response_with_status(text: str, status_code: int = 200) -> tuple:
    print(f"Response: {text} | Status Code: {status_code}")
    return text, status_code


System.Clear()
System.Size(140, 30)
System.Title("⛩️ kinoflix ⛩️")
login = os.getlogin()


def display_ui():
    System.Clear()
    print("\n" * 2)
    print(Colorate.Diagonal(Colors.purple_to_red, Center.XCenter(kinoflix_banner)))
    print(" ")
    print(
        Colorate.Diagonal(
            Colors.purple_to_red,
            Center.XCenter("v1.0.2 - github.com/nildontsleep/kinoflix"),
        )
    )
    print("\n" * 5)


Anime.Fade(
    Center.Center(banner_image), Colors.purple_to_red, Colorate.Diagonal, enter=True
)


def start_flask_app(host: str, port: int):
    return app.run(host, port)


def main():
    display_ui()
    hostname, local_ip = gethostname(), gethostbyname(gethostname())
    print(" ")

    host = (
        Write.Input(
            "  " + login + " ┃ desired ip adress (enter to automate ) : ",
            Colors.purple_to_red,
            interval=0.002,
        )
        or local_ip
    )
    print(" ")
    port = (
        Write.Input(
            "  " + login + " ┃ desired port (enter to automate) : ",
            Colors.purple_to_red,
            interval=0.002,
        )
        or "8080"
    )

    try:
        port = int(port)
    except ValueError:
        Colorate.Error("  " + login + " ┃ invalid port; port should be an integer.")
        return

    print(" ")
    Write.Input(
        "  " + login + " ┃ press enter to run the server ",
        Colors.purple_to_red,
        interval=0.002,
    )

    url = f"http://{host}:{port}/"

    display_ui()
    print(Colorate.Vertical(Colors.purple_to_red, f"{login} ┃ running on: {url}"))
    print(Colors.green, end="")

    start_flask_app(host=host, port=port)


if __name__ == "__main__":
    while True:
        main()
