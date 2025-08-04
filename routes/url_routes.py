from flask import Blueprint, request, jsonify, redirect
from models.db import db
from models.url_map import URLMap
from services.shortener import generate_short_code
from utils.validators import is_valid_url
from datetime import datetime
from flasgger import swag_from
from config import Config

url_bp = Blueprint("url_bp", __name__)


@url_bp.route("/shorten", methods=["POST"])
@swag_from("../swagger.yml")
def shorten_url():
    """
    API to create a new short url for the given long url
    - httpMethod: POST
    - path: /shorten
    - request.url: https://www.example.com/United_Kingdom/London/Population
    
    Returns:
        - 201, {"short_url": "http://127.0.0.1:5000/r/ZRLmqg"}
        - 400, {"error": "Invalid URL format"}
    """
    data = request.get_json()
    original_url = data.get("url")

    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL format"}), 400

    short_code = generate_short_code()
    url_map = URLMap(short_code=short_code, original_url=original_url)

    db.session.add(url_map)
    db.session.commit()

    return (
        jsonify(
            {
                "short_url": f"{Config.BASE_URL}/r/{short_code}",
            }
        ),
        201,
    )


@url_bp.route("/expand/<short_code>", methods=["GET"])
@swag_from("../swagger.yml")
def expand(short_code):
    """
    API to return the details of a particular short code
    - httpMethod: GET
    - path: /expand/<short_code>
    Args:
        short_code (string): Unique short code for the URL

    Returns:
        - 200, {"original_url": "https://www.example.com/United_Kingdom/London/Population", "created_at":"2024-03-01T12:02:00"}
        - 400, {"error": "Short URL not found"}
    """
    record = URLMap.query.get(short_code)
    if not record:
        return jsonify({"error": "Short URL not found"}), 404
    return (
        jsonify(
            {
                "original_url": record.original_url,
                "created_at": record.created_at.isoformat(),
            }
        ),
        200,
    )


@url_bp.route("/urls", methods=["GET"])
@swag_from("../swagger.yml")
def all_urls():
    """
    API to return all the short urls created.
    - httpMethod: GET
    - path: /urls

    Returns:
        - 200, [{"created_at": "2024-03-01T12:02:00","original_url": "https://www.google.com","short_code": "Zh8Qkr","short_url": "http://127.0.0.1:5000/r/Zh8Qkr"}]
        - 400, {"error": "No details found"}
    """
    response = URLMap.query.all()
    result = []
    if not response:
        return jsonify({"error": "No details found"}), 404
    for record in response:
        result.append(
            {
                "short_code": record.short_code,
                "short_url": f"{Config.BASE_URL}/r/{record.short_code}",
                "original_url": record.original_url,
                "created_at": record.created_at.isoformat(),
            }
        )
    return (
        jsonify(result),
        200,
    )


@url_bp.route("/update/<short_code>", methods=["PUT"])
@swag_from("../swagger.yml")
def update(short_code):
    """
    API to update existing short url with the given new long url
    - httpMethod: PUT
    - path: /update/<short_code>
    - request.url: https://www.example.com/United_Kingdom/London/Population/v2
    
    Args:
        short_code (string): Unique short code for the URL

    Returns:
        - 200, {"message": "Updated successfully"}
        - 400, {"error": "Invalid URL format"}
        - 404, {"error": "Short URL not found"}
    """
    record = URLMap.query.get(short_code)
    if not record:
        return jsonify({"error": "Short URL not found"}), 404

    data = request.get_json()
    new_url = data.get("url")
    if not is_valid_url(new_url):
        return jsonify({"error": "Invalid URL format"}), 400

    record.original_url = new_url
    db.session.commit()
    return jsonify({"message": "Updated successfully"}), 200


@url_bp.route("/delete/<short_code>", methods=["DELETE"])
@swag_from("../swagger.yml")
def delete(short_code):
    """
    API to delete short url
    - httpMethod: DELETE
    - path: /delete/<short_code>
    
    Args:
        short_code (string): Unique short code for the URL

    Returns:
        - 204, {"message": "Deleted successfully"}
        - 404, {"error": "Short URL not found"}
    """
    record = URLMap.query.get(short_code)
    if not record:
        return jsonify({"error": "Short URL not found"}), 404

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"}), 204


@url_bp.route("/r/<short_code>", methods=["GET"])
@swag_from("../swagger.yml")
def redirect_short_url(short_code):
    """
    API to redirect from the short url
    - httpMethod: GET
    - path: /r/<short_code>
    
    Args:
        short_code (string): Unique short code for the URL

    Returns:
        - 302, redirects to the original url
        - 404, {"error": "Short URL not found"}
    """
    record = URLMap.query.get(short_code)
    if not record:
        return jsonify({"error": "Short URL not found"}), 404
    return redirect(record.original_url)
