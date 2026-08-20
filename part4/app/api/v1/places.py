from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace("places", description="Place operations")

amenity_model = api.model(
    "PlaceAmenity",
    {
        "id": fields.String(description="Amenity ID"),
        "name": fields.String(description="Name of the amenity"),
    },
)

user_model = api.model(
    "PlaceUser",
    {
        "id": fields.String(description="User ID"),
        "first_name": fields.String(description="First name of the owner"),
        "last_name": fields.String(description="Last name of the owner"),
        "email": fields.String(description="Email of the owner"),
    },
)

review_model = api.model(
    "PlaceReview",
    {
        "id": fields.String(description="Review ID"),
        "text": fields.String(description="Text of the review"),
        "rating": fields.Integer(description="Rating of the place (1-5)"),
        "user_id": fields.String(description="ID of the user"),
    },
)

place_model = api.model(
    "Place",
    {
        "title": fields.String(required=True, description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(required=True, description="Price per night"),
        "latitude": fields.Float(required=True, description="Latitude of the place"),
        "longitude": fields.Float(required=True, description="Longitude of the place"),
        "owner_id": fields.String(required=True, description="ID of the owner"),
        "amenities": fields.List(
            fields.String, required=True, description="List of amenities ID's"
        ),
        "reviews": fields.List(
            fields.Nested(review_model), description="List of reviews"
        ),
    },
)

place_update_model = api.model(
    "PlaceUpdate",
    {
        "title": fields.String(required=False, description="Title of the place"),
        "price": fields.Float(required=False, description="Price per night"),
        "latitude": fields.Float(required=False, description="Latitude of the place"),
        "longitude": fields.Float(required=False, description="Longitude of the place"),
        "amenities": fields.List(fields.String, required=False),
    },
)


@api.route("/")
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @jwt_required()
    def post(self):
        """Register a new place"""
        place = api.payload
        try:
            if get_jwt_identity() != place["owner_id"]:
                return {"error": "Unauthorized action."}, 403

            new_place = facade.create_place(place)
            return new_place.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, "List of places retrieved successfully")
    def get(self):
        return [place.to_dict() for place in facade.get_all_places()], 200


@api.route("/<place_id>")
class PlaceResource(Resource):
    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        place_dict = place.to_dict()

        if place.owner:
            owner = place.owner
            place_dict["owner"] = {
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email,
                "id": owner.id,
            }

        place_dict["amenities"] = [amenity.to_dict() for amenity in place.amenities]
        return place_dict, 200

    @api.expect(place_model)
    @api.response(200, "Place updated successfully")
    @api.response(404, "Place not found")
    @api.response(400, "Invalid input data")
    @api.response(403, "Unauthorized action.")
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get("is_admin", False)

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if current_user_id != place.owner.id and not is_admin:
            return {"error": "Unauthorized action."}, 403

        try:
            updated_place = facade.update_place(place_id, place_data)

            if not updated_place:
                return {"error": "Place not found"}, 404

            return updated_place.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, "Place deleted successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Place not found")
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        place = facade.get_place(place_id)
        is_admin = get_jwt().get("is_admin", False)

        if not place:
            return {"error": "Place not found"}, 404

        if place.owner.id != get_jwt_identity() and not is_admin:
            return {"error": "Unauthorized action."}, 403

        success = facade.delete_place(place_id)
        if not success:
            return {"error": "Place not found"}, 404

        return {"message": "Place deleted successfully"}, 200


@api.route("/<place_id>/reviews")
class PlaceReviewList(Resource):
    @api.response(200, "List of reviews for the place retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                "id": rev.id,
                "text": rev.text,
                "rating": rev.rating.value
                if hasattr(rev.rating, "value")
                else rev.rating,
            }
            for rev in reviews
        ], 200
