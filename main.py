from typing import Text

from flask import Flask, jsonify, request
from flask_cors import CORS

from api import Main

app = Flask(__name__)
main = Main()

# cors
CORS(app)


@app.get("/")
def read_root():
    """
    Get home page
    params: page (optional) - int
    return: JSON

    """

    page = request.args.get("page")
    try:
        if page and not page.isdigit():
            return jsonify(message="error"), 400
        return main.get_home(int(page) if page else 1), 200
    except Exception as err:
        return jsonify(message=err), 500


@app.get("/search/<query>")
def search(query):
    """
    Search donghua by query
    params: query - string (required)
    return: JSON
    """
    if not query:
        return jsonify(message="missing query parameter"), 400
    return main.search(query), 200


# slug from url
@app.get("/info/<slug>")
def get_info(slug: Text):
    """
    Show detail of donghua
    params: slug name of donghua - string (required)
    return: JSON

    """
    try:
        data = main.get_info(slug)
        return data, 200
    except Exception as err:
        return jsonify(message=err), 500


@app.get("/genres")
def list_genres():
    """
    Show list of genres
    return: JSON

    """
    try:
        data = main.genres()
        return data, 200
    except Exception as err:
        return jsonify(message=err), 500


@app.get("/genre/<slug>")
def get_genres(slug):
    """
    Show list of donghua by genre
    params: slug genre - string (required)
    query: page (optional) - int
    return: JSON

    """
    try:
        page = request.args.get("page")
        if page and not page.isdigit():
            return jsonify(message="error"), 400

        data = main.genres(slug, int(page) if page else 1)
        return jsonify(data), 200
    except Exception as err:
        print(err)
        return jsonify(message=err), 500


@app.get("/episode/<slug>")
def get_episode(slug: Text):
    """
    Get detail of episode
    params: slug episode - string (required)
    return: JSON

    """
    try:
        data = main.get_episode(slug)
        if data:
            return jsonify(data), 200
        return jsonify(message="not found"), 404
    except Exception as err:
        return jsonify(message=err), 500


# get episode from url
@app.get("/video-source/<slug>")
def get_video(slug: Text):
    """
    Show list of video source
    params: slug - string (required)
    return: JSON

    """
    try:
        print(slug)
        data = main.get_video_source(slug)
        if data:
            return jsonify(data), 200
        return jsonify(message="not found"), 404
    except Exception as err:
        print(err)
        return jsonify(message=err), 500


@app.get("/anime")
def anime():
    """
    Show list of anime
    return: JSON

    """
    try:
        req = request.args
        todict = dict(req)
        data = main.anime(params=todict)
        return jsonify(data), 200
    except Exception as err:
        print(err)
        return jsonify(message=err), 500


if __name__ == "__main__":
    app.run(debug=True)
