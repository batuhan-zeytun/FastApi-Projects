# 🏆 Tournament Voting App

This is a simple tournament-style voting application built with **FastAPI** (backend) and **vanilla JavaScript/HTML/CSS** (frontend). Users are presented with pairwise matchups and vote for their preferred item. Winners advance to the next round until a final winner is selected.

## 📁 Project Structure

Fastapi-Quiz-App/
│
├── main.py # FastAPI backend
├── schemas.py # Pydantic models for request validation
├── quiz_items.txt # JSON file containing all the quiz items (id, text, image)
│
├── frontend/
│ ├── index.html # Frontend UI
│ ├── main.js # Voting logic and UI updates
│ └── style.css # Styling for UI

## 🚀 Features

- Pairwise matchups in each round (like tournament brackets)
- Auto-advance to the next match after voting
- Smooth image highlight effect for selected item
- Final winner is displayed with image and name
- Dynamic data loading from a JSON file (`quiz_items.txt`)


## 📦 Requirements

- Python 3.8+
- `fastapi`
- `uvicorn`

You can install dependencies with:

pip install -r requirements.txt


## ▶️ Running the Application

1. Start the FastAPI Backend
uvicorn main:app --reload

2. Open the Frontend
Simply open the frontend/index.html file in your browser.

## 📄 quiz_items.txt Format

[
  {
    "id": 1,
    "text": "Inception",
    "image": "https://example.com/inception.jpg"
  },
  {
    "id": 2,
    "text": "Matrix",
    "image": "https://example.com/matrix.jpg"
  }
]
