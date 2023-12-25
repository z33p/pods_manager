import random

from state_modifier_enum import StateModifierEnum


class PodState:
    def __init__(self, cpu: float, memory: float, total_pods: int):
        self.cpu: str = cpu
        self.memory: str = memory
        self.total_pods: int = total_pods

    def __iter__(self):
        return iter((self.cpu, self.memory, self.total_pods))

    def next_state(self, modifier_enum: StateModifierEnum):
        next_state_switcher = {
            StateModifierEnum.HIGH_INPUT: lambda: self.handle_input_modifier(self.get_high_rate_modifier),
            StateModifierEnum.LOW_INPUT: lambda: self.handle_input_modifier(self.get_low_rate_modifier),
            StateModifierEnum.HIGH_OUTPUT: lambda: self.handle_output_modifier(self.get_high_rate_modifier),
            StateModifierEnum.LOW_OUTPUT: lambda: self.handle_output_modifier(self.get_low_rate_modifier),
        }

        fn_modify_state = next_state_switcher.get(modifier_enum)

        if fn_modify_state is None:
            return

        return fn_modify_state()

    def get_high_rate_modifier(self):
        random_cpu_modifier = random.randint(5, 10) / 100
        random_memory_modifier = random.randint(5, 10) / 100
        return random_cpu_modifier, random_memory_modifier

    def get_low_rate_modifier(self):
        random_cpu_modifier = random.randint(1, 5) / 100
        random_memory_modifier = random.randint(1, 5) / 100
        return random_cpu_modifier, random_memory_modifier

    def handle_input_modifier(self, get_rate_modifier):
        random_cpu_modifier, random_memory_modifier = get_rate_modifier()

        self.cpu = self.cpu * (1 + random_cpu_modifier)
        self.memory = self.memory * (1 + random_memory_modifier)

    def handle_output_modifier(self, get_rate_modifier):
        random_cpu_modifier, random_memory_modifier = get_rate_modifier()

        self.cpu = self.cpu * (1 - random_cpu_modifier)
        self.memory = self.memory * (1 - random_memory_modifier)

