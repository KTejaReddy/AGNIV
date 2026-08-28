from .models import AdaptivePolicies, ConfidenceLevel

class PoliciesManager:
    def __init__(self):
        self.policies = AdaptivePolicies()

    def get_policies(self) -> AdaptivePolicies:
        return self.policies

    def update_policies(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self.policies, key):
                setattr(self.policies, key, value)

policies_manager = PoliciesManager()
