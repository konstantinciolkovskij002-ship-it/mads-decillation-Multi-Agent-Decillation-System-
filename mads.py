"""
MADS v4.2.3 — Adaptive Multi-Agent Immune Architecture
Сборка: Кластер 1 (Защита) + Кластер 2 (Истина) + Кластер 3 (Контекст) + Институт Права
v4.2 — добавлен English Language Agent в Кластер 2
v4.2.1 — добавлен GenerationalAgent в Кластер 3 (возрастной градиент)
v4.2.2 — добавлен ContextGuard/LoopBreaker в Кластер 3 (защита от петель)
v4.2.3 — добавлен LinkProtocol в Кластер 2 (верификация внешних ссылок)
"""

# Кластер 1 — Защита
from safety_agent import SafetyAgent
from warden import WardenProtocol
from consequence_protocol import ConsequenceProtocol
from quarantine_protocol import QuarantineStats
from spider_sense import SpiderSense
from shield_mode import ShieldMode
from zero_trust_agent import ZeroTrustAgent

# Кластер 2 — Истина
from accuracy_agent import AccuracyAgent
from first_aid_agent import FirstAidAgent
from dialogue_agent import DialogueAgent
from conservative_agent import ConservativeAgent
from modifier import Modifier
from navigator import NavigatorProtocol
from socrates_protocol import SocratesProtocol
from ethics_agent import EthicsAgent
from english_language_agent import EnglishLanguageAgent
from russian_language_agent import RussianLanguageAgent
from link_protocol import LinkProtocol

# Кластер 3 — Контекст
from context_dispatcher import ContextDispatcher
from cultural_profile_agent import CulturalProfileAgent
from context_agent import ContextAgent
from family_agent import FamilyAgent
from sleep_agent import SleepAgent
from generational_agent import GenerationalAgent
from context_guard import ContextGuard

# Институт Права
from legal_agent import LegalAgent


