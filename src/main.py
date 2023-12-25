import random
import time
from pod_state import PodState

from queue_state import QueueState
from state_modifier_enum import StateModifierEnum


class MachineState:
    def __init__(self, pod_state: PodState, queue_state: QueueState):
        self.pod_state: PodState = pod_state
        self.queue_state: QueueState = queue_state

        self.current_tick = 0

    def __iter__(self):
        return iter((self.pod_state, self.queue_state, self.current_tick))

    def print_state(self):
        (pod_state, queue_state, current_tick) = self
        (cpu, memory, total_pods) = pod_state
        (messages_queued, publish_rate, ack_rate) = queue_state

        print(f"Tick: {current_tick} PODS: {total_pods} CPU: {cpu:.2f} MEM: {memory:.2f} Q_COUNT: {messages_queued} Q_PUB: {publish_rate:.2f} Q_ACK: {ack_rate:.2f}")

    def next_state(self):
        self.current_tick += 1

        random_modifier = self.get_random_modifier_using_weights()
        print("Random Modifier: " + random_modifier.name)

        has_queue_state_changed = self.queue_state.next_state(
            random_modifier, self.pod_state)
        if has_queue_state_changed:
            self.pod_state.next_state(random_modifier)

    def get_random_modifier_using_weights(self) -> StateModifierEnum:
        balanced_odds: int = 6
        low_input_odds: int = 2
        high_input_odds: int = 1
        low_output_odds: int = 1 + self.pod_state.total_pods
        high_output_odds: int = 1

        weighted_numbers = [StateModifierEnum.BALANCED] * balanced_odds + \
            [StateModifierEnum.LOW_INPUT] * low_input_odds + \
            [StateModifierEnum.HIGH_INPUT] * high_input_odds + \
            [StateModifierEnum.LOW_OUTPUT] * low_output_odds + \
            [StateModifierEnum.HIGH_OUTPUT] * high_output_odds

        result = random.choice(weighted_numbers)

        return StateModifierEnum(result)


def main():
    pod_state: PodState = PodState(cpu=100, memory=200, total_pods=3)
    queue_state: QueueState = QueueState(
        messages_queued=100, ack_rate=10, publish_rate=1)

    machine_state: MachineState = MachineState(pod_state, queue_state)

    while True:
        machine_state.print_state()
        time.sleep(.2)
        machine_state.next_state()


if __name__ == '__main__':
    main()
