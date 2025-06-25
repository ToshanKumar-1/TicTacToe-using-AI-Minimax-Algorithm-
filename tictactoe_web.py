import streamlit as st
import random

st.set_page_config(page_title="Tic Tac Toe", layout="centered")

# --- Game State ---
if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turn = "X"
    st.session_state.result = ""
    st.session_state.difficulty = "Hard"
    st.session_state.player_score = 0
    st.session_state.ai_score = 0

# --- Utils ---
def is_winner(player):
    b = st.session_state.board
    return any(
        all(cell == player for cell in row) or
        all(row[i] == player for row in b) or
        all(b[i][i] == player for i in range(3)) or
        all(b[i][2 - i] == player for i in range(3))
        for i, row in enumerate(b)
    )

def is_full():
    return all(cell != "" for row in st.session_state.board for cell in row)

def minimax(is_max):
    if is_winner("O"): return 1
    if is_winner("X"): return -1
    if is_full(): return 0

    best = -float("inf") if is_max else float("inf")
    for i in range(3):
        for j in range(3):
            if st.session_state.board[i][j] == "":
                st.session_state.board[i][j] = "O" if is_max else "X"
                score = minimax(not is_max)
                st.session_state.board[i][j] = ""
                best = max(best, score) if is_max else min(best, score)
    return best

def best_move():
    level = st.session_state.difficulty
    empty = [(i, j) for i in range(3) for j in range(3) if st.session_state.board[i][j] == ""]
    if level == "Easy":
        return random.choice(empty)
    if level == "Medium" and random.random() < 0.5:
        return random.choice(empty)

    move = (-1, -1)
    best_score = -float("inf")
    for i, j in empty:
        st.session_state.board[i][j] = "O"
        score = minimax(False)
        st.session_state.board[i][j] = ""
        if score > best_score:
            best_score = score
            move = (i, j)
    return move

def reset_board():
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turn = "X"
    st.session_state.result = ""

# --- Layout ---
st.title("🧠 Tic Tac Toe vs AI")
col1, col2, col3 = st.columns(3)
col1.metric("You", st.session_state.player_score)
col2.metric("AI", st.session_state.ai_score)
col3.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="difficulty")

# --- Grid ---
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        cell = st.session_state.board[i][j]
        if st.session_state.result or cell != "":
            cols[j].button(cell or " ", disabled=True, key=f"{i}-{j}")
        else:
            if cols[j].button(" ", key=f"{i}-{j}"):
                st.session_state.board[i][j] = "X"
                if is_winner("X"):
                    st.session_state.player_score += 1
                    st.session_state.result = "🎉 You win!"
                elif is_full():
                    st.session_state.result = "🤝 It's a draw!"
                else:
                    ai_i, ai_j = best_move()
                    st.session_state.board[ai_i][ai_j] = "O"
                    if is_winner("O"):
                        st.session_state.ai_score += 1
                        st.session_state.result = "💻 AI wins!"
                    elif is_full():
                        st.session_state.result = "🤝 It's a draw!"

# --- Status ---
if st.session_state.result:
    st.success(st.session_state.result)
    st.button("Play Again", on_click=reset_board)


# use this command to run
# python -m streamlit run "c:\Users\user\OneDrive\Desktop\Projects\TicTacToe using Python\tictactoe_web.py"
