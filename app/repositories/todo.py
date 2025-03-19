from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoRepository:
    def __init__(self, session):
        self.session = session

    async def create_todo(self, todo_data: TodoCreate) -> Todo:
        new_todo = Todo(**todo_data.model_dump())
        self.session.add(new_todo)
        await self.session.commit()
        await self.session.refresh(new_todo)
        return new_todo

    async def get_todos(self) -> list[Todo]:
        result = await self.session.execute(select(Todo))
        return result.scalars().all()

    async def get_todo(self, todo_id: int) -> Todo:
        result = await self.session.execute(select(Todo).where(Todo.id == todo_id))
        todo = result.scalar_one_or_none()
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        return todo

    async def update_todo(self, todo_id: int, todo_data: TodoUpdate) -> Todo:
        result = await self.session.execute(
            update(Todo)
            .where(Todo.id == todo_id)
            .values(**todo_data.model_dump(exclude_unset=True))
            .returning(Todo)
        )
        todo = result.scalar_one_or_none()
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        await self.session.commit()
        return todo

    async def delete_todo(self, todo_id: int) -> None:
        result = await self.session.execute(
            delete(Todo).where(Todo.id == todo_id).returning(Todo.id)
        )
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        await self.session.commit()
