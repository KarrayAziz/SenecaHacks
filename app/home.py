# gym_webapp.py (Page d'Accueil avec Authentification)
import os
import streamlit as st

from app.style_utils import load_css
from app.sidebar import render_sidebar
from auth.authenticator import get_authenticator

st.set_page_config(
    page_title="FormFit AI - Accueil",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Appliquer le style CSS et afficher la barre latérale
load_css()
render_sidebar()

# Get authenticator
auth = get_authenticator()

# Show user menu in sidebar if authenticated
auth.show_user_menu()

# --- CONTENU PRINCIPAL ---
# Titre principal avec style
st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <h1 style='color: #FF4B4B; font-size: 3rem; margin-bottom: 0.5rem;'>
        Analysez. Corrigez. Progressez.
    </h1>
    <h2 style='color: #666; font-weight: 300; margin-bottom: 2rem;'>
        Votre assistant personnel pour une posture parfaite et la prévention des blessures
    </h2>
</div>
""", unsafe_allow_html=True)

# Check if user is authenticated
if auth.is_authenticated():
    user_data = auth.get_user_data()
    
    # Personalized welcome message
    st.markdown(f"""
    <div style='text-align: center; background: linear-gradient(135deg, #FF4B4B20, #FF758F20);
                padding: 2rem; border-radius: 1rem; margin: 2rem 0;'>
        <h3>👋 Bienvenue, {user_data['name']} !</h3>
        <p>Prêt pour votre prochaine séance d'entraînement ? Accédez à votre dashboard personnalisé 
        ou commencez une nouvelle analyse de mouvement.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick access buttons for authenticated users
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Mon Dashboard", use_container_width=True, type="primary"):
            st.switch_page("pages/01_Dashboard.py")
    
    with col2:
        if st.button("🏃‍♂️ Nouvelle séance", use_container_width=True, type="secondary"):
            st.switch_page("pages/01_Commencer.py")
    
    with col3:
        if st.button("💬 Assistant IA", use_container_width=True, type="secondary"):
            st.switch_page("pages/03_Chatbot.py")
    
    # User's recent activity (if any)
    from database.models import WorkoutTracker
    workout_tracker = WorkoutTracker(auth.db_manager)
    recent_workouts = workout_tracker.get_user_workouts(user_data['id'], limit=3)
    
    if recent_workouts:
        st.markdown("## 🏃‍♂️ Vos dernières séances")
        
        for workout in recent_workouts:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.write(f"**{workout['exercise_type']}**")
            with col2:
                st.write(f"📅 {workout['workout_date'][:10]}")
            with col3:
                if workout['reps']:
                    st.write(f"🔄 {workout['reps']} reps")
            with col4:
                if workout['form_score']:
                    st.write(f"⭐ {workout['form_score']}/10")

else:
    # Non-authenticated user experience
    # Section d'introduction
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; background: linear-gradient(135deg, #FF4B4B20, #FF758F20);
                    padding: 2rem; border-radius: 1rem; margin: 2rem 0;'>
            <h3>🎯 Bienvenue sur FormFit AI !</h3>
            <p>Notre mission est d'utiliser la vision par ordinateur pour vous fournir
            des retours en temps réel sur vos exercices.</p>
            <p><strong>Connectez-vous pour accéder à toutes les fonctionnalités personnalisées !</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Login/Register section for non-authenticated users
    st.markdown("## 🔐 Connexion / Inscription")
    
    tab1, tab2 = st.tabs(["🔑 Se connecter", "📝 S'inscrire"])
    
    with tab1:
        auth.login_form()
    
    with tab2:
        auth.register_form()

# Fonctionnalités principales (visible pour tous)
st.markdown("## 🌟 Fonctionnalités principales")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; border-radius: 1rem;
                background: linear-gradient(135deg, #FF4B4B10, #FF758F10);'>
        <h2 style='color: #FF4B4B;'>📊</h2>
        <h4>Analysez</h4>
        <p>Analyse précise de votre posture en temps réel</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; border-radius: 1rem;
                background: linear-gradient(135deg, #FF4B4B10, #FF758F10);'>
        <h2 style='color: #FF4B4B;'>🔧</h2>
        <h4>Corrigez</h4>
        <p>Conseils personnalisés pour améliorer votre technique</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; border-radius: 1rem;
                background: linear-gradient(135deg, #FF4B4B10, #FF758F10);'>
        <h2 style='color: #FF4B4B;'>📈</h2>
        <h4>Progressez</h4>
        <p>Suivi automatique de vos répétitions et progrès</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Available exercises section
st.markdown("## 🏋️‍♂️ Exercices disponibles")

exercises = [
    {
        "name": "Squats",
        "icon": "🦵",
        "description": "Renforcement des jambes et fessiers",
        "page": "pages/squats_detection.py"
    },
    {
        "name": "Bicep Curls", 
        "icon": "💪",
        "description": "Développement des biceps",
        "page": "pages/05_Bicep_Curls.py"
    },
    {
        "name": "Deadlift",
        "icon": "🏋️",
        "description": "Exercice complet du corps",
        "page": "pages/deadlift_detection.py"
    },
    {
        "name": "Shoulder Press",
        "icon": "🙆‍♂️", 
        "description": "Renforcement des épaules",
        "page": "pages/shoulderpress_detection.py"
    },
    {
        "name": "Wall Seat",
        "icon": "🧱",
        "description": "Endurance des jambes",
        "page": "pages/wallseat_detection.py"
    }
]

cols = st.columns(len(exercises))
for i, exercise in enumerate(exercises):
    with cols[i]:
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; border: 1px solid #E6E6E6; border-radius: 1rem;
                    background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{exercise['icon']}</div>
            <h5 style='margin-bottom: 0.5rem; color: #FF4B4B;'>{exercise['name']}</h5>
            <p style='font-size: 0.9rem; color: #666; margin-bottom: 1rem;'>{exercise['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Commencer {exercise['name']}", key=f"exercise_{i}", use_container_width=True):
            if auth.is_authenticated():
                st.switch_page(exercise['page'])
            else:
                st.warning("🔒 Connectez-vous pour accéder aux exercices!")

# Call to action
if not auth.is_authenticated():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; background: #FF4B4B;
                    border-radius: 1rem; color: white; margin: 2rem 0;'>
            <h3>🚀 Prêt à commencer ?</h3>
            <p>Créez votre compte pour accéder à toutes les fonctionnalités personnalisées !</p>
        </div>
        """, unsafe_allow_html=True)

# Section avantages
st.markdown("## ✅ Pourquoi choisir FormFit AI ?")

advantages = [
    {"icon": "🎯", "title": "Précision", "desc": "Analyse précise basée sur l'IA"},
    {"icon": "⚡", "title": "Temps réel", "desc": "Retours instantanés pendant l'exercice"},
    {"icon": "🛡️", "title": "Sécurité", "desc": "Prévention des blessures intégrée"},
    {"icon": "📱", "title": "Simplicité", "desc": "Interface intuitive et facile à utiliser"},
    {"icon": "📊", "title": "Suivi personnalisé", "desc": "Dashboard et statistiques détaillées"},
    {"icon": "🤖", "title": "Assistant IA", "desc": "Chatbot fitness intelligent"}
]

cols = st.columns(3)
for i, adv in enumerate(advantages):
    with cols[i % 3]:
        if i % 3 == 0 and i > 0:
            st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; margin-bottom: 1rem;'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{adv['icon']}</div>
            <h5>{adv['title']}</h5>
            <p style='font-size: 0.9rem; color: #666;'>{adv['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🔥 <strong>FormFit AI</strong> - Votre partenaire pour un entraînement intelligent et sécurisé</p>
    <p>💪 Rejoignez des milliers d'utilisateurs qui améliorent leur forme physique avec l'IA</p>
</div>
""", unsafe_allow_html=True)