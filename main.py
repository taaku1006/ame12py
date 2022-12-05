from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64
from scraping import Get_amedas_data
from graph import draw_graph
from fastapi.responses import FileResponse

class Data(BaseModel):
    a_name: str
    st_name: str
    start: str
    end: str

app = FastAPI()


origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api5")
def read_item(data: Data):
    amedas = Get_amedas_data(data.a_name, data.st_name)
    amedas.set_date1(data.start, data.end)
    amedas.dl_data('daily')
    draw_graph("data.csv")
    with open('./temp.png', 'rb') as imgFile:
        image = base64.b64encode(imgFile.read()).decode("utf-8")
        return { "path": ('data:image/jpeg;base64,' + image) }

@app.get('/download/{name}', response_class=FileResponse)
def get_file(name: str):
    path2 = f'files/{name}'
    return path2