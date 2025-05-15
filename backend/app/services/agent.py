# backend/app/services/agent.py

class MockAgent:
    """
    Agente de prueba que ignora el historial y siempre responde "hello".
    Más adelante reemplazable por un cliente OpenAI real.
    """
    def get_response(self, messages: list[dict]) -> str:
        return "hello"