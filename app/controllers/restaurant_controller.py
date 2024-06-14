from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from app.models.restaurant_model import Restaurant
from app.views.restaurant_view import render_restaurants_list, render_restaurant_detail
from app.utils.decorators import jwt_required, role_required

restaurant_bp = Blueprint("restaurant", __name__)

@restaurant_bp.route("/restaurants", methods=["GET"])
@jwt_required
def get_restaurants():
    restaurants = restaurant.get_all()
    return jsonify(render_restaurants_list(restaurants))

@restaurant_bp.route("/restaurants/<int:id>", methods=["GET"])
@jwt_required
def get_restaurant(id):
    restaurant = restaurant.get_by_id(id)
    if restaurant:
        return jsonify(render_restaurant_detail(restaurant))
    return jsonify({"error": "restaurant no encontrado"}), 404


@restaurant_bp.route("/restaurants", methods=["POST"])
@jwt_required
@role_required(role=["admin"])
def post_restaurant():
    data = request.json
    name = data.get("name")
    address = data.get("address")
    city = data.get("city")
    phone = data.get("phone")
    description = data.get("description")
    rating = data.get("rating")

    if not name or not address or not city or not phone or not description or not rating:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    restaurant = restaurant(name=name, address=address, city=city, phone=phone, description=description, rating=rating)
    restaurant.save()
    return jsonify(render_restaurant_detail(restaurant)), 201

@restaurant_bp.route("/restaurants/<int:id>", methods=["PUT"])
@jwt_required
@role_required(role=["admin"])
def update_restaurant(id):
    restaurants = restaurant.get_by_id(id)

    if not restaurants:
        return jsonify({"error": "restaurant no encontrado"}), 404

    data = request.json
    
    if "name" in data:
        restaurants.name = data['name']
    if "address" in data:
        restaurants.address = data['address']
    if "city" in data:
        restaurants.city = data['city']
    if "phone" in data:
        restaurants.phone = data['phone']
    if "description" in data:
        restaurants.description = data['description']
    if "rating" in data:
        restaurants.rating = data['rating']

    restaurants.save()
    return jsonify(render_restaurant_detail(restaurants))

@restaurant_bp.route("/restaurants/<int:id>", methods=["DELETE"])
@jwt_required
@role_required(role=["admin"])
def delete_restaurant(id):
    restaurants = restaurant.get_by_id(id)
    if not restaurants:
        return jsonify({"error": "restaurant no encontrado"}), 404

    restaurants.delete()
    return "", 204