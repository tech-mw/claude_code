from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from game import HighLowGame

app = FastAPI(title="High-Low Card Game API")

# CORS設定（ローカル開発用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
)

game = HighLowGame()


class GuessRequest(BaseModel):
    is_higher: bool


@app.get("/")
def read_root():
    return {"message": "High-Low Card Game API"}


@app.post("/api/new-game")
def new_game():
    """新しいゲームを開始"""
    return game.new_game()


@app.get("/api/state")
def get_state():
    """現在のゲーム状態を取得"""
    return game.get_state()


@app.post("/api/guess")
def make_guess(request: GuessRequest):
    """予想を行う"""
    return game.guess(request.is_higher)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
