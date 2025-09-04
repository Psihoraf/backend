

from fastapi import FastAPI, Query, Body
import uvicorn
app = FastAPI()


hotels =[
    {"id": 1, "title": "Sochi", "name":"sochi"},
    {"id": 2, "title": "Dubai", "name":"dubai"}
]

@app.get("/hotels")

def func(
        id: int |None=Query(None, description="Айдишник"),
        title: str |None = Query(None, description="Название города")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    return hotels_

@app.delete("/hotels/{hotel_id}")
def delete_hotel(
        hotel_id:int
):
    global hotels
    hotels= [hotel for hotel in hotels if hotel["id"]!=hotel_id]
    return {"status":"OK"}

@app.post("/hotels")
def create_hotel(
        title:str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id":hotels[-1]["id"]+1,
        "title": title
    })
    return {"Status":"OK"}

@app.patch("/hotels/{hotel_id}")
def patch_hotel(
        hotel_id:int,
        title:str|None = Body(),
        name:str|None = Body()

):

    for hotel in hotels:
        if hotel_id and hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return hotel


@app.put("/hotels/{hotel_id}")
def put_hotel(
        hotel_id:int,
        title:str= Body(),
        name:str = Body()

):

    for hotel in hotels:
        if hotel_id and hotel["id"] == hotel_id:
            if title and name is not None:
                hotel["title"] = title
                hotel["name"] = name
                return hotel

if __name__ == "__main__":
    uvicorn.run("main:app", reload=False)