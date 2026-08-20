from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.utils.admin_required import admin_required

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model(
    "Amenity",
    {
        "id": fields.String(
            readOnly=True, description="The unique identifier of the amenity"
        ),
        "name": fields.String(required=True, description="Name of the amenity"),
    },
)


@api.route("/")
class AmenityList(Resource):
    """Handle amenity list and creation"""

    @api.marshal_list_with(amenity_model)
    def get(self):
        return facade.get_all_amenities(), 200

    @api.expect(amenity_model)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    @admin_required()
    def post(self):
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {"id": new_amenity.id, "name": new_amenity.name}, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route("/<string:amenity_id>")
@api.response(404, "Amenity not found")
class AmenityResource(Resource):
    """Handle individual amenity operations"""

    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity, 200

    @api.expect(amenity_model)
    @api.response(200, "Amenity successfully updated")
    @api.response(400, "Invalid input data")
    @admin_required()
    def put(self, amenity_id):
        amenity_data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                api.abort(404, "Amenity not found")
            return {"id": updated_amenity.id, "name": updated_amenity.name}, 200
        except ValueError as e:
            api.abort(400, str(e))
