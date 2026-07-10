from fastapi import FastAPI, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from schemas import CreateTeam, UpdateTeam, BaseResponse
from sqlalchemy import text
from services import (create_response, 
                      create_team_service, 
                      delete_team_service, 
                      get_all_teams_service, 
                      get_team_by_id_service,
                      update_team_service,
                      search_team_service,
                      sort_team_service)

Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
def test_connect_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "message": "Connection Success!",
            "data": "Kết nối thành công"
        }
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
    
@app.get("/teams", response_model= BaseResponse, status_code=status.HTTP_200_OK)
def get_all_team(request: Request, db: Session = Depends(get_db)):
    all_team = get_all_teams_service(db)
    return create_response(request, 
                           status.HTTP_200_OK, 
                           "Danh sách đội bóng tham gia WorldCup", 
                           all_team)

@app.get("/teams/search", response_model= BaseResponse, status_code=status.HTTP_200_OK)
def search_team(request: Request, group_name: str | None, db: Session = Depends(get_db)):
    team_search = search_team_service(db, group_name)
    return create_response(request, 
                           status.HTTP_200_OK, 
                           "Đội bóng tìm được", 
                           team_search)

@app.get("/teams/sort", response_model= BaseResponse, status_code=status.HTTP_200_OK)
def sort_teams(request: Request, order: str = "desc", db: Session = Depends(get_db)):
    team_sort = sort_team_service(db, order)
    return create_response(request, 
                           status.HTTP_200_OK, 
                           "Sắp xếp đội bóng thành công", 
                           team_sort)

@app.get("/teams/{team_id}", response_model= BaseResponse, status_code=status.HTTP_200_OK)
def get_team_by_id(team_id: int, request: Request, db: Session = Depends(get_db)):
    team_exist = get_team_by_id_service(db, team_id)
    return create_response(request, 
                           status.HTTP_200_OK, 
                           "Lấy thành công đội bóng", 
                           team_exist)

@app.post("/teams", response_model= BaseResponse, status_code=status.HTTP_201_CREATED)
def create_team(request: Request, new_team: CreateTeam, db:Session= Depends(get_db)):
    team_create = create_team_service(db, new_team)
    return create_response(request, 
                           status.HTTP_201_CREATED, 
                           "Tạo thành công đội bóng mới", 
                           team_create)

@app.put("/teams/{team_id}", response_model= BaseResponse, status_code=status.HTTP_200_OK)
def update_team(request: Request, team_id: int, update_team: UpdateTeam, db:Session = Depends(get_db)):
    team_update = update_team_service(db, update_team, team_id)
    return create_response(request, 
                           status.HTTP_200_OK, 
                           "Cập nhật thành công đội bóng", 
                           team_update)

@app.delete("/teams/{team_id}", response_model= BaseResponse, status_code=status.HTTP_200_OK)
def delete_team(request: Request, team_id: int, db: Session = Depends(get_db)):
    team_delete = delete_team_service(db, team_id)
    return create_response(request, 
                           status.HTTP_200_OK, 
                           "Xóa thành công đội bóng", 
                           team_delete)
