# Anichin API

AniChin API adalah sebuah proyek yang dikembangkan untuk memudahkan developer dalam mengakses data-data anime dan manga. Proyek ini menggunakan teknologi RESTful API sehingga memudahkan developer dalam mengakses data-data yang dibutuhkan.

## API Reference

#### Get info

```http
  GET /info/{slug}
```

| Parameter | Type     | Description                        |
| :-------- | :------- | :--------------------------------- |
| `slug`    | `string` | **Required**. Slug untuk informasi |

#### Get video

```http
  GET /info/{slug}
```

| Parameter | Type     | Description                        |
| :-------- | :------- | :--------------------------------- |
| `slug`    | `string` | **Required**. Slug untuk video url |

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
