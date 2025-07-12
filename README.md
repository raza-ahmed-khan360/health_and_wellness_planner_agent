# 🧠 Health & Wellness Planner Agent (CLI Version)

A smart and friendly **Command-Line AI assistant** that helps you define health goals, plan meals, recommend workouts, schedule check-ins, and track progress. Built using the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/).

---

## 🚀 Features

- ✅ **Goal Analyzer** – Parses natural language goals (e.g., "I want to lose 5 kg in 2 months")
- 🥗 **Meal Planner** – Weekly diet plans for various preferences (vegan, keto, diabetic, etc.)
- 🏃 **Workout Recommender** – Custom 7-day plans for beginner, intermediate, or advanced users
- ⏰ **Check-in Scheduler** – Schedules weekly check-ins with reminders
- 📊 **Progress Tracker** – Logs progress updates (e.g., weight loss logs)
- 🩹 **Injury Support Agent** – Suggests safe workouts when injured
- 🧑‍⚕️ **Nutrition Expert Agent** – Provides advice for medical conditions
- 🆘 **Escalation Agent** – Escalates serious issues to a human coach

---

## 📦 Requirements

- Python 3.8+
- OpenAI API Key (GPT-4o recommended)
- `openai-agents` SDK
- `pydantic`, `python-dotenv`, etc.

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/raza-ahmed-khan360/health-and-wellness-planner-agent.git
cd health-and-wellness-planner-agent
```

### 2. Create Virtual Environment
```
python -m venv .venv
```
## Windows
```
.venv\Scripts\activate
```
## macOS/Linux
```
source .venv/bin/activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Add Environmental Variable
Create ```.env``` file:

```
OPENAI_API_KEY=your-api-key-here
```

# ▶️ Run the Agent (CLI)

```
python main.py
```

# 💬 Example Conversation
```
🧠 Welcome to your Health & Wellness Planner!
Type your goals, health info, or meal/workout requests. Type 'exit' to quit.

👤 You: I want to lose 5 kg in 2 months
🤖 AI: Got it! You've set a goal to lose 5 kg in 2 months.

👤 You: I follow a vegetarian diet
🤖 AI: Here's a weekly vegetarian meal plan...

👤 You: I’m a beginner at workouts
🤖 AI: Here's your 7-day beginner workout routine...

👤 You: I have neck pain
🤖 AI: 🩹 I recommend gentle, low-impact workouts like yoga or light walking.

👤 You: Schedule my check-in on Monday at 8am
🤖 AI: ✅ Check-in set for Monday at 8am.
```

# 🧱 Project Structure

```
health_and_wellness_planner_agent/
├── agent/                    # Main agent and sub-agents
│   ├── escalation_agent.py
│   ├── injury_support_agent.py
│   ├── nutrition_expert_agent.py
├── tools/                     # Tool implementations
│   ├── goal_analyzer.py
│   ├── meal_planner.py
│   ├── scheduler.py
│   ├── tracker.py
│   ├── workout_recommender.py
├── context.py                 # Shared context models (UserSessionContext, RunContextWrapper)
├── hooks.py                   # Custom agent/tool hooks
├── utils/                     # Streaming, logging, and helpers
├── main.py                    # CLI entry point
├── .env                       # API key (not committed)
├── requirements.txt
└── README.md
```

# 🔗 Resources

[OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)

