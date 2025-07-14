from fastapi import FastAPI
import random, copy, json
import schemas
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_quiz_items():
    file_path = Path(__file__).parent / "quiz_items.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

quiz_items = load_quiz_items()

votes = []
votes_round2 = []
votes_round3 = []

round1_matchups = []
round2_matchups = []
round3_matchups = []

def create_next_round_matchups(winners):
    if len(winners) == 1:
        return [], winners

    if len(winners) % 2 != 0:
        bye_item = winners.pop()
    else:
        bye_item = None

    matchups = []
    for i in range(0, len(winners), 2):
        matchups.append({
            "match_id": i // 2 + 1,
            "pair": [winners[i], winners[i+1]]
        })

    if bye_item:
        matchups.append({
            "match_id": len(matchups) + 1,
            "pair": [bye_item]
        })

    return matchups, None

@app.get("/")
async def root():
    return {"message": "Quiz app is working!"}

@app.get("/matchups/round1")
def get_first_round():
    global round1_matchups
    items_copy = copy.deepcopy(quiz_items)
    random.shuffle(items_copy)

    matchups = []
    for i in range(0, len(items_copy), 2):
        match = {
            "match_id": i // 2 + 1,
            "pair": [items_copy[i], items_copy[i + 1]]
        }
        matchups.append(match)

    round1_matchups = matchups
    return {"round": 1, "matchups": matchups}

@app.post("/vote")
def vote(request: schemas.VoteRequest):
    new_vote = {"match_id": request.match_id, "selected_item_id": request.selected_item_id}
    votes.append(new_vote)

    return {"message": "Vote recorded", "current_votes": votes}


@app.get("/matchups/round2")
def get_second_round():
    global round2_matchups
    if not votes:
        return {"message": "No votes yet."}

    winners = []
    for matchup in round1_matchups:
        match_id = matchup["match_id"]
        match_votes = [v for v in votes if v["match_id"] == match_id]
        if not match_votes:
            continue
        selected_id = match_votes[-1]["selected_item_id"]
        selected_item = next((item for item in matchup["pair"] if item["id"] == selected_id), None)
        if selected_item:
            winners.append(selected_item)

    matchups, final_winners = create_next_round_matchups(winners)
    round2_matchups = matchups

    if final_winners:
        return {"round": 2, "winner": final_winners[0]}

    return {"round": 2, "matchups": matchups}

@app.post("/vote/round2")
def vote_round2(request: schemas.VoteRequest):
    vote_record = {
        "match_id": request.match_id,
        "selected_item_id": request.selected_item_id
    }
    votes_round2.append(vote_record)
    return {"message": "Vote recorded for Round 2", "current_votes": votes_round2}


@app.get("/matchups/round3")
def get_third_round():
    global round3_matchups
    if not votes_round2:
        return {"message": "No votes yet for round 2."}

    winners = []
    for matchup in round2_matchups:
        match_id = matchup["match_id"]
        match_votes = [v for v in votes_round2 if v["match_id"] == match_id]
        if not match_votes:
            continue
        selected_id = match_votes[-1]["selected_item_id"]
        selected_item = next((item for item in matchup["pair"] if item["id"] == selected_id), None)
        if selected_item:
            winners.append(selected_item)

    matchups, final_winners = create_next_round_matchups(winners)
    round3_matchups = matchups

    if final_winners:
        return {"round": 3, "winner": final_winners[0]}

    return {"round": 3, "matchups": matchups}

@app.post("/vote/round3")
def vote_round3(request: schemas.VoteRequest):
    vote_record = {
        "match_id": request.match_id,
        "selected_item_id": request.selected_item_id
    }
    votes_round3.append(vote_record)
    return {"message": "Vote recorded for Round 3", "current_votes": votes_round3}


@app.get("/winner")
def get_winner():
    if not votes_round3:
        return {"message": "No votes yet for round 3."}

    for matchup in round3_matchups:
        match_id = matchup["match_id"]
        match_votes = [v for v in votes_round3 if v["match_id"] == match_id]
        if not match_votes:
            continue
        selected_id = match_votes[-1]["selected_item_id"]
        selected_item = next((item for item in matchup["pair"] if item["id"] == selected_id), None)
        if selected_item:
            return {"winner": selected_item}

    return {"message": "No winner could be determined."}
