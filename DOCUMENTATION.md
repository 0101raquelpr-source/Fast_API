# API Documentation

A simple API for managing a movie database, featuring user authentication and role-based access control.

## Authentication

The API uses JSON Web Tokens (JWT) for authentication. After a successful login, a JWT is set as an `access_token` in an HTTP-only cookie. This token must be sent with subsequent requests to access protected endpoints.

### Security & Roles

*   **Password Hashing**: Passwords are securely hashed using `argon2` after a `sha256` pre-hash. They are never stored in plain text.
*   **Standard User**: A registered user can log in and access public endpoints.
*   **Admin User**: A user with the `admin` role has special permissions. For example, only an admin can access a protected dashboard.

### Auth Endpoints

*   #### `POST /auth/register`
    *   **Description**: Creates a new user. The default role is `client`.
    *   **Request Body**: `UserCreate` model with `username` and `password`.
    *   **Response**: `201 Created` with a confirmation message.

*   #### `POST /auth/login`
    *   **Description**: Authenticates a user and returns an `access_token` in a cookie.
    *   **Request Body**: `username` and `password` in a form data.
    *   **Response**: `200 OK` with a confirmation message. The `Set-Cookie` header will contain the `access_token`.

*   #### `GET /auth/profile`
    *   **Description**: Retrieves the profile of the currently logged-in user.
    *   **Authentication**: Requires a valid `access_token` cookie.
    *   **Response**: `200 OK` with the user's profile data (id, username, role).

*   #### `GET /auth/dashboard`
    *   **Description**: An example of a protected endpoint.
    *   **Authentication**: Requires an admin user (`role: "admin"`).
    *   **Response**: `200 OK` with a welcome message for the admin. Returns `403 Forbidden` if the user is not an admin.

---

## Movie Endpoints

All movie-related endpoints are under the `/movies` prefix.

*   #### `GET /movies/`
    *   **Description**: Retrieves a paginated list of all movies.
    *   **Query Parameters**:
        *   `offset` (int, default: 0): Number of records to skip.
        *   `size` (int, default: 10): Number of records to return.
    *   **Response**: `200 OK` with a list of movie objects.

*   #### `POST /movies/`
    *   **Description**: Creates a new movie.
    *   **Authentication**: Can be protected to require a logged-in user.
    *   **Request Body**: A JSON object matching the `MovieCreate` model.
    *   **Response**: `201 Created` with the newly created movie object, including its database-generated `id`.

*   #### `GET /movies/{id}`
    *   **Description**: Retrieves a single movie by its unique ID.
    *   **Path Parameter**: `id` (int) of the movie.
    *   **Response**: `200 OK` with the movie object. Returns `404 Not Found` if the movie does not exist.

*   #### `GET /movies/by_category`
    *   **Description**: Filters and retrieves movies belonging to a specific category.
    *   **Query Parameter**: `category` (str).
    *   **Response**: `200 OK` with a list of matching movies. Returns `404 Not Found` if no movies match the category.

*   #### `PUT /movies/{id}`
    *   **Description**: Updates the details of an existing movie. Only the fields provided in the request body will be updated.
    *   **Authentication**: Can be protected to require an admin user.
    *   **Path Parameter**: `id` (int) of the movie to update.
    *   **Request Body**: A JSON object with the fields to update (e.g., `{"title": "New Title"}`).
    *   **Response**: `200 OK` with the fully updated movie object.

*   #### `DELETE /movies/{id}`
    *   **Description**: Deletes a movie from the database.
    *   **Authentication**: Can be protected to require an admin user.
    *   **Path Parameter**: `id` (int) of the movie to delete.
    *   **Response**: `200 OK` with a confirmation message: `{"message": "Movie deleted successfully"}`.

---

## Other Endpoints

*   #### `GET /`
    *   **Description**: The home page of the application.
    *   **Response**: `200 OK` with an HTML page.

*   #### `GET /movies/get_file`
    *   **Description**: Serves a sample PDF file.
    *   **Response**: `200 OK` with the PDF file content.