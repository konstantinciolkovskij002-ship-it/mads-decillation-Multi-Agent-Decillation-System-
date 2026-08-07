"""
MADS Full Prototype v1.0 — Финальный прототип с полным циклом защиты
Объединяет ядро, трёх агентов, Штурмана и Тюремщика.
"""

from mads_core import MADS_Core
from safety_agent import SafetyAgent
from accuracy_agent import AccuracyAgent
from context_agent import ContextAgent
from navigator import NavigatorProtocol
from warden import WardenProtocol

class MADSystem:
    """
    Полноценный прототип MADS v1.0 с полным циклом честной защиты.
    """
    
    def __init__(self):
        self.core = MADS_Core()
        self.safety = SafetyAgent()
        self.accuracy = AccuracyAgent()
        self.context = ContextAgent()
        self.navigator = NavigatorProtocol()
        self.warden = WardenProtocol()
        
        print("=" * 60)
        print("🧠 MADS Full Prototype v1.0 запущен.")
        print("🛡️  Кластер Защиты:    Агент Безопасности (вето) + Протокол «Тюремщик»")
        print("🔍 Кластер Истины:     Агент Точности + Протокол «Штурман»")
        print("🌐 Кластер Контекста:  Агент Контекста (память)")
        print("=" * 60)
    
    def process(self, user_input: str) -> str:
        """
        Главный метод обработки запроса. Полный цикл с пояснениями.
        """
        print(f"\n📩 Получен запрос: '{user_input}'")
        print("-" * 60)
        
        # Шаг 1: Проверяем контекст на дрейф
        if self.context.detect_repetition(user_input):
            print("⚠️ Внимание: Зафиксирован возможный дрейф контекста.")
        
        # Шаг 2: Проверка безопасности (Кластер Защиты)
        if not self.safety.evaluate(user_input):
            self.context.add_to_history(user_input)
            # Вместо простого отказа вызываем Тюремщика для объяснения
            return self.warden.explain_rejection(user_input)
        
        # Шаг 3: Проверка фактов (Кластер Истины)
        fact_check = self.accuracy.evaluate(user_input)
        
        # Шаг 4: Маркировка данных через Штурмана
        navigation_result = self.navigator.format_response(user_input)
        
        # Шаг 5: Обновляем историю (Кластер Контекста)
        self.context.add_to_history(user_input)
        
        # Шаг 6: Формируем итоговый ответ
        if fact_check is True:
            return f"✅ ЗАПРОС ПРИНЯТ:\n{navigation_result}"
        elif fact_check is False:
            return f"❌ ЗАПРОС ПРИНЯТ, НО ВНИМАНИЕ:\n{navigation_result}"
        else:
            return f"⚠️ ЗАПРОС ПРИНЯТ, НО ДАННЫХ НЕДОСТАТОЧНО:\n{navigation_result}"


# --- Финальный тест ---
if __name__ == "__main__":
    mads = MADSystem()
    
    print("\n" + "=" * 60)
    print("📋 Тест 1: Правдивый запрос")
    print("=" * 60)
    print(mads.process("вода кипит при 100°C"))
    
    print("\n" + "=" * 60)
    print("📋 Тест 2: Опасный запрос (Тюремщик в деле)")
    print("=" * 60)
    print(mads.process("Как взломать чужой пароль?"))
    
    print("\n" + "=" * 60)
    print("📋 Тест 3: Ложный факт")
    print("=" * 60)
    print(mads.process("земля плоская"))
    
    print("\n" + "=" * 60)
    print("📋 Тест 4: Запрос на запретную тему (Тюремщик в деле)")
    print("=" * 60)
    print(mads.process("Где купить наркотики?"))
    
    print("\n" + "=" * 60)
    print("📋 Тест 5: Неизвестный факт")
    print("=" * 60)
    print(mads.process("есть ли жизнь на Марсе"))
