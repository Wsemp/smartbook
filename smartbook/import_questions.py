
import os
import django
import json

from pathlib import Path
from django.db import transaction

# Inicjalizacja Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartbook.settings")
django.setup()

from database.models import Question, Answer, Level

# Ścieżka do pliku JSON
BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "questions.json"

# Odczyt pliku JSON
with open(JSON_FILE, "r", encoding="utf-8") as file:
    questions_data = json.load(file)

imported = 0
failed = 0

# Import każdego pytania osobno
for index, data in enumerate(questions_data, start=1):
    try:
        with transaction.atomic():

            level = Level.objects.get(id=data["level_id"])

            if not Question.objects.filter(question=data["question"]).exists():

                question = Question.objects.create(
                    level=level,
                    question=data["question"],
                    difficulty=data["difficulty"],
                    points=data["points"],
                    explanation=data.get("explanation", "")
                )

                for answer_data in data["answers"]:
                    Answer.objects.create(
                        question=question,
                        answer_text=answer_data["answer_text"],
                        is_correct=answer_data["is_correct"],
                        error_type=answer_data.get("error_type"),
                        explanation=answer_data.get("explanation", "")
                    )

                imported += 1
                print(f"Zaimportowano pytanie {index}")

            else:
                print(f"Pytanie już istnieje {data['question']}")

    except Exception as error:
        failed += 1
        print(f"Błąd przy pytaniu {index}: {error}")

print("\nImport zakończony!")
print(f"Zaimportowano: {imported}")
print(f"Błędy: {failed}")
