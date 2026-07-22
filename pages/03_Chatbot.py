import asyncio
import base64
import json
import os
import sys
from datetime import datetime

import streamlit as st

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.style_utils import load_css
from app.sidebar import render_sidebar
from auth.authenticator import get_authenticator
from database.models import ChatHistory, WorkoutTracker
from services.ai_manager import AIManager
from services.voice_manager import VoiceManager

# Page configuration
st.set_page_config(
    page_title="FormFit AI - Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide default Streamlit navigation
# Remplacez votre ancien bloc st.markdown par celui-ci

st.markdown("""
<style>
    [data-testid="stSidebarNav"] {display: none !important;}
    .st-emotion-cache-79elbk {display: none !important;}
    .st-emotion-cache-10p9htt {display: none !important;}
    
    /* Chat styling */
    .chat-message {
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background: linear-gradient(135deg, #FF4B4B20, #FF758F20);
        border-left: 4px solid #FF4B4B;
    }
    .bot-message {
        background: #F0F2F6; /* Fond gris clair */
        border-left: 4px solid #666;
        color: #333333; /* <-- CORRECTION : Ajout du texte de couleur foncée */
    }
    .chat-container {
        height: 400px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #E6E6E6;
        border-radius: 0.5rem;
        background: white;
    }
</style>
""", unsafe_allow_html=True)

# Load styles and sidebar
load_css()
render_sidebar()

# Get authenticator and require authentication
auth = get_authenticator()
auth.require_authentication()
auth.show_user_menu()

# Get user data
user_data = auth.get_user_data()
if not user_data:
    st.error("Erreur: Impossible de charger les données utilisateur")
    st.stop()

# Initialize chat history and workout tracker
chat_history = ChatHistory(auth.db_manager)
workout_tracker = WorkoutTracker(auth.db_manager)


try:
    if "ai_manager" not in st.session_state:
        st.session_state.ai_manager = AIManager()
    if "voice_manager" not in st.session_state:
        st.session_state.voice_manager = VoiceManager()
except Exception as e:
    st.error(f"Erreur lors de l'initialisation des assistants IA/Voix: {e}")
    st.stop()

# Page title
st.markdown(f"""
<div style='text-align: center; padding: 1rem 0;'>
    <h1 style='color: #FF4B4B; margin-bottom: 0.5rem;'>💬 Assistant Fitness IA</h1>
    <p style='color: #666; font-size: 1.1rem;'>Votre coach personnel intelligent</p>
</div>
""", unsafe_allow_html=True)


def autoplay_audio(mp3_path: str):
    with open(mp3_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    audio_html = f"""
        <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# Initialize session state for chat
if 'chat_messages' not in st.session_state:
    # Load chat history from database
    history = chat_history.get_chat_history(user_data['id'], limit=20)
    st.session_state.chat_messages = []
    for chat in history:
        st.session_state.chat_messages.append({"role": "user", "content": chat['message']})
        st.session_state.chat_messages.append({"role": "assistant", "content": chat['response']})

# Chat interface
st.markdown("## 💬 Conversation")

# Chat container
chat_container = st.container()

with chat_container:
    # Display chat history
    for message in st.session_state.chat_messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 Vous :</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>🤖 Assistant :</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)

# --- NOUVELLE INTERFACE D'ENTRÉE (TEXTE + VOIX) ---

# Fonction pour gérer la logique de réponse (pour ne pas la répéter)
def handle_response(user_text):
    # Add user message to UI
    st.session_state.chat_messages.append({"role": "user", "content": user_text})
    
    # Generate response from the powerful AI
    with st.spinner("🤖 L'assistant réfléchit..."):
        response = st.session_state.ai_manager.get_response(user_text)
    
    # Add assistant response to UI
    st.session_state.chat_messages.append({"role": "assistant", "content": response})
    
    # Save to database
    chat_history.save_chat(user_data['id'], user_text, response)
    
    # Play TTS response
    try:
        mp3_path = asyncio.run(st.session_state.voice_manager.tts_to_file(response))
        if mp3_path and os.path.exists(mp3_path):
            autoplay_audio(mp3_path)
            os.remove(mp3_path)
    except Exception as e:
        st.warning(f"Erreur Text-to-Speech : {e}")

    st.rerun()

# Input area
st.markdown("### Posez votre question :")
user_input = st.text_area(
    "Écrivez votre message...",
    key="user_input",
    height=100,
    placeholder="Ex: Recommande-moi un entraînement pour le haut du corps."
)

# Buttons row
col1, col2, col3 = st.columns([2, 2, 3])

with col1:
    if st.button("📤 Envoyer", use_container_width=True, type="primary"):
        if user_input.strip():
            handle_response(user_input.strip())

with col2:
    if st.button("🎤 Parler", use_container_width=True):
        with st.spinner("🎙️ J'écoute... Parlez maintenant !"):
            try:
                # IMPORTANT: Assurez-vous d'avoir mis le bon index de micro dans voice_manager.py !
                spoken_text = st.session_state.voice_manager.listen()
                if spoken_text:
                    handle_response(spoken_text)
                else:
                    st.toast("Je n'ai rien entendu. Veuillez réessayer.")
            except Exception as e:
                st.error(f"Erreur micro : {e}")

with col3:
    if st.button("🗑️ Effacer conversation", use_container_width=True):
        st.session_state.chat_messages = []
        # Optionnel: vous pourriez aussi vouloir effacer l'historique en base de données ici
        st.rerun()

# --- FIN DE LA NOUVELLE INTERFACE ---

# Suggested questions (VERSION CORRIGÉE)
st.markdown("### 💡 Questions suggérées :")

suggestions = [
    "Quels sont mes progrès cette semaine ?",
    "Recommande-moi des exercices pour débutant",
    "Comment améliorer ma nutrition ?",
    "J'ai besoin de motivation !",
    "Quel est mon score de forme moyen ?"
]

cols = st.columns(len(suggestions))
for i, suggestion in enumerate(suggestions):
    with cols[i]:
        if st.button(suggestion, key=f"suggestion_{i}", use_container_width=True):
            # On appelle simplement notre fonction centrale !
            handle_response(suggestion)

# Quick actions
st.markdown("---")
st.markdown("### ⚡ Actions rapides")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Voir Dashboard", use_container_width=True):
        st.switch_page("pages/01_Dashboard.py")

with col2:
    if st.button("🏃‍♂️ Nouvelle séance", use_container_width=True):
        st.switch_page("pages/01_Commencer.py")

with col3:
    if st.button("👤 Modifier profil", use_container_width=True):
        st.switch_page("pages/02_Profile.py")

# Info box
st.markdown("""
<div style='background: #F0F8FF; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #007ACC; margin: 2rem 0;'>
    <p><strong>💡 Astuce :</strong> Plus vous utilisez l'assistant, plus il comprend vos besoins ! N'hésitez pas à poser des questions spécifiques sur votre entraînement, nutrition ou motivation.</p>
</div>
""", unsafe_allow_html=True)