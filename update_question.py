import json
import random

QUESTION_START = "<!-- QUESTION_START -->"
QUESTION_END = "<!-- QUESTION_END -->"

README = "README.md"
QUESTIONS = "questions.json"
CURRENT = "current.txt"

with open(QUESTIONS, "r", encoding="utf-8") as f:
    questions = json.load(f)

with open(CURRENT, "r") as f:
    index = int(f.read().strip())

if index >= len(questions):
    index = 0

question = questions[index]

options = question["options"][:]
random.shuffle(options)

next_index = (index + 1) % len(questions)

with open(CURRENT, "w") as f:
    f.write(str(next_index))

difficulty_icons = {
    "Easy": "🟢 Easy",
    "Medium": "🟡 Medium",
    "Hard": "🔴 Hard"
}

difficulty = difficulty_icons.get(
    question.get("difficulty", "Medium"),
    "🟡 Medium"
)

beans = min((index + 1) * 10, 500)
filled = beans // 25
empty = 20 - filled
progress = "█" * filled + "░" * empty

markdown = f"""
# ☕ Fuel the Coders

> **Coffee fuels developers. Curiosity fuels innovation.**

Every **6 hours**, a brand-new Software Engineering or AI interview challenge appears.

Answer it before revealing the solution!

---

## 🧠 Interview Question #{index + 1}

🏷️ **Category:** {question["category"]}

🎯 **Difficulty:** {difficulty}

---

### {question["question"]}

🅰️ {options[0]}

🅱️ {options[1]}

🅲 {options[2]}

🅳 {options[3]}

<details>

<summary>☕ Reveal Answer</summary>

## ✅ Correct Answer

**{question["answer"]}**

---

### 💡 Explanation

{question["explanation"]}

</details>

---

# ☕

## Community Coffee Jar

```text
{progress}

🫘 {beans}/500 Beans
```

> Every solved challenge symbolically adds one coffee bean to the community jar.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏳ **Next Challenge:** 6 Hours

⭐ Happy Coding!
""".strip()

with open(README, "r", encoding="utf-8") as f:
    readme = f.read()

start = readme.find(QUESTION_START)
end = readme.find(QUESTION_END)

if start == -1 or end == -1:
    raise Exception(
        "README markers not found. Add:\n"
        "<!-- QUESTION_START -->\n"
        "<!-- QUESTION_END -->"
    )

end += len(QUESTION_END)

new_section = (
    QUESTION_START
    + "\n\n"
    + markdown
    + "\n\n"
    + QUESTION_END
)

updated_readme = (
    readme[:start]
    + new_section
    + readme[end:]
)

with open(README, "w", encoding="utf-8") as f:
    f.write(updated_readme)

print("README updated successfully!")
