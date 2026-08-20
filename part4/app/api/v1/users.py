from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from app.utils.admin_required import admin_required

api = Namespace("users", description="User operations")

user_model = api.model(
    "User",
    {
        "first_name": fields.String(
            required=True, description="First name of the user"
        ),
        "last_name": fields.String(required=True, description="Last name of the user"),
        "email": fields.String(required=True, description="Email of the user"),
        "password": fields.String(required=True, description="Password of the user"),
        "is_admin": fields.Boolean(required=False, description="Admin or not"),
    },
)

user_update_model = api.model(
    "UserUpdate",
    {
        "first_name": fields.String(
            required=False, description="First name of the user"
        ),
        "last_name": fields.String(required=False, description="Last name of the user"),
        "email": fields.String(required=False, description="Email of the user"),
        "password": fields.String(required=False, description="Password of the user"),
    },
)


@api.route("/")
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered or invalid input data")
    @admin_required()
    def post(self):
        """Register a new user"""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data["email"])
        if existing_user:
            return {"error": "Email already registered"}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
            }, 201
        except ValueError as error:
            return {"error": str(error)}, 400

    @api.response(200, "List of users retrieved successfully")
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()

        return [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
            for user in users
        ], 200


@api.route("/<user_id>")
class UserResource(Resource):
    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }, 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, "User updated successfully")
    @api.response(404, "User not found")
    @api.response(400, "Invalid input data or attempted to modify protected fields")
    @api.response(403, "Unauthorized action.")
    @jwt_required()
    def put(self, user_id):
        """Update a user's information"""
        user_data = api.payload
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get("is_admin", False)

        if user_id != current_user_id and not is_admin:
            return {"error": "Unauthorized action."}, 403
        if ("email" in user_data or "password" in user_data) and not is_admin:
            return {"error": "You cannot modify email or password."}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {"error": "User not found"}, 404

            return {
                "id": updated_user.id,
                "first_name": updated_user.first_name,
                "last_name": updated_user.last_name,
                "email": updated_user.email,
            }, 200
        except ValueError as error:
            return {"error": str(error)}, 400
