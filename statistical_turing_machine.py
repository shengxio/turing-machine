import numpy as np
from typing import Dict, List, Tuple, Callable
from collections import defaultdict
import time

class StatisticalState:
    def __init__(self, state: str, probability: float = 1.0, history: List[str] = None):
        self.state = state
        self.probability = probability
        self.history = history or []
        self.transition_count = defaultdict(int)
        self.input_count = defaultdict(int)

class StatisticalTuringMachine:
    def __init__(self, input_list: List[float], transition_func: Callable[[float, str], Dict[str, float]]):
        self.input_list = input_list
        self.current_index = 0
        self.step = 1
        
        # Store the transition function
        self.transition_func = transition_func
        
        # Initialize statistical state
        self.current_state = StatisticalState('q0')
        
        # Statistical analysis parameters
        self.confidence_threshold = 0.8
        self.learning_rate = 0.1
    
    def _get_current_input(self) -> float:
        """Get the current input value"""
        if self.current_index < len(self.input_list):
            return self.input_list[self.current_index]
        return None
    
    def _update_statistics(self, current_input: float, next_state: str):
        """Update statistical information based on transitions"""
        self.current_state.transition_count[next_state] += 1
        self.current_state.input_count[current_input] += 1
        
        # Update transition probabilities based on observed patterns
        total_transitions = sum(self.current_state.transition_count.values())
        if total_transitions > 0:
            # Get current transition probabilities from the function
            current_transitions = self.transition_func(current_input, self.current_state.state)
            for state in current_transitions:
                observed_prob = self.current_state.transition_count[state] / total_transitions
                current_prob = current_transitions[state]
                # Update probability with learning rate
                current_transitions[state] = (
                    (1 - self.learning_rate) * current_prob + 
                    self.learning_rate * observed_prob
                )
    
    def _get_confidence(self) -> float:
        """Calculate confidence in current state based on history"""
        if not self.current_state.history:
            return 0.5  # Initial confidence
            
        # Calculate pattern consistency
        pattern_length = min(3, len(self.current_state.history))
        recent_pattern = self.current_state.history[-pattern_length:]
        pattern_count = self.current_state.history.count(tuple(recent_pattern))
        
        return pattern_count / len(self.current_state.history)
    
    def process_input(self) -> bool:
        current_input = self._get_current_input()
        if current_input is None:
            return False
            
        print(f"Processing input: {current_input}")
        
        # Get transition probabilities from the function
        transitions = self.transition_func(current_input, self.current_state.state)
        
        # Choose next state based on probabilities
        states = list(transitions.keys())
        probs = list(transitions.values())
        next_state = np.random.choice(states, p=probs)
        
        # Update statistics
        self._update_statistics(current_input, next_state)
        
        # Update state history
        self.current_state.history.append(next_state)
        
        # Move to next state
        self.current_state = StatisticalState(
            next_state,
            probability=transitions[next_state],
            history=self.current_state.history
        )
        
        # Move to next input
        self.current_index += 1
        
        # Check if we should continue
        return not next_state in ['q_accept', 'q_reject']
    
    def _initialize(self):
        """Initialize the statistical simulation"""
        print(f"Input list: {self.input_list}")
        print("Starting statistical simulation...")
        print("Initial state:", self._get_state_display())
        print("Press Enter to continue each step...")
        input()
    
    def _get_state_display(self) -> str:
        """Get a string representation of the current statistical state"""
        confidence = self._get_confidence()
        stats = (
            f"State: {self.current_state.state} "
            f"(Confidence: {confidence:.2f})\n"
            f"Transition counts: {dict(self.current_state.transition_count)}\n"
            f"Input counts: {dict(self.current_state.input_count)}"
        )
        return stats
    
    def _process_step(self) -> bool:
        """Process a single step of the simulation"""
        print(f"\nStep {self.step}:")
        print(self._get_state_display())
        print(f"Current input index: {self.current_index}")
        
        if not self.process_input():
            return False
            
        print("\nPress Enter to continue...")
        input()
        self.step += 1
        return True
    
    def _finalize(self):
        """Handle the end of simulation"""
        confidence = self._get_confidence()
        print("\nStatistical Analysis:")
        print(f"Final state: {self.current_state.state}")
        print(f"Confidence in result: {confidence:.2f}")
        print("\nTransition Statistics:")
        for state, counts in self.current_state.transition_count.items():
            print(f"  {state}: {counts} times")
        
        if self.current_state.state == 'q_accept':
            print("\nResult: ACCEPT")
            print(f"Confidence level: {confidence:.2f}")
        else:
            print("\nResult: REJECT")
            print(f"Confidence level: {confidence:.2f}")
    
    def run(self):
        """Run the statistical Turing machine simulation"""
        self._initialize()
        
        while self._process_step():
            pass
            
        self._finalize()

def example_transition_func(input_value: float, current_state: str) -> Dict[str, float]:
    """Example transition function that maps input values to state probabilities"""
    # If we've reached the end of processing
    if input_value is None:
        if current_state == 'q0':
            return {'q_accept': 1.0}
        else:
            return {'q_reject': 1.0}
            
    # Normal state transitions
    if current_state == 'q0':
        if input_value > 0.5:
            return {'q1': 0.7, 'q0': 0.3}
        else:
            return {'q0': 0.7, 'q1': 0.3}
    elif current_state == 'q1':
        if input_value > 0.5:
            return {'q0': 0.7, 'q1': 0.3}
        else:
            return {'q1': 0.7, 'q0': 0.3}
    # For any other state, reject
    return {'q_reject': 1.0}

def main():
    print("Testing Statistical Turing Machine with Input List")
    print("=" * 50)
    
    # Test with a list of input values
    input_list = [0.7, 0.3, 0.8, 0.2]
    stm = StatisticalTuringMachine(input_list, example_transition_func)
    stm.run()

if __name__ == "__main__":
    main() 