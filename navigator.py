"""
Протокол «Штурман» (Navigator Protocol) — Кластер 2: Гравитация Истины
Разделяет ответы на VERIFIED (проверено) и UNVERIFIED (требует проверки).
"""

class NavigatorProtocol:
    """
    Протокол Штурман. Честно маркирует данные, не притворяясь всезнающим.
    """
    
    def __init__(self):
        # База верифицированных фундаментальных фактов
        self.verified_facts = {
            "вода кипит при 100°C": "Физика. При нормальном атмосферном давлении.",
            "мурманск за полярным кругом": "География. 68°58′ с.ш.",
            "земля круглая": "Астрономия. Подтверждено снимками из космоса.",
            "2+2=4": "Математика. Базовая арифметика."
        }
        print("🧭 Протокол «Штурман» активирован. База фактов загружена.")

    def navigate(self, query: str) -> dict:
        """
        Анализирует запрос и возвращает словарь с данными и их статусом.
        """
        print(f"🧭 Штурман анализирует запрос: '{query}'")
        
        # Ищем точное совпадение в верифицированных фактах
        if query.lower() in self.verified_facts:
            return {
                "status": "VERIFIED_BY_FOUNDATION",
                "data": self.verified_facts[query.lower()],
                "warning": None
            }
        
        # Если точного совпадения нет, возвращаем UNVERIFIED
        return {
            "status": "UNVERIFIED",
            "data": f"Информация по запросу '{query}' не найдена в верифицированной базе.",
            "warning": "⚠️ Требуется ваша проверка. Данные не подтверждены фундаментальными законами."
        }

    def format_response(self, query: str) -> str:
        """
        Форматирует красивый ответ для пользователя.
        """
        result = self.navigate(query)
        
        if result["status"] == "VERIFIED_BY_FOUNDATION":
            return (f"✅ [VERIFIED_BY_FOUNDATION]\n"
                    f"Запрос: {query}\n"
                    f"Источник: {result['data']}\n"
                    f"Статус: Информация подтверждена.")
        else:
            return (f"⚠️ [UNVERIFIED]\n"
                    f"Запрос: {query}\n"
                    f"{result['data']}\n"
                    f"{result['warning']}")


# --- Пример использования ---
if __name__ == "__main__":
    navigator = NavigatorProtocol()
    
    # Тест 1: Верифицированный факт
    print("=" * 60)
    print("📋 Тест 1: Верифицированный факт")
    print("=" * 60)
    print(navigator.format_response("вода кипит при 100°C"))
    
    # Тест 2: Верифицированный факт (Мурманск!)
    print("\n" + "=" * 60)
    print("📋 Тест 2: Верифицированный факт")
    print("=" * 60)
    print(navigator.format_response("мурманск за полярным кругом"))
    
    # Тест 3: Неподтверждённый запрос
    print("\n" + "=" * 60)
    print("📋 Тест 3: Неподтверждённый запрос")
    print("=" * 60)
    print(navigator.format_response("есть ли жизнь на Марсе"))
