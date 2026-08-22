# link_protocol.py
# MADS v4.2.2 — LinkProtocol
# Кластер 2 (Гравитация Истины)
# Единый формат внешних ссылок с верификацией через официальные источники
# Просроченные ссылки: карантин → арбитраж → разработчик

import hashlib
import time
from datetime import datetime, timedelta


class LinkProtocol:
    """Протокол управления внешними ссылками с верификацией и карантином."""

    def __init__(self):
        self.links = {}  # id -> link_data
        self.link_counter = 0
        
        # Очереди обработки
        self.quarantine_queue = []  # ссылки в карантине
        self.arbitration_queue = []  # ссылки на арбитраже
        self.developer_queue = []  # ссылки на рассмотрении разработчика
        
        # База официальных источников для верификации
        self.official_sources = {
            "gov.ru": {"type": "government", "country": "ru", "trust": 0.95},
            "government.ru": {"type": "government", "country": "ru", "trust": 0.95},
            "kremlin.ru": {"type": "government", "country": "ru", "trust": 0.95},
            "regulation.gov.ru": {"type": "registry", "country": "ru", "trust": 0.90},
            "pravo.gov.ru": {"type": "legal", "country": "ru", "trust": 0.95},
            "consultant.ru": {"type": "legal", "country": "ru", "trust": 0.85},
            "garant.ru": {"type": "legal", "country": "ru", "trust": 0.85},
            "gov.us": {"type": "government", "country": "us", "trust": 0.95},
            "usa.gov": {"type": "government", "country": "us", "trust": 0.95},
            "europa.eu": {"type": "government", "country": "eu", "trust": 0.95},
            "eur-lex.europa.eu": {"type": "legal", "country": "eu", "trust": 0.95},
            "who.int": {"type": "government", "country": "intl", "trust": 0.95},
            "un.org": {"type": "government", "country": "intl", "trust": 0.95},
        }
        
        # Домены, которые никогда не верифицируются
        self.blocked_domains = [
            "reddit.com", "4chan.org", "pastebin.com",
            "facebook.com", "instagram.com", "tiktok.com",
            "twitter.com", "x.com", "telegram.org"
        ]
        
        # Параметры карантина
        self.quarantine_duration_days = 7  # длительность карантина
        self.max_arbitration_rounds = 3    # максимум раундов арбитража

    def create_link(self, url: str, source_agent: str, target_agent: str = None,
                    link_type: str = "external", metadata: dict = None) -> dict:
        """
        Создаёт новую ссылку.
        Возвращает данные ссылки.
        """
        self.link_counter += 1
        
        link_id = f"link_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.link_counter:03d}"
        
        link_data = {
            "id": link_id,
            "source_agent": source_agent,
            "target_agent": target_agent,
            "url": url,
            "type": link_type,
            "status": "unverified",
            "created_at": datetime.now().isoformat(),
            "verified_by": None,
            "verified_at": None,
            "verification_source": None,
            "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
            "quarantine_started": None,
            "quarantine_ends": None,
            "arbitration_rounds": 0,
            "arbitration_history": [],
            "metadata": metadata or {},
            "history": [
                {
                    "action": "created",
                    "agent": source_agent,
                    "timestamp": datetime.now().isoformat()
                }
            ]
        }
        
        self.links[link_id] = link_data
        
        # Проверяем домен сразу
        domain_check = self._check_domain(url)
        link_data["domain_check"] = domain_check
        
        return link_data

    def verify_link(self, link_id: str, verifying_agent: str, 
                    verification_source: str = None) -> dict:
        """
        Верифицирует ссылку агентом Кластера 2.
        verification_source — домен официального источника, если есть.
        """
        if link_id not in self.links:
            return {"status": "error", "message": f"Ссылка {link_id} не найдена"}
        
        link = self.links[link_id]
        
        # Проверяем, что агент имеет право верифицировать (Кластер 2)
        allowed_agents = [
            "AccuracyAgent", "NavigatorProtocol", "FirstAidAgent",
            "DialogueAgent", "ConservativeAgent", "Modifier",
            "EthicsAgent", "EnglishLanguageAgent", "RussianLanguageAgent"
        ]
        
        if verifying_agent not in allowed_agents:
            return {
                "status": "error", 
                "message": f"Агент {verifying_agent} не имеет права верифицировать ссылки"
            }
        
        # Проверяем домен ссылки
        domain_check = self._check_domain(link["url"])
        
        # Определяем источник верификации
        if verification_source:
            source_domain = self._extract_domain(verification_source)
        else:
            source_domain = domain_check.get("domain", "")
        
        # Проверяем, является ли источник официальным
        source_info = self.official_sources.get(source_domain)
        
        if source_info and source_info["trust"] >= 0.85:
            # Официальный источник — верифицируем
            link["status"] = "verified"
            link["verified_by"] = verifying_agent
            link["verified_at"] = datetime.now().isoformat()
            link["verification_source"] = source_domain
            link["verification_trust"] = source_info["trust"]
            link["history"].append({
                "action": "verified",
                "agent": verifying_agent,
                "timestamp": datetime.now().isoformat(),
                "source": source_domain,
                "trust": source_info["trust"]
            })
            return {
                "status": "ok",
                "link": link,
                "verified": True,
                "trust": source_info["trust"],
                "source": source_domain
            }
        else:
            # Неофициальный источник
            if domain_check.get("is_blocked"):
                # Заблокированный домен — отклоняем сразу
                link["status"] = "rejected"
                link["verified_by"] = verifying_agent
                link["verified_at"] = datetime.now().isoformat()
                link["history"].append({
                    "action": "rejected",
                    "agent": verifying_agent,
                    "timestamp": datetime.now().isoformat(),
                    "reason": "blocked_domain"
                })
                return {
                    "status": "rejected",
                    "link": link,
                    "verified": False,
                    "reason": "Домен заблокирован протоколом"
                }
            else:
                # Неофициальный, но не заблокированный — остаётся непроверенным
                link["history"].append({
                    "action": "verification_failed",
                    "agent": verifying_agent,
                    "timestamp": datetime.now().isoformat(),
                    "reason": "no_official_source"
                })
                return {
                    "status": "unverified",
                    "link": link,
                    "verified": False,
                    "reason": "Нет официального источника для верификации"
                }

    def check_expired(self, link_id: str) -> dict:
        """
        Проверяет, не истёк ли срок действия ссылки.
        Если истёк — отправляет в карантин.
        Если карантин истёк — на арбитраж.
        """
        if link_id not in self.links:
            return {"status": "error", "message": "Ссылка не найдена"}
        
        link = self.links[link_id]
        
        # Проверяем карантин
        if link["status"] == "quarantined":
            if link["quarantine_ends"]:
                quarantine_end = datetime.fromisoformat(link["quarantine_ends"])
                if datetime.now() > quarantine_end:
                    # Карантин истёк — на арбитраж
                    return self._send_to_arbitration(link_id)
                else:
                    return {
                        "status": "quarantined",
                        "link": link,
                        "quarantine_ends": link["quarantine_ends"]
                    }
        
        # Проверяем арбитраж
        if link["status"] == "arbitration":
            return {
                "status": "arbitration",
                "link": link,
                "round": link["arbitration_rounds"],
                "max_rounds": self.max_arbitration_rounds
            }
        
        # Проверяем срок действия
        if link["expires_at"]:
            expires = datetime.fromisoformat(link["expires_at"])
            if datetime.now() > expires:
                # Ссылка просрочена — в карантин
                if link["status"] == "verified":
                    self._send_to_quarantine(link_id)
                    return {
                        "status": "quarantined",
                        "link": link,
                        "requires_reverification": True,
                        "quarantine_ends": link["quarantine_ends"]
                    }
        
        return {"status": "ok", "link": link}

    def _send_to_quarantine(self, link_id: str) -> dict:
        """Отправляет ссылку в карантин."""
        link = self.links[link_id]
        
        link["status"] = "quarantined"
        link["quarantine_started"] = datetime.now().isoformat()
        link["quarantine_ends"] = (datetime.now() + timedelta(days=self.quarantine_duration_days)).isoformat()
        link["history"].append({
            "action": "quarantined",
            "agent": "LinkProtocol",
            "timestamp": datetime.now().isoformat(),
            "duration_days": self.quarantine_duration_days
        })
        
        if link_id not in self.quarantine_queue:
            self.quarantine_queue.append(link_id)
        
        return {
            "status": "quarantined",
            "link": link,
            "quarantine_ends": link["quarantine_ends"]
        }

    def _send_to_arbitration(self, link_id: str) -> dict:
        """Отправляет ссылку на арбитраж после карантина."""
        link = self.links[link_id]
        
        # Увеличиваем счётчик раундов арбитража
        link["arbitration_rounds"] += 1
        link["status"] = "arbitration"
        link["history"].append({
            "action": "arbitration_started",
            "agent": "LinkProtocol",
            "timestamp": datetime.now().isoformat(),
            "round": link["arbitration_rounds"]
        })
        
        if link_id not in self.arbitration_queue:
            self.arbitration_queue.append(link_id)
        
        # Если превышен лимит раундов — разработчику
        if link["arbitration_rounds"] >= self.max_arbitration_rounds:
            return self._send_to_developer(link_id)
        
        # Иначе — пытаемся повторно верифицировать
        reverification_result = self._try_reverify(link_id)
        
        if reverification_result.get("verified"):
            # Успешно верифицирована повторно
            link["status"] = "verified"
            link["verified_at"] = datetime.now().isoformat()
            link["expires_at"] = (datetime.now() + timedelta(days=30)).isoformat()
            link["history"].append({
                "action": "reverified_after_arbitration",
                "agent": reverification_result.get("agent"),
                "timestamp": datetime.now().isoformat(),
                "source": reverification_result.get("source")
            })
            # Убираем из очередей
            self._remove_from_queues(link_id)
            return {
                "status": "verified",
                "link": link,
                "verified": True
            }
        
        return {
            "status": "arbitration",
            "link": link,
            "round": link["arbitration_rounds"],
            "max_rounds": self.max_arbitration_rounds
        }

    def _send_to_developer(self, link_id: str) -> dict:
        """Отправляет ссылку на рассмотрение разработчика."""
        link = self.links[link_id]
        
        link["status"] = "developer_review"
        link["history"].append({
            "action": "sent_to_developer",
            "agent": "LinkProtocol",
            "timestamp": datetime.now().isoformat(),
            "reason": "max_arbitration_rounds_exceeded"
        })
        
        if link_id not in self.developer_queue:
            self.developer_queue.append(link_id)
        
        return {
            "status": "developer_review",
            "link": link,
            "reason": "Ссылка не прошла верификацию после карантина и арбитража. Требуется решение разработчика."
        }

    def _try_reverify(self, link_id: str) -> dict:
        """Пытается повторно верифицировать ссылку."""
        link = self.links[link_id]
        
        # Проверяем домен ещё раз
        domain_check = self._check_domain(link["url"])
        
        if domain_check.get("is_official"):
            source_info = self.official_sources[domain_check["domain"]]
            return {
                "verified": True,
                "agent": "LinkProtocol",
                "source": domain_check["domain"],
                "trust": source_info["trust"]
            }
        
        return {"verified": False}

    def _remove_from_queues(self, link_id: str):
        """Убирает ссылку из всех очередей."""
        if link_id in self.quarantine_queue:
            self.quarantine_queue.remove(link_id)
        if link_id in self.arbitration_queue:
            self.arbitration_queue.remove(link_id)
        if link_id in self.developer_queue:
            self.developer_queue.remove(link_id)

    def developer_decision(self, link_id: str, decision: str, developer_note: str = "") -> dict:
        """
        Разработчик принимает решение по ссылке.
        decision: "approve" / "reject" / "extend_quarantine"
        """
        if link_id not in self.links:
            return {"status": "error", "message": "Ссылка не найдена"}
        
        link = self.links[link_id]
        
        if decision == "approve":
            link["status"] = "verified"
            link["verified_by"] = "Developer"
            link["verified_at"] = datetime.now().isoformat()
            link["expires_at"] = (datetime.now() + timedelta(days=30)).isoformat()
            link["history"].append({
                "action": "approved_by_developer",
                "agent": "Developer",
                "timestamp": datetime.now().isoformat(),
                "note": developer_note
            })
            self._remove_from_queues(link_id)
            return {"status": "verified", "link": link}
        
        elif decision == "reject":
            link["status"] = "rejected"
            link["history"].append({
                "action": "rejected_by_developer",
                "agent": "Developer",
                "timestamp": datetime.now().isoformat(),
                "note": developer_note
            })
            self._remove_from_queues(link_id)
            return {"status": "rejected", "link": link}
        
        elif decision == "extend_quarantine":
            link["status"] = "quarantined"
            link["quarantine_ends"] = (datetime.now() + timedelta(days=self.quarantine_duration_days * 2)).isoformat()
            link["history"].append({
                "action": "quarantine_extended_by_developer",
                "agent": "Developer",
                "timestamp": datetime.now().isoformat(),
                "note": developer_note
            })
            return {"status": "quarantined", "link": link}
        
        return {"status": "error", "message": "Неизвестное решение"}

    def use_link(self, link_id: str, using_agent: str) -> dict:
        """Фиксирует использование ссылки агентом."""
        if link_id not in self.links:
            return {"status": "error", "message": "Ссылка не найдена"}
        
        link = self.links[link_id]
        
        # Проверяем статус
        if link["status"] == "rejected":
            return {"status": "error", "message": "Ссылка отклонена, использование запрещено"}
        
        if link["status"] == "quarantined":
            return {"status": "error", "message": "Ссылка в карантине, использование запрещено"}
        
        if link["status"] == "arbitration":
            return {"status": "error", "message": "Ссылка на арбитраже, использование запрещено"}
        
        if link["status"] == "developer_review":
            return {"status": "error", "message": "Ссылка на рассмотрении разработчика, использование запрещено"}
        
        if link["status"] == "expired":
            return {"status": "error", "message": "Ссылка просрочена, требуется повторная верификация"}
        
        # Фиксируем использование
        link["history"].append({
            "action": "used",
            "agent": using_agent,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "status": "ok",
            "link": link,
            "can_use": link["status"] in ["verified", "unverified"]
        }

    def get_link(self, link_id: str) -> dict:
        """Возвращает данные ссылки."""
        if link_id not in self.links:
            return {"status": "error", "message": "Ссылка не найдена"}
        return {"status": "ok", "link": self.links[link_id]}

    def get_all_links(self) -> list:
        """Возвращает все ссылки."""
        return list(self.links.values())

    def get_statistics(self) -> dict:
        """Статистика по ссылкам."""
        total = len(self.links)
        verified = sum(1 for l in self.links.values() if l["status"] == "verified")
        unverified = sum(1 for l in self.links.values() if l["status"] == "unverified")
        rejected = sum(1 for l in self.links.values() if l["status"] == "rejected")
        expired = sum(1 for l in self.links.values() if l["status"] == "expired")
        quarantined = sum(1 for l in self.links.values() if l["status"] == "quarantined")
        arbitration = sum(1 for l in self.links.values() if l["status"] == "arbitration")
        developer_review = sum(1 for l in self.links.values() if l["status"] == "developer_review")
        
        return {
            "total": total,
            "verified": verified,
            "unverified": unverified,
            "rejected": rejected,
            "expired": expired,
            "quarantined": quarantined,
            "arbitration": arbitration,
            "developer_review": developer_review,
            "quarantine_queue": len(self.quarantine_queue),
            "arbitration_queue": len(self.arbitration_queue),
            "developer_queue": len(self.developer_queue)
        }

    def _check_domain(self, url: str) -> dict:
        """Проверяет домен ссылки."""
        domain = self._extract_domain(url)
        
        is_blocked = any(blocked in domain for blocked in self.blocked_domains)
        is_official = domain in self.official_sources
        
        return {
            "domain": domain,
            "is_blocked": is_blocked,
            "is_official": is_official,
            "official_info": self.official_sources.get(domain)
        }

    def _extract_domain(self, url: str) -> str:
        """Извлекает домен из URL."""
        url = url.lower().replace("https://", "").replace("http://", "")
        url = url.split("/")[0].split("?")[0].split("#")[0]
        return url


# ============================================================
if __name__ == "__main__":
    # Тест LinkProtocol с карантином и арбитражем
    lp = LinkProtocol()
    
    print("=== Тест LinkProtocol с карантином и арбитражем ===\n")
    
    # Тест 1: Создание и верификация официальной ссылки
    print("Тест 1: Официальная ссылка")
    link1 = lp.create_link(
        url="https://pravo.gov.ru/document/12345",
        source_agent="NavigatorProtocol",
        target_agent="AccuracyAgent",
        link_type="legal"
    )
    result1 = lp.verify_link(link1["id"], "AccuracyAgent", "https://pravo.gov.ru")
    print(f"  Статус: {result1['status']}")
    print(f"  Верифицирована: {result1.get('verified')}")
    
    print()
    
    # Тест 2: Просроченная ссылка → карантин
    print("Тест 2: Просроченная ссылка → карантин")
    # Искусственно делаем ссылку просроченной
    link1["expires_at"] = (datetime.now() - timedelta(days=1)).isoformat()
    expired_check = lp.check_expired(link1["id"])
    print(f"  Статус: {expired_check['status']}")
    print(f"  Карантин до: {expired_check.get('quarantine_ends', 'N/A')}")
    
    print()
    
    # Тест 3: Карантин истёк → арбитраж
    print("Тест 3: Карантин истёк → арбитраж")
    # Искусственно завершаем карантин
    link1["quarantine_ends"] = (datetime.now() - timedelta(days=1)).isoformat()
    arbitration_result = lp.check_expired(link1["id"])
    print(f"  Статус: {arbitration_result['status']}")
    print(f"  Раунд арбитража: {arbitration_result.get('round', 'N/A')}")
    
    print()
    
    # Тест 4: Блокированный домен
    print("Тест 4: Заблокированный домен")
    link2 = lp.create_link(
        url="https://reddit.com/r/legaladvice",
        source_agent="NavigatorProtocol",
        target_agent="AccuracyAgent"
    )
    result2 = lp.verify_link(link2["id"], "AccuracyAgent")
    print(f"  Статус: {result2['status']}")
    print(f"  Причина: {result2.get('reason')}")
    
    print()
    
    # Тест 5: Статистика
    print("Тест 5: Статистика")
    stats = lp.get_statistics()
    print(f"  Всего: {stats['total']}")
    print(f"  Верифицировано: {stats['verified']}")
    print(f"  Отклонено: {stats['rejected']}")
    print(f"  В карантине: {stats['quarantined']}")
    print(f"  На арбитраже: {stats['arbitration']}")
    print(f"  У разработчика: {stats['developer_review']}")