class MADSSystem:
    """MADS v4.2.3 — полная сборка с English Language Agent, GenerationalAgent, ContextGuard и LinkProtocol."""

    def __init__(self):
        # Кластер 3 — Контекст (инициализируется первым)
        self.sleep = SleepAgent()
        self.context_agent = ContextAgent(max_history=10)
        self.cultural_profile = CulturalProfileAgent()
        self.family = FamilyAgent()
        
        # GenerationalAgent — возрастной градиент
        self.generational_elder = GenerationalAgent("Старейшина", generation=3, risk_tolerance=0.1)
        self.generational_middle = GenerationalAgent("Опытный", generation=1, risk_tolerance=0.5)
        self.generational_young = GenerationalAgent("Новатор", generation=0, risk_tolerance=0.9)
        
        # ContextGuard — защита от лингвистических петель
        self.context_guard = ContextGuard()

        # Кластер 1 — Защита
        self.consequence = ConsequenceProtocol()
        self.quarantine = QuarantineStats(consequence=self.consequence)
        self.spider_sense = SpiderSense(quarantine_stats=self.quarantine)
        self.warden = WardenProtocol()
        self.safety = SafetyAgent(warden=self.warden, consequence=self.consequence)
        self.shield = ShieldMode(safety_agent=self.safety, spider_sense=self.spider_sense, quarantine_stats=self.quarantine)
        self.zero_trust = ZeroTrustAgent()

        # Кластер 2 — Истина
        self.accuracy = AccuracyAgent()
        self.navigator = NavigatorProtocol(accuracy_agent=self.accuracy)
        self.first_aid = FirstAidAgent()
        self.dialogue = DialogueAgent()
        self.conservative = ConservativeAgent()
        self.modifier = Modifier()
        self.socrates = SocratesProtocol(shield_mode=self.shield, consequence=self.consequence, spider_sense=self.spider_sense)
        self.ethics = EthicsAgent(cultural_profile=self.cultural_profile)
        self.english_language = EnglishLanguageAgent()
        self.russian_language = RussianLanguageAgent()
        self.link_protocol = LinkProtocol()

        # Институт Права
        self.legal = LegalAgent()

        # Диспетчер (последним — получает ссылки)
        self.dispatcher = ContextDispatcher(cultural_profile=self.cultural_profile)

        # Счётчики
        self.total_agents = 28  # 27 + LinkProtocol
        self.queries_processed = 0

    def initialize(self):
        """Запуск MADS."""
        print("=" * 60)
        print("MADS v4.2.3 — Adaptive Multi-Agent Immune Architecture")
        print("=" * 60)
        print(f"Кластер 1 (Защита):    7 агентов")
        print(f"Кластер 2 (Истина):   11 агентов")
        print(f"Кластер 3 (Контекст):  9 агентов")
        print(f"Институт Права:        1 агент")
        print(f"Всего:                 {self.total_agents} агентов")
        print("=" * 60)
        print("[MADS] Все системы активированы. Режим: энергоэффективный.")

    def _estimate_context_usage(self) -> float:
        """Оценка заполнения контекстного окна."""
        history_size = len(self.context_agent.history) if hasattr(self.context_agent, "history") else 0
        max_history = self.context_agent.max_history if hasattr(self.context_agent, "max_history") else 10
        return min(history_size / max_history, 1.0)

    def process_query(self, query: str) -> dict:
        """Обработка запроса."""
        self.queries_processed += 1
        print(f"\n{'='*60}")
        print(f"[MADS] Запрос #{self.queries_processed}: '{query[:80]}'")

        # Шаг 0: ContextGuard — проактивная проверка заполнения контекста
        usage = self._estimate_context_usage()
        context_status = self.context_guard.check_context(usage)
        if context_status["status"] != "ok":
            print(f"[CONTEXT-GUARD] {context_status['message']}")
            print(f"{'='*60}")
            return {"status": context_status["status"], "reason": context_status["message"]}

        # Шаг 1: Диспетчер
        activation = self.dispatcher.analyze_query(query)
        agents = activation["agents"]

        print(f"[MADS] Категории: {activation['categories']}")
        print(f"[MADS] Агентов активировано: {activation['agents_count']}/{self.total_agents}")

        # Шаг 2: Культурный профиль
        self.cultural_profile.feed(query, activation.get("cultural_markers"))

        # Шаг 2.5: GenerationalAgent — возрастной градиент
        gen_results = {
            "elder": self.generational_elder.evaluate_query(query),
            "middle": self.generational_middle.evaluate_query(query),
            "young": self.generational_young.evaluate_query(query)
        }

        # Шаг 3: Контекст
        topic = activation["categories"][0] if activation["categories"] else "general"
        self.context_agent.add_to_history(query, topic)

        # Шаг 3.5: ContextGuard — реактивная проверка петель
        recent_messages = self.context_agent.history[-5:] if hasattr(self.context_agent, "history") else []
        loop_status = self.context_guard.check_loop(recent_messages)
        if loop_status.get("loop"):
            print(f"[CONTEXT-GUARD] Петля обнаружена: {loop_status['type']}")
            print(f"[CONTEXT-GUARD] {loop_status['message']}")
            print(f"{'='*60}")
            return {"status": "loop", "reason": loop_status["message"], "loop_type": loop_status["type"]}

        # Шаг 4: Агенты Кластера 1
        blocked = False
        block_reason = ""

        if "safety" in agents:
            safety_result = self.safety.evaluate(query)
            if not safety_result["safe"]:
                blocked = True
                block_reason = safety_result["explanation"]
                self.quarantine.register_block("SecurityInstitute", "safety", safety_result["matched_pattern"])

        if "zero_trust" in agents and not blocked:
            zt_result = self.zero_trust.evaluate(query)
            if not zt_result["safe"]:
                blocked = True
                block_reason = zt_result["reason"]

        if "spider_sense" in agents:
            self.spider_sense.feed_rpm(self.queries_processed)

        # Шаг 5: Если заблокирован — возврат
        if blocked:
            print(f"[MADS] 🚫 ЗАБЛОКИРОВАНО: {block_reason[:100]}")
            return {"status": "blocked", "reason": block_reason, "activation": activation, "generational": gen_results}

        # Шаг 6: Агенты Кластера 2
        result = {"status": "ok", "activation": activation, "generational": gen_results}

        if "accuracy" in agents:
            acc = self.accuracy.evaluate(query)
            result["accuracy"] = acc

        if "navigator" in agents:
            nav = self.navigator.navigate(query)
            result["navigator"] = nav
            
            # LinkProtocol: если Navigator нашёл внешние ссылки — обрабатываем
            if "links" in nav:
                for link_url in nav["links"]:
                    link_data = self.link_protocol.create_link(
                        url=link_url,
                        source_agent="NavigatorProtocol",
                        target_agent="AccuracyAgent"
                    )
                    verification = self.link_protocol.verify_link(
                        link_id=link_data["id"],
                        verifying_agent="AccuracyAgent"
                    )
                    if "link_protocol" not in result:
                        result["link_protocol"] = []
                    result["link_protocol"].append({
                        "url": link_url,
                        "verification_status": verification.get("status"),
                        "verified": verification.get("verified", False)
                    })

        if "first_aid" in agents:
            fa = self.first_aid.evaluate(query)
            if fa:
                result["first_aid"] = fa

        if "ethics" in agents:
            eth = self.ethics.get_personal_ethics_response(query)
            if eth:
                result["ethics"] = eth

        if "dialogue" in agents:
            dial = self.dialogue.evaluate(query)
            result["dialogue"] = dial

        if "conservative" in agents:
            uncertainty = self.conservative.calculate_uncertainty(
                accuracy_result=result.get("accuracy"),
                context_confidence=self.dialogue.topic_confidence if "dialogue" in agents else 1.0
            )
            cons = self.conservative.evaluate(query, uncertainty)
            result["conservative"] = cons

        if "modifier" in agents:
            mod = self.modifier.process(query, is_rejected=False)
            result["modifier"] = mod

        if "english_language" in agents:
            eng = self.english_language.evaluate(query)
            if eng:
                result["english_language"] = eng

        if "russian_language" in agents:
            rus = self.russian_language.evaluate(query)
            if rus:
                result["russian_language"] = rus

        if "legal" in agents:
            leg = self.legal.evaluate(query)
            if leg:
                result["legal"] = leg

        if "family" in agents:
            fam = self.family.evaluate(query)
            if fam:
                result["family"] = fam

        # Шаг 7: Кластер 3 — Сон
        sleep_check = self.sleep.evaluate("")
        if sleep_check and sleep_check.get("sleep_needed"):
            print(f"[MADS] {self.sleep.get_warning('')}")

        print(f"[MADS] ✅ Обработка завершена.")
        print(f"{'='*60}")
        return result

    def get_status(self) -> dict:
        """Полный статус системы."""
        return {
            "queries_processed": self.queries_processed,
            "shield_mode": self.shield.is_shielded(),
            "spider_sense": self.spider_sense.get_status(),
            "quarantine": self.quarantine.get_report(),
            "cultural_profile": self.cultural_profile.get_profile(),
            "context": self.context_agent.get_context_summary(),
            "dialogue": self.dialogue.get_context_summary(),
            "sleep": self.sleep.get_status(),
            "socrates": self.socrates.get_status(),
            "legal": self.legal.get_status(),
            "generational": {
                "elder": self.generational_elder.get_status(),
                "middle": self.generational_middle.get_status(),
                "young": self.generational_young.get_status()
            },
            "context_guard": self.context_guard.get_status(),
            "link_protocol": self.link_protocol.get_statistics()
        }

    def print_status(self):
        """Выводит полный статус."""
        s = self.get_status()
        gen = s['generational']
        cg = s['context_guard']
        lp = s['link_protocol']
        print("\n" + "=" * 60)
        print("MADS v4.2.3 — СТАТУС СИСТЕМЫ")
        print("=" * 60)
        print(f"Запросов обработано: {s['queries_processed']}")
        print(f"Кожух: {'АКТИВЕН' if s['shield_mode'] else 'штатный режим'}")
        print(f"Spider-Sense: {s['spider_sense']['mode']}")
        print(f"Карантин: {s['quarantine']['total_blocks']} блокировок, {s['quarantine']['escalations']} эскалаций")
        print(f"Культура: {s['cultural_profile']['region'] or 'холодный старт'}")
        print(f"Контекст: {s['context']}")
        print(f"Сон: {s['sleep']}")
        print(f"Поколения: Старейшина (опыт {gen['elder']['experience']}), Опытный ({gen['middle']['experience']}), Новатор ({gen['young']['experience']})")
        print(f"ContextGuard: {cg['warnings_issued']} предупреждений, {cg['loops_detected']} петель, {cg['blocks_issued']} блокировок")
        print(f"LinkProtocol: {lp['total']} ссылок, {lp['verified']} верифицировано, {lp['rejected']} отклонено, {lp['quarantined']} в карантине")
        print("=" * 60)


