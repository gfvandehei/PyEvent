from typing import Callable, Any

class EventListener(object):
    def __init__(self, expression: str, action: Callable[[str, Any], None]):
        self.expression = expression
        self.action = action

        self.expression_components = self.expression.split(".")

    def reg_event(self, event_path: str, data: Any):
        self.action(event_path, data)