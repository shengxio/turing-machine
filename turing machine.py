import time

class TuringMachine:
    def __init__(self, input_string):
        self.tape = list(input_string) + ['B']  # Add blank symbol at end
        self.head_position = 0
        self.current_state = 'q0'
        self.step = 1
        
        # Define transition table
        self.transition_table = {
            'q0': {
                '0': lambda: self._move_right('q0'),
                '1': lambda: self._move_right('q1'),
                'B': lambda: self._accept()
            },
            'q1': {
                '0': lambda: self._move_right('q1'),
                '1': lambda: self._move_right('q0'),
                'B': lambda: self._reject()
            }
        }
        
    def get_tape_display(self):
        tape_display = self.tape.copy()
        tape_display[self.head_position] = f"[{tape_display[self.head_position]}]"
        return ''.join(tape_display)
    
    def _move_right(self, next_state):
        """Move the head right and transition to next state"""
        print(f"Action: Move to {next_state}, move right")
        self.tape[self.head_position] = self.tape[self.head_position]  # Keep the same symbol
        self.head_position += 1
        self.current_state = next_state
        return True
    
    def _accept(self):
        """Accept the input"""
        print("Action: Reached end of input, accepting")
        self.current_state = 'q_accept'
        return False
    
    def _reject(self):
        """Reject the input"""
        print("Action: Reached end of input, rejecting")
        self.current_state = 'q_reject'
        return False
    
    def process_symbol(self):
        current_symbol = self.tape[self.head_position]
        print(f"Reading symbol: {current_symbol}")
        
        # Get the action from transition table and execute it
        action = self.transition_table[self.current_state][current_symbol]
        return action()
    
    def _initialize(self):
        """Initialize the simulation"""
        print(f"Input: {''.join(self.tape[:-1])}")  # Don't show the blank symbol
        print("Starting simulation...")
        print("Press Enter to continue each step...")
        input()
    
    def _process_step(self):
        """Process a single step of the simulation"""
        print(f"\nStep {self.step}:")
        print(f"State: {self.current_state}")
        print(f"Tape: {self.get_tape_display()}")
        
        if not self.process_symbol():
            return False
            
        print("\nPress Enter to continue...")
        input()
        self.step += 1
        return True
    
    def _finalize(self):
        """Handle the end of simulation"""
        print(f"\nFinal state: {self.current_state}")
        if self.current_state == 'q_accept':
            print("Result: ACCEPT - The input has an even number of 1's")
        else:
            print("Result: REJECT - The input has an odd number of 1's")
    
    def run(self):
        """Run the Turing machine simulation"""
        self._initialize()
        
        while self._process_step():
            pass
            
        self._finalize()

def main():
    print("Testing Turing Machine for Even Number of 1's")
    print("=" * 50)
    
    # Test with even number of 1's
    tm1 = TuringMachine("10101")
    tm1.run()
    
    print("\n" + "=" * 50)
    
    # # Test with odd number of 1's
    # tm2 = TuringMachine("101")
    # tm2.run()

if __name__ == "__main__":
    main()
