from pydantic import BaseModel, Field


class MoveRequest(BaseModel):
    player: str = Field(pattern="^P[12]$")
    direction: str = Field(pattern="^(UP|DOWN|LEFT|RIGHT)$")


class WallRequest(BaseModel):
    player: str = Field(pattern="^P[12]$")
    x: int = Field(ge=0, le=7)
    y: int = Field(ge=0, le=7)
    orientation: str = Field(pattern="^(H|V)$")

