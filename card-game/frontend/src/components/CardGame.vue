<template>
  <div class="game-container">
    <h1>🎴 High-Low カードゲーム</h1>

    <div class="score-board">
      <div class="score-item">
        <span class="label">スコア:</span>
        <span class="value">{{ gameState.score }}</span>
      </div>
      <div class="score-item">
        <span class="label">連続正解:</span>
        <span class="value">{{ gameState.streak }}</span>
      </div>
    </div>

    <div class="card-display" v-if="gameState.current_card">
      <div class="card" :class="getCardColor(gameState.current_card.suit)">
        <div class="card-value">{{ gameState.current_card.display }}</div>
        <div class="card-suit">{{ getSuitSymbol(gameState.current_card.suit) }}</div>
      </div>
    </div>

    <div class="result-message" v-if="lastResult">
      <div :class="['message', lastResult.correct ? 'correct' : 'incorrect']">
        {{ lastResult.correct ? '✓ 正解!' : '✗ 不正解!' }}
      </div>
      <div class="cards-comparison">
        <div class="small-card" :class="getCardColor(lastResult.previous_card.suit)">
          {{ lastResult.previous_card.display }}{{ getSuitSymbol(lastResult.previous_card.suit) }}
        </div>
        <span class="arrow">→</span>
        <div class="small-card" :class="getCardColor(lastResult.next_card.suit)">
          {{ lastResult.next_card.display }}{{ getSuitSymbol(lastResult.next_card.suit) }}
        </div>
      </div>
    </div>

    <div class="question" v-if="!loading">
      次のカードは現在のカードより...
    </div>

    <div class="buttons">
      <button
        @click="makeGuess(true)"
        :disabled="loading"
        class="btn btn-higher"
      >
        ⬆️ 高い
      </button>
      <button
        @click="makeGuess(false)"
        :disabled="loading"
        class="btn btn-lower"
      >
        ⬇️ 低い
      </button>
    </div>

    <button @click="newGame" class="btn btn-new-game">
      🔄 新しいゲーム
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Card {
  suit: string
  value: number
  display: string
}

interface GameState {
  current_card: Card | null
  score: number
  streak: number
}

interface GuessResult {
  correct: boolean
  previous_card: Card
  next_card: Card
  score: number
  streak: number
}

const API_URL = 'http://localhost:8000'

const gameState = ref<GameState>({
  current_card: null,
  score: 0,
  streak: 0
})

const lastResult = ref<GuessResult | null>(null)
const loading = ref(false)

const getSuitSymbol = (suit: string): string => {
  const symbols: Record<string, string> = {
    hearts: '♥',
    diamonds: '♦',
    clubs: '♣',
    spades: '♠'
  }
  return symbols[suit] || suit
}

const getCardColor = (suit: string): string => {
  return suit === 'hearts' || suit === 'diamonds' ? 'red' : 'black'
}

const fetchGameState = async () => {
  try {
    const response = await fetch(`${API_URL}/api/state`)
    const data = await response.json()
    gameState.value = data
  } catch (error) {
    console.error('ゲーム状態の取得に失敗:', error)
  }
}

const newGame = async () => {
  try {
    loading.value = true
    lastResult.value = null
    const response = await fetch(`${API_URL}/api/new-game`, {
      method: 'POST'
    })
    const data = await response.json()
    gameState.value = data
  } catch (error) {
    console.error('新しいゲームの開始に失敗:', error)
  } finally {
    loading.value = false
  }
}

const makeGuess = async (isHigher: boolean) => {
  try {
    loading.value = true
    const response = await fetch(`${API_URL}/api/guess`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ is_higher: isHigher })
    })
    const result: GuessResult = await response.json()

    lastResult.value = result
    gameState.value.score = result.score
    gameState.value.streak = result.streak
    gameState.value.current_card = result.next_card

    // 結果表示後、少し待ってからリセット
    setTimeout(() => {
      lastResult.value = null
    }, 2000)
  } catch (error) {
    console.error('予想の送信に失敗:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  newGame()
})
</script>

<style scoped>
.game-container {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 2em;
}

.score-board {
  display: flex;
  justify-content: space-around;
  margin-bottom: 30px;
  padding: 15px;
  background: #f5f5f5;
  border-radius: 10px;
}

.score-item {
  text-align: center;
}

.score-item .label {
  display: block;
  font-size: 0.9em;
  color: #666;
  margin-bottom: 5px;
}

.score-item .value {
  display: block;
  font-size: 1.8em;
  font-weight: bold;
  color: #667eea;
}

.card-display {
  display: flex;
  justify-content: center;
  margin: 30px 0;
}

.card {
  width: 150px;
  height: 210px;
  background: white;
  border: 3px solid #333;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 3em;
  font-weight: bold;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s;
}

.card:hover {
  transform: scale(1.05);
}

.card.red {
  color: #e74c3c;
}

.card.black {
  color: #2c3e50;
}

.card-value {
  font-size: 2.5em;
}

.card-suit {
  font-size: 1.5em;
  margin-top: 10px;
}

.result-message {
  text-align: center;
  margin: 20px 0;
}

.message {
  font-size: 1.5em;
  font-weight: bold;
  margin-bottom: 10px;
}

.message.correct {
  color: #27ae60;
}

.message.incorrect {
  color: #e74c3c;
}

.cards-comparison {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
}

.small-card {
  padding: 10px 15px;
  border: 2px solid #333;
  border-radius: 8px;
  font-size: 1.2em;
  font-weight: bold;
  background: white;
}

.small-card.red {
  color: #e74c3c;
}

.small-card.black {
  color: #2c3e50;
}

.arrow {
  font-size: 1.5em;
  color: #666;
}

.question {
  text-align: center;
  font-size: 1.2em;
  color: #555;
  margin: 20px 0;
}

.buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin: 30px 0;
}

.btn {
  padding: 15px 40px;
  font-size: 1.2em;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
  color: white;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-higher {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.btn-higher:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
}

.btn-lower {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.btn-lower:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(245, 87, 108, 0.4);
}

.btn-new-game {
  display: block;
  margin: 20px auto 0;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.btn-new-game:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(79, 172, 254, 0.4);
}
</style>
