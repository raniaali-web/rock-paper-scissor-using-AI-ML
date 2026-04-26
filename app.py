import streamlit as st
import random
import numpy as np
from sklearn.naive_bayes import MultinomialNB
import base64

# Encode moves
move_map = {"rock":0, "paper":1, "scissors":2}
reverse_map = {0:"rock", 1:"paper", 2:"scissors"}

player_moves = []
model = MultinomialNB()

# Train model
def train_model(moves):
    if len(moves) < 2:
        return None
    X = np.array(moves[:-1]).reshape(-1,1)
    y = np.array(moves[1:])
    model.fit(X,y)
    return model

# Computer choice
def computer_choice(moves):
    if len(moves) < 5:
        return random.choice([0,1,2])
    trained = train_model(moves)
    if trained:
        predicted = model.predict(np.array([moves[-1]]).reshape(-1,1))[0]
    else:
        predicted = random.choice([0,1,2])
    return (predicted + 1) % 3

# Winner logic
def get_winner(user, computer):
    if user == computer:
        return "It's a tie!"
    elif (user == 0 and computer == 2) or \
         (user == 1 and computer == 0) or \
         (user == 2 and computer == 1):
        return "You win!"
    else:
        return "Computer wins!"

# Background function (base64 embed)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(image_file):
    bin_str = get_base64_of_bin_file(image_file)
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Call background
set_background("images/background.jfif")   # tumhari abstract painting

# Title
st.markdown("<h1 style='text-align:center; color:#FFD700;'>🎮 Rock-Paper-Scissors with ML</h1>", unsafe_allow_html=True)

# Gesture images
col1, col2, col3 = st.columns(3)
with col1:
    st.image("images/rock.png", caption="Rock", width=150)
with col2:
    st.image("images/paper.png", caption="Paper", width=150)
with col3:
    st.image("images/scissors.png", caption="Scissors", width=150)

# Initialize scoreboard (run once at top of app.py)
if "score_user" not in st.session_state:
    st.session_state.score_user = 0
if "score_comp" not in st.session_state:
    st.session_state.score_comp = 0
# User choice
user_choice = st.radio("Choose your move:", ["rock","paper","scissors"])

if st.button("Play"):
    user_move = move_map[user_choice]
    player_moves.append(user_move)

    comp_move = computer_choice(player_moves)
    st.image(f"images/{reverse_map[comp_move]}.png", caption=f"Computer chose {reverse_map[comp_move]}", width=150)

    result = get_winner(user_move, comp_move)

    # 🏆 Update scoreboard
    if "You win!" in result:
        st.session_state.score_user += 1
    elif "Computer wins!" in result:
        st.session_state.score_comp += 1

#show result
    st.success(get_winner(user_move, comp_move))
 
 # Show scoreboard
    st.markdown(f"🏆 **Your Score:** {st.session_state.score_user} | 🤖 **Computer Score:** {st.session_state.score_comp}")