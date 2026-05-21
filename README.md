# UniAssist — Medical Study Assistant

## First-time setup (do this once)

### Step 1 — Open Terminal
On Mac: press `Cmd + Space`, type `Terminal`, press Enter.

### Step 2 — Navigate to the app folder
```
cd ~/uniassist
```

### Step 3 — Run setup
```
./setup.sh
```

### Step 4 — Add your API key
1. Open the file `uniassist/.env` in any text editor
2. Replace `sk-ant-your-key-here` with your real key
3. Get a free key at: https://console.anthropic.com
4. Save the file

---

## Starting the app (every time)

```
cd ~/uniassist
./start.sh
```

Then open your browser and go to: **http://localhost:8000**

To stop: press `Ctrl + C` in Terminal.

---

## How to use it

### 1. Upload your materials (start here)
- Go to **Materials** in the sidebar
- Drag & drop your PDFs, PowerPoint slides, or photos of notes
- Type the subject name (e.g. "Cardiology")

### 2. Generate content
Each material gets buttons for:
- **Slides** — structured revision slides with clinical pearls
- **Flashcards** — flip cards for active recall
- **Quiz** — board-exam style MCQs
- **Mind Map** — visual topic overview

### 3. Study with the AI Tutor
- Go to **AI Tutor**
- **Explain mode** — ask anything, get clear answers
- **Socratic mode** — the AI guides you with questions instead (great for exam prep)

### 4. Track your progress
- The **Dashboard** shows your accuracy by topic
- Red = needs work, Green = strong
- The app automatically targets your weakest areas in quizzes

### 5. Set your exam dates
- Go to **Study Plan**
- Add your exam date and subject
- Click **Generate Study Plan** for a day-by-day schedule targeting your gaps
