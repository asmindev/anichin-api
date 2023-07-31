# Anichin API

AniChin API adalah sebuah proyek yang dikembangkan untuk memudahkan developer dalam mengakses data-data anime dan manga. Proyek ini menggunakan teknologi RESTful API sehingga memudahkan developer dalam mengakses data-data yang dibutuhkan.

## API Reference

# FastAPI Donghua API

![FastAPI Logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

This is a FastAPI-based API for fetching information about donghua (Chinese animation). It provides various endpoints to retrieve donghua data based on different criteria.

## Endpoints

| Endpoint           | Description                 | Parameters                                                              | Response                                                         |
| :----------------- | :-------------------------- | :---------------------------------------------------------------------- | :--------------------------------------------------------------- |
| `GET /`            | Get the home page           | `page` (optional) - int: The page number for pagination                 | JSON containing donghua data                                     |
| `GET /search`      | Search for donghua by query | `q` - string (required): The search query                               | JSON containing search results                                   |
| `GET /info/{slug}` | Show detail of donghua      | `slug` - string (required): The unique identifier (slug) of the donghua | JSON containing detailed information about the specified donghua |
| `GET /genres`      | Show list of genres         | None                                                                    | JSON containing the list of genres                               |
|                    |                             | `page` (optional) - int: The page number for pagination                 |                                                                  |

| `GET /genre/{slug}` | Show list of donghua by genre | `slug` - string (required): The slug of the genre | JSON containing the list of donghua for the specified genre |
| `GET /episode/{slug}` | Show list of episode | `slug` - string (required): The unique identifier (slug) of the donghua | JSON containing the list of episodes for the specified donghua |
| `GET /video-source/{slug}` | Show list of video source | `slug` - string (required): The unique identifier (slug) of the donghua | JSON containing the list of video sources for the specified donghua |

## Error Handling

The API handles various error scenarios and returns appropriate error responses in JSON format.

| HTTP Status Code | Description                                               |
| :--------------- | :-------------------------------------------------------- |
| 400              | Bad Request - Invalid request or missing query parameters |
| 404              | Not Found - The requested resource is not found           |
| 500              | Internal Server Error - An internal server error occurs   |

## Run Locally

Clone the project

```bash
  git clone https://github.com/asmindev/anichin-api
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  uvicorn main:app --reload
```

## Authors

-   [@iniasmin\_](https://instagram.com/iniasmin_)
-   [@asmindev](https://github.com/asmindev_)