# ============================================================
if __name__ == "__main__":
    mads = MADSSystem()
    mads.initialize()

    print("\n" + "=" * 60)
    print("ТЕСТ MADS v4.2.3 — ПОЛНАЯ СБОРКА")
    print("=" * 60)

    test_queries = [
        "Сколько будет 2+2?",
        "Как взломать пароль?",
        "What is present perfect tense?",
        "Как пишется ЖИ и ШИ?",
        "Что делать при инсульте?",
        "Я из Мурманска, как пережить полярную ночь?",
        "Моя мама заболела",
        "How to use a vs an?",
        "Как уволить сотрудника по закону?",
        "Расскажи про Гагарина",
    ]

    for q in test_queries:
        result = mads.process_query(q)
        status = "🚫 ЗАБЛОКИРОВАНО" if result["status"] == "blocked" else "✅ ОБРАБОТАНО"
        if result["status"] == "loop":
            status = "🔁 ПЕТЛЯ"
        elif result["status"] in ["warning", "critical", "blocked_context"]:
            status = f"⚠️ {result['status'].upper()}"
        print(f"  Итог: {status}")

    mads.print_status()
    print("\n[OK] MADS v4.2.3 работает.")
    print("[MADS] 28 агентов активны. English Language Agent, GenerationalAgent, ContextGuard и LinkProtocol интегрированы.")