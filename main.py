from typing import Union, Text

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from api import Main

app = FastAPI()
main = Main()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# slug from url
@app.get("/info/{slug}")
def get_info(slug: Text):
    slug = slug
    data = main.get_info(slug)
    return data


# get episode from url
@app.get("/video/{slug}")
def get_video(slug: Text):
    try:

        data = main.get_video(slug)
        if data:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=data,
            )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Not Found"},
        )
    except Exception as err:
        print(err)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error"},
        )
