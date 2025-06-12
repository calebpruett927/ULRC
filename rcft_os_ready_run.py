import time
from rcft_runtime_metrics import RCFTMetrics

class SymbolicAgent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.metrics = RCFTMetrics()

    def act(self, temperature):
        self.metrics.update(temperature)

class RCFTOS:
    def __init__(self, num_agents):
        self.agents = [SymbolicAgent(f"A{i}") for i in range(num_agents)]
        self.external_temperature = 25.0

    def update_environment(self, temp):
        self.external_temperature = temp

    def run_loop(self):
        while True:
            for agent in self.agents:
                agent.act(self.external_temperature)
            time.sleep(1)