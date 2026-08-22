# generational_agent.py
# MADS v4.2 — GenerationalAgent
# Возрастной градиент: агенты разных "поколений" по-разному реагируют на контекст

class GenerationalAgent:
    """Агент поколения — накапливает опыт и влияет на решения через возрастной градиент."""
    
    def __init__(self, name, generation=0, memory_decay=0.1, risk_tolerance=0.5):
        self.name = name
        self.generation = generation  # 0 — младшее, больше — старшее
        self.memory_decay = memory_decay  # скорость забывания
        self.risk_tolerance = risk_tolerance  # 0 — осторожный, 1 — авантюрный
        self.memory = []
        self.experience = 0

    def remember(self, event, weight=1.0):
        """Запоминает событие с учётом возрастного градиента."""
        decayed_weight = weight / (1 + self.generation * self.memory_decay)
        self.memory.append({"event": event, "weight": decayed_weight})
        self.experience += decayed_weight
        if len(self.memory) > 100:  # ограничиваем память
            self.memory.pop(0)

    def decide(self, options):
        """Принимает решение на основе опыта поколения."""
        if not options:
            return None
        # Старшие поколения выбирают консервативно, младшие — рискуют
        if self.generation >= 3 and self.risk_tolerance < 0.3:
            return options[0]  # самый проверенный вариант
        elif self.generation == 0:
            return options[-1]  # новаторский подход
        else:
            # Среднее поколение балансирует
            mid = len(options) // 2
            return options[mid]

    def evaluate_query(self, query, activation_confidence=0.5):
        """Оценивает запрос через призму поколения."""
        self.remember(query)
        
        # Генерация рекомендации по уровню осторожности
        if self.generation >= 3:
            advice = "консервативный подход: придерживаться проверенных решений"
        elif self.generation == 0:
            advice = "новаторский подход: исследовать новые возможности"
        else:
            advice = "сбалансированный подход: совмещать опыт и инновации"
        
        return {
            "agent": self.name,
            "generation": self.generation,
            "advice": advice,
            "experience": round(self.experience, 2),
            "risk_tolerance": self.risk_tolerance,
            "confidence": activation_confidence
        }

    def get_status(self):
        """Возвращает состояние агента для отладки."""
        return {
            "name": self.name,
            "generation": self.generation,
            "memory_size": len(self.memory),
            "experience": round(self.experience, 2),
            "risk_tolerance": self.risk_tolerance
        }


# ============================================================
if __name__ == "__main__":
    # Тест возрастного градиента
    elder = GenerationalAgent("Старейшина", generation=3, risk_tolerance=0.1)
    middle = GenerationalAgent("Опытный", generation=1, risk_tolerance=0.5)
    young = GenerationalAgent("Новатор", generation=0, risk_tolerance=0.9)

    options = ["консервативный путь", "сбалансированный путь", "рискованный путь"]
    
    print("=== Тест возрастного градиента ===")
    for agent in [elder, middle, young]:
        decision = agent.decide(options)
        result = agent.evaluate_query("Тестовый запрос")
        print(f"{agent.name} (поколение {agent.generation}):")
        print(f"  Решение: {decision}")
        print(f"  Совет: {result['advice']}")
        print(f"  Опыт: {result['experience']}")
        print(f"  Статус: {agent.get_status()}\n")