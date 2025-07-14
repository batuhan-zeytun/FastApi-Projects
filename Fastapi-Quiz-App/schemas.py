from pydantic import BaseModel


class VoteRequest (BaseModel):
    match_id: int
    selected_item_id: int

