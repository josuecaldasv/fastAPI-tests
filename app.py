from typing import Any, Dict, List
from fastapi import FastAPI, Depends
from custom import CustomPage, CustomParams
import json

app = FastAPI()

# Load data
with open("books.json", "r") as file:
    BOOKS = json.load(file)

# Endpoint
@app.get("/books/all/", response_model=CustomPage[Dict[str, Any]]) 
async def read_all_books(params: CustomParams = Depends()):
    total_items = len(BOOKS)
    start = params.items_per_page * (params.current_page - 1)
    end = start + params.items_per_page
    paginated_items = BOOKS[start:end]

    return CustomPage.create(
        items=paginated_items,
        params=params,
        total=total_items
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:app', reload=True)
