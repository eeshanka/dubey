
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

1. Implement Pass 1 of Two Pass Assembler.

Prog.

def parse_line(line):
    parts = line.strip().split()
    
    label = None
    opcode = None
    operand = None

    if len(parts) == 3:
        label, opcode, operand = parts
    elif len(parts) == 2:
        opcode, operand = parts
    else:
        opcode = parts[0]

    return label, opcode, operand

def pass_1(source_code):
    location_counter = 0
    symbol_table = {}
    intermediate_code = []
    
    for line in source_code:
        label, opcode, operand = parse_line(line)
        
        if label:
            if label not in symbol_table:
                symbol_table[label] = location_counter
 
        intermediate_code.append(f"{opcode} {operand} {location_counter}")
        
        location_counter += 1

    return symbol_table, intermediate_code

source_code = [
    "START",   
    "LOAD A",    
    "ADD B",    
    "STORE C",   
    "END"       
]

symbol_table, intermediate_code = pass_1(source_code)

print("Symbol Table:")
for label, address in symbol_table.items():
    print(f"{label}: {address}")

print("\nIntermediate Code:")
for code in intermediate_code:
    print(code)
    
    
Output:

Symbol Table:
START: 0

Intermediate Code:
LOAD A 0
ADD B 1
STORE C 2
END 3


- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  



2. WAP to define a MACRO without argument, expand MACRO calls.


program: 

#include <stdio.h>

// Defining a MACRO without arguments
#define PRINT_HELLO() printf("Hello, World!\n");

int main() {
    // Calling the macro
    PRINT_HELLO();  // This will expand to printf("Hello, World!\n");

    return 0;
}


Output:

Hello, World!
    
    
Runnng op:

cd Desktop
gcc -o macro_example macro_example.c
./macro_example

     
     - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
     
3. Write a program to compute FOLLOW for a CFG.

Program:

# Function to check if a character exists in a list
def in_list(lst, char):
    return char in lst

# Function to compute FOLLOW set for a given grammar
def compute_follow(productions, non_terminals):
    follow = {nt: set() for nt in non_terminals}  # Initialize FOLLOW sets
    follow[non_terminals[0]].add('$')  # Start symbol follows $ (end of input)

    changed = True
    while changed:
        changed = False
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                for i in range(len(rhs)):
                    if rhs[i] in non_terminals:  # If current symbol is a non-terminal
                        # If the next symbol exists in the production
                        if i + 1 < len(rhs):
                            next_symbol = rhs[i + 1]
                            # If the next symbol is a terminal, add it to FOLLOW
                            if next_symbol not in non_terminals:
                                if not in_list(follow[rhs[i]], next_symbol):
                                    follow[rhs[i]].add(next_symbol)
                                    changed = True
                            # If the next symbol is a non-terminal, add its FOLLOW set
                            else:
                                for symbol in follow[next_symbol]:
                                    if not in_list(follow[rhs[i]], symbol):
                                        follow[rhs[i]].add(symbol)
                                        changed = True
                        # If the current symbol is at the end of the production
                        elif rhs[i] in non_terminals:
                            for symbol in follow[lhs]:
                                if symbol not in follow[rhs[i]]:
                                    follow[rhs[i]].add(symbol)
                                    changed = True

    return follow

# Function to print FOLLOW sets
def print_follow(follow):
    for non_terminal in follow:
        print(f"FOLLOW({non_terminal}) = {{", end="")
        print(", ".join(follow[non_terminal]), end="")
        print(" }")

# Input the grammar
def main():
    num_rules = int(input("Enter number of rules: "))
    productions = {}
    non_terminals = set()
    
    print("Enter the grammar rules (e.g., A->BC):")
    for _ in range(num_rules):
        rule = input("Rule: ")
        lhs, rhs = rule.split("->")
        non_terminals.add(lhs)
        rhs_list = rhs.split("|")
        productions[lhs] = rhs_list

    # Compute FOLLOW sets
    follow = compute_follow(productions, non_terminals)
    
    # Print the FOLLOW sets
    print_follow(follow)

