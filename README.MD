![kinoflix](https://github.com/user-attachments/assets/ced26b08-d517-4aa6-9a61-ce7622075cca)

![⭐](https://img.shields.io/github/stars/planetwiide/kinoflix?style=social)
![🍴](https://img.shields.io/github/forks/planetwiide/kinoflix?style=social)
![🐞](https://img.shields.io/github/issues/planetwiide/kinoflix)
![⚡](https://img.shields.io/github/commit-activity/m/planetwiide/kinoflix)
![🆙](https://img.shields.io/github/last-commit/planetwiide/kinoflix)
![📚](https://img.shields.io/github/license/planetwiide/kinoflix)

## 🏯 kinoflix | v1.0.1

**kinoflix** is a flask-based media server designed for streaming and managing your movie collection with ease. enjoy a sleek, user-friendly interface and seamless navigation.



## ✅ to-do list 

- [x] theme managment ⚡
- [x] fix not working on phone 🍃
- [x] search bar 🔍
- [x] security fixes 🫀
- [ ] in app media edit 📋 (figured out how to do it, adding it in the week)
- [ ] anime/series support 🏯
- [ ] auto fetch media informations with an api (imdb) 🎀

## 🚀 features 

- **user authentication** 🪪
  secure login and user management.

- **responsive dashboard** 📊  
  access your media library easily with an aesthetic layout.

- **movie streaming** 🎥  
  stream movies in various formats (mkv, mp4, etc.) from anywhere.

- **ascii art interface** 🖤
  enjoy an engaging browsing experience with pystyle.

## ⚙️ installation 

### prerequisites

make sure you have python and flask installed:

```bash
pip install flask
```

### clone the repository

```bash
git clone https://github.com/planetwiide/kinoflix.git
cd kinoflix
```

### run the application

```bash
python main.py
```

## 🎬 adding a movie 

to add a movie to **kinoflix**, follow these steps:

1. **place the movie file** in the `media` directory.
   - supported formats: **mkv**, **avi**, and **mp4**.

2. **rename the movie file** to a simple name, like:
   - "fight club" or "blade runner 2049".

3. **add the cover image**:
   - place the cover image in the `media_infos` directory.
   - rename the cover image to match the movie name (e.g., "fight club.png" or "blade runner 2049.png").

4. **copy the template**:
   - copy the `template.yml` file from the `media_infos` directory.
   - rename it to match your movie title (e.g., "fight club.yml" or "blade runner 2049.yml").

5. **edit the information**:
   - open the renamed `.yml` file in Notepad or any plain text editor.
   - update the details as needed.

## 🖥️ usage 

1. open your web browser and navigate to the printed url.
2. log in with your credentials.
3. enjoy streaming your favorite movies!

## 🤝 contributing 

contributions are welcome! please feel free to submit a pull request or open an issue.

## 📄 license 

this project is licensed under the mit license.
