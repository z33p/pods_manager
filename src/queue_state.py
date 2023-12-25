
import random
from pod_state import PodState

from state_modifier_enum import StateModifierEnum


def scale_to_range(value, min_range, max_range):
    """ Escalona um valor para o intervalo especificado. """
    return max(min_range, min(max_range, int(value)))


def generate_normal_random(mean: int, stddev: int, offset: int, limit: int):
    # Gerar um número da distribuição normal
    normal_random = random.gauss(mean, stddev)
    # Escalonar o número para o intervalo de offset a limit
    return scale_to_range(normal_random, offset, limit)


class QueueState:
    def __init__(self, messages_queued: int, publish_rate: float, ack_rate: float):
        self.messages_queued = messages_queued
        self.publish_rate = publish_rate
        self.ack_rate = ack_rate

    def __iter__(self):
        return iter((self.messages_queued, self.publish_rate, self.ack_rate))

    def calculate_throughput(self) -> float:
        throughput = self.publish_rate - self.ack_rate
        return throughput

    def next_state(self, modifier_enum: StateModifierEnum, pod_state: PodState) -> bool:
        messages_throughput = self.calculate_throughput()

        has_current_state_changed = False

        if messages_throughput > 0 or self.messages_queued > 0:
            messages_queued = int(
                self.messages_queued + messages_throughput)

            self.messages_queued = messages_queued if messages_queued > 0 else 0
            has_current_state_changed = True

        next_state_switcher = {
            StateModifierEnum.HIGH_INPUT: lambda: self.handle_input_modifier(is_high=True),
            StateModifierEnum.LOW_INPUT: lambda: self.handle_input_modifier(is_high=False),
            StateModifierEnum.HIGH_OUTPUT: lambda: self.handle_output_modifier(pod_state, is_high=True),
            StateModifierEnum.LOW_OUTPUT: lambda: self.handle_output_modifier(pod_state, is_high=False),
        }

        fn_modify_state = next_state_switcher.get(modifier_enum)

        if fn_modify_state is not None:
            fn_modify_state()

        return has_current_state_changed

    def handle_input_modifier(self, is_high: bool):
        if is_high:
            self.publish_rate = generate_normal_random(
                mean=35, stddev=15, offset=20, limit=100)
        else:
            self.publish_rate = generate_normal_random(
                mean=5, stddev=10, offset=0, limit=20)

    def handle_output_modifier(self, pod_state: PodState, is_high: bool):
        pod_ack_in_state = round(
            pod_state.total_pods * 2 + (pod_state.cpu / 100))

        if is_high:
            mean = pod_ack_in_state + 30
            limit = pod_ack_in_state + 100
            self.ack_rate = generate_normal_random(
                mean=mean, stddev=10, offset=20, limit=limit)
        else:
            mean = pod_ack_in_state + 5
            limit = pod_ack_in_state + 20
            self.ack_rate = generate_normal_random(
                mean=mean, stddev=10, offset=0, limit=limit)
