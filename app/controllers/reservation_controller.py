from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from app.models.reservation_model import Reservation
from app.views.reservation_view import render_reservations_list, render_reservation_detail
from app.utils.decorators import jwt_required, role_required
from datetime import datetime

reservation_bp = Blueprint("reservation", __name__)

@reservation_bp.route("/reservations", methods=["GET"])
@jwt_required
def get_reservations():
    reservations = Reservation.get_all()
    return jsonify(render_reservations_list(reservations))

@reservation_bp.route("/reservations/<int:id>", methods=["GET"])
@jwt_required
def get_reservation(id):
    reservation = Reservation.get_by_id(id)
    if reservation:
        return jsonify(render_reservation_detail(reservation))
    return jsonify({"error": "Reserva no encontrada"}), 404

@reservation_bp.route("/reservations", methods=["POST"])
@jwt_required
@role_required(role=["admin"])
def post_reservation():
    data = request.json
    user_id = data.get("user_id")
    restaurant_id = data.get("restaurant_id")
    reservation_date = data.get("reservation_date")
    num_guests = data.get("num_guests")
    special_requests = data.get("special_requests")
    status = data.get("status")

    if not user_id or not restaurant_id or not reservation_date or not num_guests or not status:
        return jsonify({"error": "Faltan datos requeridos"}), 400
    
    new_reservation = Reservation(user_id=user_id, restaurant_id=restaurant_id, reservation_date=reservation_date, num_guests=num_guests, special_requests=special_requests, status=status)
    new_reservation.save()
    return jsonify(render_reservation_detail(new_reservation)), 201

@reservation_bp.route("/reservations/<int:id>", methods=["PUT"])
@jwt_required
@role_required(role=["admin", "customer"])
def update_reservation(id):
    reservations = Reservation.get_by_id(id)

    if not reservations:
        return jsonify({"error": "Reserva no encontrada"}), 404

    data = request.json
    
    if "user_id" in data:
        reservations.user_id = data['user_id']
    if "restaurant_id" in data:
        reservations.restaurant_id = data['restaurant_id']
    if "reservation_date" in data:
        reservations.reservation_date = data['reservation_date']
    if "num_guests" in data:
        reservations.num_guests = data['num_guests']
    if "special_requests" in data:
        reservations.special_requests = data['special_requests']
    if "status" in data:
        reservations.status = data['status']

    reservations.save()
    return jsonify(render_reservation_detail(reservations))

@reservation_bp.route("/reservations/<int:id>", methods=["DELETE"])
@jwt_required
@role_required(role=["admin", "customer"])
def delete_reservation(id):
    reservation = Reservation.query.get(id)
    if reservation is None:
        return jsonify({"error": "Reserva no encontrada"}), 404
    reservation.delete()
    return jsonify({"message": "Reserva eliminada correctamente"}), 200