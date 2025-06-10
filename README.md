# Turing Machine Simulator

This repository contains a simple Python implementation of a Turing Machine simulator that checks whether a binary string contains an even number of 1's. The simulation is interactive and demonstrates the step-by-step operation of a Turing Machine.

## Features
- Simulates a Turing Machine for binary strings.
- Accepts if the input has an even number of 1's, rejects otherwise.
- Step-by-step interactive simulation with clear state and tape visualization.

## File Structure
- `turing machine.py`: Main Python script containing the Turing Machine simulator and example runs.
- `requirements.txt`: (Currently empty) No external dependencies required.
- `.gitignore`: Standard Python ignores.

## Requirements
- Python 3.6 or higher (for f-string support).

## Usage
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```
2. **Run the simulator:**
   ```bash
   python "turing machine.py"
   ```
3. **Follow the prompts:**
   - The script will run two example simulations: one with an even number of 1's and one with an odd number.
   - Press Enter to step through each transition.

## How It Works
- The Turing Machine reads the input tape from left to right.
- It switches between two states (`q0` and `q1`) depending on the symbol read (`0` or `1`).
- When the end of the input (blank symbol `B`) is reached:
  - If in state `q0`, the input is **accepted** (even number of 1's).
  - If in state `q1`, the input is **rejected** (odd number of 1's).

## Example Output
```
Testing Turing Machine for Even Number of 1's
==================================================
Input: 1010
Starting simulation...
Press Enter to continue each step...

Step 1:
State: q0
Tape: [1]010B
Reading symbol: 1
Action: Move to q1, move right
...
Final state: q_accept
Result: ACCEPT - The input has an even number of 1's
```

## License
This project is provided for educational purposes. 