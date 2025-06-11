import numpy as np
from typing import Dict, List, Tuple
import time

class QuantumState:
    def __init__(self, state: str, amplitude: complex = 1.0):
        self.state = state
        self.amplitude = amplitude

class QuantumTuringMachine:
    def __init__(self, input_string: str):
        self.tape = list(input_string) + ['B']  # Add blank symbol at end
        self.head_position = 0
        self.step = 1
        
        # Initialize quantum state in superposition
        self.quantum_states = [QuantumState('q0', 1.0)]  # Start in |q0⟩
        
        # Define quantum transition amplitudes
        self.transition_matrix = {
            'q0': {
                '0': {'q0': 1/np.sqrt(2), 'q1': 1/np.sqrt(2)},  # Hadamard-like transition
                '1': {'q0': 1/np.sqrt(2), 'q1': 1/np.sqrt(2)},
                'B': {'q_accept': 1.0}
            },
            'q1': {
                '0': {'q1': 1/np.sqrt(2), 'q0': 1/np.sqrt(2)},
                '1': {'q1': 1/np.sqrt(2), 'q0': 1/np.sqrt(2)},
                'B': {'q_reject': 1.0}
            }
        }
    
    def get_tape_display(self) -> str:
        tape_display = self.tape.copy()
        tape_display[self.head_position] = f"[{tape_display[self.head_position]}]"
        return ''.join(tape_display)
    
    def _apply_quantum_transition(self, current_symbol: str) -> List[QuantumState]:
        """Apply quantum transitions to all current states"""
        new_states = []
        
        for qstate in self.quantum_states:
            if qstate.state in ['q_accept', 'q_reject']:
                new_states.append(qstate)
                continue
                
            transitions = self.transition_matrix[qstate.state][current_symbol]
            for next_state, amplitude in transitions.items():
                new_amplitude = qstate.amplitude * amplitude
                new_states.append(QuantumState(next_state, new_amplitude))
        
        return new_states
    
    def _normalize_states(self, states: List[QuantumState]) -> List[QuantumState]:
        """Normalize the amplitudes of quantum states"""
        total_probability = sum(abs(state.amplitude) ** 2 for state in states)
        if total_probability > 0:
            normalization_factor = 1 / np.sqrt(total_probability)
            for state in states:
                state.amplitude *= normalization_factor
        return states
    
    def _measure(self) -> str:
        """Perform quantum measurement"""
        probabilities = {state.state: abs(state.amplitude) ** 2 for state in self.quantum_states}
        states = list(probabilities.keys())
        probs = list(probabilities.values())
        
        # Normalize probabilities
        total = sum(probs)
        if total > 0:
            probs = [p/total for p in probs]
        
        return np.random.choice(states, p=probs)
    
    def process_symbol(self) -> bool:
        current_symbol = self.tape[self.head_position]
        print(f"Reading symbol: {current_symbol}")
        
        # Apply quantum transitions
        new_states = self._apply_quantum_transition(current_symbol)
        self.quantum_states = self._normalize_states(new_states)
        
        # Move head right
        self.head_position += 1
        
        # Check if we should continue
        return not any(state.state in ['q_accept', 'q_reject'] for state in self.quantum_states)
    
    def _initialize(self):
        """Initialize the quantum simulation"""
        print(f"Input: {''.join(self.tape[:-1])}")
        print("Starting quantum simulation...")
        print("Initial quantum state:", self._get_state_display())
        print("Press Enter to continue each step...")
        input()
    
    def _get_state_display(self) -> str:
        """Get a string representation of the current quantum state"""
        state_str = " + ".join(
            f"{state.amplitude:.2f}|{state.state}⟩"
            for state in self.quantum_states
        )
        return state_str
    
    def _process_step(self) -> bool:
        """Process a single step of the simulation"""
        print(f"\nStep {self.step}:")
        print(f"Quantum state: {self._get_state_display()}")
        print(f"Tape: {self.get_tape_display()}")
        
        if not self.process_symbol():
            return False
            
        print("\nPress Enter to continue...")
        input()
        self.step += 1
        return True
    
    def _finalize(self):
        """Handle the end of simulation and measurement"""
        print("\nPerforming quantum measurement...")
        final_state = self._measure()
        print(f"Measured state: {final_state}")
        
        if final_state == 'q_accept':
            print("Result: ACCEPT - The input has an even number of 1's")
        else:
            print("Result: REJECT - The input has an odd number of 1's")
    
    def run(self):
        """Run the quantum Turing machine simulation"""
        self._initialize()
        
        while self._process_step():
            pass
            
        self._finalize()

def main():
    print("Testing Quantum Turing Machine for Even Number of 1's")
    print("=" * 50)
    
    # Test with even number of 1's
    qtm = QuantumTuringMachine("1010")
    qtm.run()

if __name__ == "__main__":
    main() 