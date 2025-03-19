from fastapi import APIRouter, Depends, status
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.repositories.todo import TodoRepository
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TodoResponse)
async def create_todo(todo_data: TodoCreate, db: AsyncSession = Depends(get_db)):
    repo = TodoRepository(db)
    return await repo.create_todo(todo_data)


@router.get("/", response_model=list[TodoResponse])
async def get_todos(db: AsyncSession = Depends(get_db)):
    repo = TodoRepository(db)
    return await repo.get_todos()


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    repo = TodoRepository(db)
    return await repo.get_todo(todo_id)


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int, todo_data: TodoUpdate, db: AsyncSession = Depends(get_db)
):
    repo = TodoRepository(db)
    return await repo.update_todo(todo_id, todo_data)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    repo = TodoRepository(db)
    await repo.delete_todo(todo_id)
