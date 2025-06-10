import time

def simulate_turing_machine(input_string):
    # Initialize
    tape = list(input_string) + ['B']  # Add blank symbol at end
    head_position = 0
    current_state = 'q0'
    step = 1
    
    print(f"Input: {input_string}")
    print("Starting simulation...")
    print("Press Enter to continue each step...")
    input()
    
    while True:
        # Print current configuration
        tape_display = tape.copy()
        tape_display[head_position] = f"[{tape_display[head_position]}]"
        print(f"\nStep {step}:")
        print(f"State: {current_state}")
        print(f"Tape: {''.join(tape_display)}")
        
        # Get current symbol
        current_symbol = tape[head_position]
        print(f"Reading symbol: {current_symbol}")
        
        # Process based on current state and symbol
        if current_state == 'q0':
            if current_symbol == '0':
                print("Action: Stay in q0, move right")
                tape[head_position] = '0'
                head_position += 1
                current_state = 'q0'
            elif current_symbol == '1':
                print("Action: Move to q1, move right")
                tape[head_position] = '1'
                head_position += 1
                current_state = 'q1'
            elif current_symbol == 'B':
                print("Action: Reached end of input, accepting")
                current_state = 'q_accept'
                break
        elif current_state == 'q1':
            if current_symbol == '0':
                print("Action: Stay in q1, move right")
                tape[head_position] = '0'
                head_position += 1
                current_state = 'q1'
            elif current_symbol == '1':
                print("Action: Move to q0, move right")
                tape[head_position] = '1'
                head_position += 1
                current_state = 'q0'
            elif current_symbol == 'B':
                print("Action: Reached end of input, rejecting")
                current_state = 'q_reject'
                break
        
        step += 1
        print("\nPress Enter to continue...")
        input()
    
    print(f"\nFinal state: {current_state}")
    if current_state == 'q_accept':
        print("Result: ACCEPT - The input has an even number of 1's")
    else:
        print("Result: REJECT - The input has an odd number of 1's")

# Test the machine with some example inputs
print("Testing Turing Machine for Even Number of 1's")
print("=" * 50)
simulate_turing_machine("1010")  # Even number of 1's
print("\n" + "=" * 50)
simulate_turing_machine("101")   # Odd number of 1's
