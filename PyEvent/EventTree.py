from typing import List, MutableSet, Dict
from PyEvent.EventListener import EventListener

class EventTreeNode(object):

    def __init__(self, component: str, level: int, parent: "EventTreeNode"):
        self.component = component
        self.level = level
        self.parent = parent
        self.children: Dict[str, EventTreeNode] = {}
        self.listeners: MutableSet[EventListener] = set()
        self._star_listeners: MutableSet[EventListener] = set()

    def create_children_for_path(self, trunc_path: List[str]):
        if len(trunc_path) == 0:
            return
        
        if trunc_path[0] == "*":
            raise Exception("Cant create real paths with *")
        elif trunc_path[0] in self.children:
            new_child = self.children[trunc_path[0]]
        else:
            new_child = EventTreeNode(trunc_path[0], level=self.level+1, parent=self)
            self.children[trunc_path[0]] = new_child
        new_child.create_children_for_path(trunc_path[1:])
        for i in self._star_listeners:
            new_child.add_listener(i, i.expression_components[self.level+2:])

    def add_listener(self, listener: EventListener, trunc_path: List[str]):
        if len(trunc_path) == 0:
            self.listeners.add(listener)
        elif trunc_path[0] == "*":
            self._star_listeners.add(listener)
            for child in self.children:
                self.children[child].add_listener(listener, trunc_path[1:])
        else:
            # check the path exists
            if not (trunc_path[0] in self.children):
                # create said path
                self.create_children_for_path([trunc_path[0]])
            self.children[trunc_path[0]].add_listener(listener, trunc_path[1:])
    
    def gather_path(self):
        current_node = self
        path_reversed = []
        while current_node != None:
            path_reversed.append(current_node.parent)
            current_node = current_node.parent

    def _event(self, trunc_path: List[str], full_path: str, data):
        # make sure path exists
        if len(trunc_path) == 0:
            #print(self.parent.parent.listeners)
            for listener in self.listeners:
                listener.reg_event(full_path, data)
        else:
            self.create_children_for_path(trunc_path)
            child = self.children[trunc_path[0]]
            child._event(trunc_path[1:], full_path, data)
    
    def event(self, full_path: str, data):
        self._event(full_path.split(".")[1:], full_path, data)
    
    def print_paths(self):
        print(" "*self.level+self.component)
        for child in self.children:
            self.children[child].print_paths()


root = EventTreeNode("Overlord", 0, None)
#root.create_children_for_path(["action", "1", "events", "file"])
#root.create_children_for_path(["action","2", "events", "file"])
root.print_paths()

listener = EventListener("Overlord.action.*.events.*", lambda e, d: print(e, d))
root.add_listener(listener, listener.expression_components[1:])

event_path = "Overlord.action.1.events.data"
root.event(event_path, None)

event_path = "Overlord.action.1.events.file"
root.event(event_path, None)