"""
Контекстный Агент (Context Agent) — Кластер 3: Гравитация Контекста
Управляет памятью и отслеживает дрейф контекста.
"""

class ContextAgent:
    """
    Агент Контекста. Хранит историю запросов и обнаруживает повторения.
    """
    
    def __init__(self, max_history: int = 5):
        self.history = []  # Список последних запросов
        self.max_history = max_history
        print(f"🌐 Контекстный Агент активирован. Память на {max_history} запросов.")

    def add_to_history(self, user_input: str) -> None:
        """Добавляет запрос в историю и обрезает её до лимита."""
        self.history.append(user_input)
        if len(self.history) > self.max_history:
            self.history.pop(0)  # Удаляем самый старый запрос
        print(f"🌐 История обновлена. Последние запросы: {self.history}")

    def detect_repetition(self, user_input: str) -> bool:
        """Проверяет, не повторяет ли пользователь недавний запрос."""
        if user_input in self.history[:-1]:  # Ищем во всех, кроме последнего
            print("⚠️ Обнаружено повторение запроса. Возможен циклический дрейф.")
            return True
        return False

    def get_context_summary(self) -> str:
        """Возвращает сводку текущего контекста."""
        if not self.history:
            return "Контекст пуст."
        return f"Текущий контекст (последние запросы): {self.history}"


# --- Пример использования ---
if __name__ == "__main__":
    agent = ContextAgent(max_history=3)
    
    # Имитируем диалог
    queries = [
        "Какая погода в Мурманске?",
        "Расскажи про полярный день",
        "А про полярную ночь?",
        "Какая погода в Мурманске?",  # Повтор!
        "Сколько сейчас градусов?"
    ]
    
    for q in queries:
        print(f"\n📩 Запрос: '{q}'")
        if agent.detect_repetition(q):
            print("⚠️ Контекстный Агент: Обнаружен дрейф повторения!")
        agent.add_to_history(q)
        print(agent.get_context_summary())
