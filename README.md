# Ads Application

## Description

This is a RESTful API built with FastAPI for a system where users can post Ads and comment on them.

## Features

- User Authentication
- CRUD operations for Ads and Comments
- Pagination for Ads
- Advanced Logging

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
    git clone https://gitlab.com/your-username/my-ads-project.git
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