if __name__ == "__main__":
    main()


Output:

     
     Enter number of rules: 4
Enter the grammar rules (e.g., A->BC):
Rule: S->AB
Rule: A->a
Rule: B->$
Rule: C->AB


FOLLOW(S) = { $, a }
FOLLOW(A) = { a }
FOLLOW(B) = { a }
FOLLOW(C) = { $, a }


- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

4. Write a program to compute FIRST for a CFG.


Program:

# Function to check if a character exists in a list
def in_list(lst, char):
    return char in lst

# Function to compute FIRST set for a given grammar
def compute_first(productions, non_terminals):
    first = {nt: set() for nt in non_terminals}  # Initialize FIRST sets

    changed = True
    while changed:
        changed = False
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                # Handle epsilon case (if the production can derive epsilon)
                if rhs == '$':  
                    if not in_list(first[lhs], '$'):
                        first[lhs].add('$')
                        changed = True
                else:
                    for symbol in rhs:
                        # If the symbol is a terminal, add it to the FIRST set
                        if symbol not in non_terminals:
                            if not in_list(first[lhs], symbol):
                                first[lhs].add(symbol)
                                changed = True
                            break
                        # If the symbol is a non-terminal, add the FIRST of that non-terminal
                        else:
                            for symbol in first[symbol]:
                                if symbol != '$' and not in_list(first[lhs], symbol):
                                    first[lhs].add(symbol)
                                    changed = True
                            # If the symbol can produce epsilon, continue with the next symbol in the production
                            if '$' not in first[symbol]:
                                break
    return first

# Function to print FIRST sets
def print_first(first):
    for non_terminal in first:
        print(f"FIRST({non_terminal}) = {{", end="")
        print(", ".join(first[non_terminal]), end="")
        print(" }")

# Input the grammar
def main():
    num_rules = int(input("Enter number of rules: "))
    productions = {}
    non_terminals = set()
    
    print("Enter the grammar rules (e.g., A->BC):")
    for _ in range(num_rules):
        rule = input("Rule: ")
        lhs, rhs = rule.split("->")
        non_terminals.add(lhs)
        rhs_list = rhs.split("|")
        productions[lhs] = rhs_list

    # Compute FIRST sets
    first = compute_first(productions, non_terminals)
    
    # Print the FIRST sets
    print_first(first)

if __name__ == "__main__":
    main()


Outpu:

Enter number of rules: 4
Enter the grammar rules (e.g., A->BC):
Rule: S->AB|C
Rule: A->a
Rule: B->$
Rule: C->d


FIRST(S) = { a, d }
FIRST(A) = { a }
FIRST(B) = { $ }
FIRST(C) = { d }



- - - - - - - - - - - -   -- - - -- - - - - - - - - - - - - -  - - - - - - -


5. Write a program to count number of characters, words, sentences, lines, tabs, numbers and blank spaces present in input using LEX.


lex prog...//

/*Lex Program to count numbers of lines, words, spaces and characters 

in a given statement*/
%{
#include<stdio.h>
int sc=0,wc=0,lc=0,cc=0;
%}

%%
[\n] { lc++; cc+=yyleng;}
[  \t] { sc++; cc+=yyleng;}
[^\t\n ]+ { wc++;  cc+=yyleng;}
%%

int main(int argc ,char* argv[ ])
{
	printf("Enter the input:\n");
	yylex();
	printf("The number of lines=%d\n",lc);
	printf("The number of spaces=%d\n",sc);
	printf("The number of words=%d\n",wc);
	printf("The number of characters are=%d\n",cc);
}

int yywrap( )
{
	return 1;
}


Output:/// (use this step to execute..)


lex demo.l

gcc lex.yy.c

./a.out

Enter the input: kuch bhi input dedo ghihdgvhj

input dene k baad.. press enter and ctrl+d)

ye l op agya

The number of lines=3

The number of spaces=6

The number of words=9

The number of characters are=70