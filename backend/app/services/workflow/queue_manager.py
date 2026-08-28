import asyncio
from typing import List, Optional
from .models import WorkflowInstance, WorkflowState

class WorkflowQueue:
    def __init__(self):
        self.queue: List[WorkflowInstance] = []
        self.active_workflows: List[WorkflowInstance] = []

    def enqueue(self, instance: WorkflowInstance):
        instance.state = WorkflowState.QUEUED
        self.queue.append(instance)

    def dequeue(self) -> Optional[WorkflowInstance]:
        if self.queue:
            return self.queue.pop(0)
        return None

    def add_active(self, instance: WorkflowInstance):
        self.active_workflows.append(instance)
        
    def remove_active(self, instance_id: str):
        self.active_workflows = [w for w in self.active_workflows if w.instance_id != instance_id]

    def get_all(self):
        return {
            "queued": self.queue,
            "active": self.active_workflows
        }
        
    def get_instance(self, instance_id: str) -> Optional[WorkflowInstance]:
        for w in self.active_workflows:
            if w.instance_id == instance_id:
                return w
        for w in self.queue:
            if w.instance_id == instance_id:
                return w
        return None

workflow_queue = WorkflowQueue()
