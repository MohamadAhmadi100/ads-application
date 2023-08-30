# Ads Application

## Description

This is a RESTful API built with FastAPI for a system where users can post Ads and comment on them.

## Features

1. User Authentication using JWT
2.CRUD operations for Ads and Comments
3.RESTful API using FastAPI
4.PostgreSQL as the database
5.Use of ORM
6.Tests for APIs
7.OpenAPI Specification
8.PyJWT for generating and decoding access and refresh tokens
9.Logger for the application
10.Exception handler for the application
11.Pagination for Ads


## Technologies Used

- FastAPI
- PostgreSQL
- Pydantic
- SQLAlchemy

## Installation

### Requirements

- Python 3.8+
- PostgreSQL
- Redis

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/MohamadAhmadi100/ads-application.git
    ```

2. Navigate to the project directory:

    ```bash
    cd my-ads-project
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables:

    ```bash
    cp .env.example .env
    ```

    Edit the `.env` file to include your database and Redis credentials.

5. Run the application:

    ```bash
    uvicorn app.main:app --reload
    ```

### Docker Setup

1. Build the Docker image: `docker build -t ads-application .`
2. Run the Docker container: `docker run -p 8000:8000 ads-application`

## Usage

The API documentation is available at `http://127.0.0.1:8000/docs`.

### Endpoints

- User Registration: `POST /user/register/`
- User Login: `POST /user/login/`
- Create Ad: `POST /ad/create/`
- Create Comment: `POST /comment/createt/`
- List Ads with Pagination: `GET /ad/list/`
- User List Ads with Pagination: `GET /ad/user_ads/`
- Edit Ad: `PUT /ad/edit/{ad_id}/`
- Delete Ad: `DELETE /ad/delete/{ad_id}/`

## Testing

Run the tests using `pytest`:

```bash
pytest
