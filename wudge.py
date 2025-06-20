#!/usr/bin/env python3
"""
Wudge Programming Language Interpreter
A file-based interpreter for the Wudge esolang
Enhanced version with stackable replace patterns
"""

import re
import sys
import os

class WudgeInterpreter:
    def __init__(self):
        self.variables = {}
        self.lines = []
        self.current_line = 0
        
    def parse_set_command(self, line):
        """Parse 'set a {b}' command"""
        match = re.match(r'set\s+(\w+)\s+\{([^}]*)\}', line)
        if match:
            var_name = match.group(1)
            value = match.group(2)
            self.variables[var_name] = value
            return True
        return False
    
    def parse_ask_command(self, line):
        """Parse 'ask a b' command"""
        match = re.match(r'ask\s+(\w+)\s+(\w+)', line)
        if match:
            prompt_var = match.group(1)
            input_var = match.group(2)
            prompt = self.variables.get(prompt_var, "")
            user_input = input(prompt)
            self.variables[input_var] = user_input
            return True
        return False
    
    def parse_jump_command(self, line):
        """Parse 'jump 10' command"""
        match = re.match(r'jump\s+(\d+)', line)
        if match:
            line_num = int(match.group(1))
            # Convert to 0-based indexing and subtract 1 because main loop will add 1
            target_line = line_num - 1
            
            # Bounds checking
            if target_line < 0:
                print(f"Error: Cannot jump to line {line_num} (before start of program)")
                return False
            elif target_line >= len(self.lines):
                print(f"Error: Cannot jump to line {line_num} (beyond end of program)")
                return False
            
            self.current_line = target_line - 1  # Subtract 1 because main loop will add 1
            return True
        return False

    def parse_print_command(self, line):
        """Parse 'print a' command"""
        match = re.match(r'print\s+(\w+)', line)
        if match:
            var_name = match.group(1)
            value = self.variables.get(var_name, "")
            print(value)
            return True
        return False
    
    def parse_replace_command(self, line):
        """Parse 'replace a [b/c],[d/e],... to f' command with stackable patterns"""
        # Match the basic structure: replace source_var ... to target_var
        match = re.match(r'replace\s+(\w+)\s+(.*?)\s+to\s+(\w+)', line)
        if not match:
            return False
        
        source_var = match.group(1)
        patterns_part = match.group(2)
        target_var = match.group(3)
        
        # Extract all [pattern/replacement] pairs
        pattern_matches = re.findall(r'\[([^/]*)/([^\]]*)\]', patterns_part)
        
        if not pattern_matches:
            return False
        
        source_value = self.variables.get(source_var, "")
        result = source_value
        
        # Apply all replacements in order
        for pattern, replacement in pattern_matches:
            result = result.replace(pattern, replacement)
        
        # Set the target variable to the result (replace, don't append)
        self.variables[target_var] = result
        
        return True
    
    def parse_if_command(self, line):
        """Parse 'if a found [b] do 10' command"""
        match = re.match(r'if\s+(\w+)\s+found\s+\[([^\]]+)\]\s+do\s+(\d+)', line)
        if match:
            var_name = match.group(1)
            pattern = match.group(2)
            lines_to_execute = int(match.group(3))
            
            value = self.variables.get(var_name, "")
            
            if pattern in value:
                # Execute next N lines normally - just continue
                return True
            else:
                # Skip next N lines
                self.current_line += lines_to_execute
                return True
        return False
    
    def execute_line(self, line):
        """Execute a single line of Wudge code"""
        line = line.strip()
        
        if not line or line.startswith('#'):  # Empty line or comment
            return True
        
        # Try each command type
        if self.parse_set_command(line):
            return True
        elif self.parse_ask_command(line):
            return True
        elif self.parse_jump_command(line):
            return True
        elif self.parse_print_command(line):
            return True
        elif self.parse_replace_command(line):
            return True
        else:
            # Check if command
            if_result = self.parse_if_command(line)
            if if_result is not False:
                return if_result
        
        print(f"Error: Unknown command: {line}")
        return False
    
    def run_file(self, filename):
        """Run Wudge code from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return False
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
        
        self.lines = code.strip().split('\n')
        self.current_line = 0
        self.variables = {}
        
        print(f"Executing Wudge program from '{filename}'...")
        print("-" * 40)
        
        while self.current_line < len(self.lines):
            line = self.lines[self.current_line]
            result = self.execute_line(line)
            
            if result is False:
                break
            
            self.current_line += 1
        
        print("-" * 40)
        print(f"Program '{filename}' finished.")
        
        return True

def main():
    interpreter = WudgeInterpreter()
    
    print("Wudge Programming Language Interpreter")
    print("=====================================")
    
    try:
        filename = input("Enter a file with valid Wudge code: ").strip()
        
        if not filename:
            print("No filename provided. Exiting.")
            sys.exit(1)
        
        # Check if file exists
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' does not exist.")
            sys.exit(1)
        
        # Execute the file
        success = interpreter.run_file(filename)
        
        if success:
            sys.exit(0)  # Normal exit
        else:
            sys.exit(1)  # Error exit
    
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
