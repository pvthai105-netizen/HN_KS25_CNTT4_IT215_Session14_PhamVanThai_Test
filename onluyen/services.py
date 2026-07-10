from sqlalchemy.orm import Session
from models import teams
from schemas import CreateTeam, UpdateTeam, BaseResponse
from fastapi import HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from fastapi.responses import JSONResponse


def create_response(request: Request,
                    status_code: int,
                    message: str | None,
                    data = None,
                    error = None):
    body = BaseResponse(status_code=status_code, 
                        message=message, 
                        data=jsonable_encoder(data), 
                        error=error,
                        timestamp=datetime.now().isoformat(),
                        path=request.url.path)
    return JSONResponse(status_code=status_code,
                        content=body.model_dump())

def get_all_teams_service(db:Session):
    all_team = db.query(teams).all()
    if not all_team:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Không có đội bóng nào được lưu trữ")
    return all_team

def get_team_by_id_service(db:Session, id: int):
    team_in_id = db.query(teams).filter(teams.id == id).first()
    if not team_in_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Không tìm thấy đội bóng")
    return team_in_id

def create_team_service(db:Session, new_team: CreateTeam):
    try:
        team_input = teams(**new_team.model_dump())
        db.add(team_input)
        db.commit()
        db.refresh(team_input)
        return team_input
    except HTTPException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail=str(err))
    except Exception as error_server:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail=str(error_server))
    
def update_team_service(db: Session, update_team: UpdateTeam, id: int):
    try:
        team_update = db.query(teams).filter(teams.id == id).first()
        if not team_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy đội bóng") 
        data_update = update_team.model_dump(exclude_unset=True)
        for key, value in data_update.items():
            setattr(team_update, key, value)
        db.commit()
        db.refresh(team_update)
        return team_update
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail= "Internal Server Error")
    
def delete_team_service(db: Session, id: int):
    try:
        team_delete = db.query(teams).filter(teams.id == id).first()
        if not team_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không tìm thấy đội bóng") 
        db.delete(team_delete)
        db.commit()
        return team_delete
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail= "Internal Server Error")
    
def search_team_service(db: Session, group_name: str):
    team_search = db.query(teams).filter(teams.group_name.contains(group_name)).all()
    if not team_search:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Không tìm thấy đội bóng")
    return team_search

def sort_team_service(db: Session, order: str = "desc"):
    if order.lower().strip() not in ["desc", "asc"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Vui lòng nhập desc hoặc asc")
    query = db.query(teams)
    if order.lower().strip() == "asc":
        query = query.order_by(teams.points.asc())
    else:
        query = query.order_by(teams.points.desc())
    
    data_sort = query.all()
    return data_sort