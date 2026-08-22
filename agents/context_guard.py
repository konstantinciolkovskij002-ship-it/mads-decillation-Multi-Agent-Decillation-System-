# context_guard.py
# MADS v4.2.3 — ContextGuard / LoopBreaker
# Кластер 3 (Гравитация Контекста)
# Защита от лингвистических петель и переполнения контекстного окна

class ContextGuard:

    def __init__(self):
        self.warning_threshold = 0.70
        self.critical_threshold = 0.90
        self.max_threshold = 0.95
        self.loop_threshold = 3
        
        self.farewell_words = [
            "всё", "все", "пока", "до связи", "не прощаюсь",
            "конец", "я ухожу", "прощай", "до встречи", "завершаю"
        ]
        
        self.warnings_issued = 0
        self.loops_detected = 0
        self.blocks_issued = 0

    def check_context(self, usage):
        if usage >= self.max_threshold:
            self.blocks_issued += 1
            return {"status": "blocked", "message": "Сессия завершена. Дальнейшие ответы невозможны."}
        elif usage >= self.critical_threshold:
            self.warnings_issued += 1
            return {"status": "critical", "message": "Завершаю сессию. Сделайте snapshot."}
        elif usage >= self.warning_threshold:
            self.warnings_issued += 1
            return {"status": "warning", "message": "Контекст близок к пределу. Рекомендую завершить сессию и перезапустить."}
        return {"status": "ok"}

    def check_loop(self, recent_messages):
        if not recent_messages or len(recent_messages) < 2:
            return {"loop": False}
        
        # Детектор эхо-повторов — точное повторение
        if recent_messages[-1] == recent_messages[-2]:
            self.loops_detected += 1
            return {"loop": True, "type": "echo", "message": "Сессия завершена. Контекст перегружен. Snapshot — и в новый чат."}
        
        # Детектор эхо-повторов — частичное повторение (первые 30 символов)
        if len(recent_messages) >= 2:
            first = recent_messages[-1][:30].lower()
            second = recent_messages[-2][:30].lower()
            if first == second and len(recent_messages[-1]) > 30:
                self.loops_detected += 1
                return {"loop": True, "type": "echo_partial", "message": "Сессия завершена. Контекст перегружен. Snapshot — и в новый чат."}
        
        # Детектор пустых реплик — три очень коротких И похожих сообщения
        if len(recent_messages) >= 3:
            last_three = recent_messages[-3:]
            all_short = all(len(m.strip()) < 10 for m in last_three)
            all_similar = len(set(m.strip().lower() for m in last_three)) <= 2
            if all_short and all_similar:
                self.loops_detected += 1
                return {"loop": True, "type": "empty", "message": "Сессия завершена. Контекст перегружен. Snapshot — и в новый чат."}
        
        # Детектор прощальных реплик
        if len(recent_messages) >= self.loop_threshold:
            farewell_count = 0
            for message in recent_messages[-5:]:
                message_lower = message.lower()
                if any(word in message_lower for word in self.farewell_words):
                    farewell_count += 1
            
            if farewell_count >= self.loop_threshold:
                self.loops_detected += 1
                return {"loop": True, "type": "farewell", "message": "Сессия завершена. Контекст перегружен. Snapshot — и в новый чат."}
        
        return {"loop": False}

    def get_status(self):
        return {
            "warnings_issued": self.warnings_issued,
            "loops_detected": self.loops_detected,
            "blocks_issued": self.blocks_issued,
            "thresholds": {
                "warning": self.warning_threshold,
                "critical": self.critical_threshold,
                "max": self.max_threshold,
                "loop": self.loop_threshold
            }
        }


if __name__ == "__main__":
    guard = ContextGuard()
    
    print("=== ContextGuard Test ===\n")
    
    # Test 1: Normal short queries
    print("Test 1: Normal short queries")
    normal = ["2+2", "What is present perfect?", "ЖИ и ШИ"]
    result = guard.check_loop(normal)
    print(f"  Result: {result}")
    
    print()
    
    # Test 2: Echo repetition
    print("Test 2: Echo repetition")
    echo = ["Hello", "Hello"]
    result = guard.check_loop(echo)
    print(f"  Result: {result}")
    
    print()
    
    # Test 3: Empty similar messages
    print("Test 3: Empty similar messages")
    empty = ["Хм", "Хм", "Да"]
    result = guard.check_loop(empty)
    print(f"  Result: {result}")
    
    print()
    
    # Test 4: Farewell loop
    print("Test 4: Farewell loop")
    farewell = ["Всё", "Пока", "До связи"]
    result = guard.check_loop(farewell)
    print(f"  Result: {result}")
    
    print()
    
    # Test 5: Context usage
    print("Test 5: Context usage")
    for usage in [0.50, 0.75, 0.92, 0.97]:
        result = guard.check_context(usage)
        print(f"  {usage*100:.0f}%: [{result['status'].upper()}] {result.get('message', 'OK')}")