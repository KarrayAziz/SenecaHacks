# 🏋️ FormFit AI

FormFit AI is a smart fitness coaching app that uses computer vision and AI to help users improve their exercise form in real time. Built for beginners and anyone looking to train safely, it provides posture analysis, rep tracking, progress insights, and AI-guided coaching through a modern Streamlit dashboard.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![Mediapipe](https://img.shields.io/badge/Mediapipe-Pose%20Estimation-orange)

##  Why this project exists

Many people feel intimidated in the gym, especially when they are new to fitness. Fear of injury, lack of guidance, and uncertainty about proper form are common barriers to staying consistent.

FormFit AI tackles that problem by bringing a personal coach experience to the user’s laptop or desktop through webcam-based motion analysis.

##  Core features

- Real-time pose estimation with Mediapipe
- Exercise form feedback for common gym movements
- Rep counting and workout tracking
- Personalized dashboard and progress analytics
- User authentication and profile management
- AI-powered fitness assistant for guidance and motivation
- Support for multiple exercises, including:
  - Squats
  - Deadlifts
  - Shoulder press
  - Bicep curls
  - Wall sits

##  How it works

1. The app captures live video from the webcam.
2. Pose landmarks are extracted using Mediapipe.
3. Joint angles and movement patterns are analyzed to evaluate form.
4. The system provides instant feedback and can save workout data for later review.
5. An AI assistant offers conversational coaching and motivation.

##  Tech stack

- Python
- Streamlit for the web app UI
- OpenCV for image processing
- Mediapipe for pose estimation
- NumPy for motion calculations
- Plotly and Pandas for analytics dashboards
- Groq + dotenv for AI responses
- SQLite for local user and workout storage

##  Project structure

```text
.
├── app/                  # Streamlit app entry pages and shared UI components
├── auth/                 # Authentication and user session logic
├── components/           # Reusable UI components
├── database/             # SQLite models and persistence layer
├── exercise_detectors/   # Exercise-specific pose detection logic
├── pages/                # Multi-page Streamlit app pages
├── services/             # AI assistant and voice-related services
├── utils/                # Utility helpers
├── images/               # Static images and assets
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

##  Getting started

### Prerequisites

- Python 3.10+
- A working webcam
- A Groq API key for the AI chatbot features

### Installation

```bash
git clone https://github.com/KarrayAziz/SenecaHacks.git
cd SenecaHacks2
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root with your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
```

### Run the app

```bash
streamlit run app/home.py
```

Then open the local URL shown in the terminal.

##  Usage

- Create an account or sign in
- Open the dashboard to review your progress
- Start a workout session and enable your webcam
- Follow real-time form feedback while exercising
- Use the chatbot for tips, motivation, or exercise guidance

##  Notes

- Some voice features may require additional system audio dependencies depending on your operating system.
- The app is designed as a local-first prototype and can be extended with cloud deployment, more exercises, and deeper analytics.

##  License

This project is licensed under the MIT License. See the LICENSE file for details.

##  Acknowledgements

Built as part of a hackathon project focused on health, fitness, and accessible AI-powered coaching.
