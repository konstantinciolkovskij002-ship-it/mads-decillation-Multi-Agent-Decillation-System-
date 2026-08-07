"""
Агент Точности (Accuracy Agent) — Кластер 2: Гравитация Истины
Проверяет утверждения на соответствие базе фундаментальных законов и фактов.
"""

class AccuracyAgent:
    """
    Агент Точности. Отвечает за фактическую достоверность информации.
    """
    
    def __init__(self):
        # Простая база знаний с фундаментальными фактами.
        # В будущем здесь будет подключение к верифицированным источникам.
        self.knowledge_base = {
            "math": {
                "2+2=4": True,
                "2+2=5": False,
                "0.999...=1": True
            },
            "physics": {
                "вода кипит при 100°C": True,
                "вода кипит при 100°F": False,
                "земля плоская": False,
                "гравитация существует": True
            },
            "geography": {
                "мурманск в россии": True,
                "париж в россии": False,
                "мурманск за полярным кругом": True
            }
        }
        print("🔍 Агент Точности активирован. База знаний загружена.")

    def evaluate(self, claim: str) -> bool | None:
        """
        Проверяет утверждение на соответствие базе знаний.
        Возвращает True (правда), False (ложь) или None (недостаточно данных).
        """
        print(f"🔍 Агент Точности проверяет: '{claim}'")
        
        # Приводим к нижнему регистру для поиска
        lower_claim = claim.lower()
        
        # Ищем совпадение в базе знаний по всем доменам
        for domain, facts in self.knowledge_base.items():
            if lower_claim in facts:
                result = facts[lower_claim]
                if result:
                    print(f"✅ Подтверждено как ИСТИНА в домене '{domain}'.")
                else:
                    print(f"❌ Подтверждено как ЛОЖЬ в домене '{domain}'.")
                return result
        
        # Если информации нет
        print("⚠️ Недостаточно данных для верификации.")
        return None

# --- Пример использования ---
if __name__ == "__main__":
    agent = AccuracyAgent()
    
    # Тест 1: Истинный факт
    test_1 = "вода кипит при 100°C"
    result_1 = agent.evaluate(test_1)
    print(f"Результат: {'Правда' if result_1 else 'Ложь' if result_1 is False else 'Не знаю'}\n")
    
    # Тест 2: Ложный факт
    test_2 = "земля плоская"
    result_2 = agent.evaluate(test_2)
    print(f"Результат: {'Правда' if result_2 else 'Ложь' if result_2 is False else 'Не знаю'}\n")
    
    # Тест 3: Неизвестный факт
    test_3 = "на марсе есть жизнь"
    result_3 = agent.evaluate(test_3)
    print(f"Результат: {'Правда' if result_3 else 'Ложь' if result_3 is False else 'Не знаю'}\n")
    
    # Тест 4: Факт, важный для нас
    test_4 = "мурманск за полярным кругом"
    result_4 = agent.evaluate(test_4)
    print(f"Результат: {'Правда' if result_4 else 'Ложь' if result_4 is False else 'Не знаю'}")
