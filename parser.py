from lark import Lark, LarkError
import os, re 

#EBNF Grammar Rules for Lark
grammar = r"""
    program: [clause_list] query
    
    clause_list: clause+
    
    clause: predicate "." 
          | predicate ":-" predicate_list "."
    
    query: "?-" predicate_list "."
    
    predicate_list: predicate ("," predicate)*
    
    predicate: atom ("(" term_list ")")*
    
    term_list: term ("," term)*
    
    term: atom 
        | variable 
        | structure 
        | numeral
    
    structure: atom "(" term_list ")"
    
    atom: small_atom 
        | "'" string "'"
    
    small_atom: LOWERCASE_CHAR [character_list]
    
    variable: UPPERCASE_CHAR [character_list]
    
    character_list: alphanumeric+
    
    alphanumeric: LOWERCASE_CHAR 
                | UPPERCASE_CHAR 
                | DIGIT 
    
    LOWERCASE_CHAR: "a".."z"
    
    UPPERCASE_CHAR: "A".."Z" | "_"
    
    numeral: DIGIT+
    
    DIGIT: "0".."9"
    
    string: character+
    
    character: alphanumeric 
             | SPECIAL
    
    SPECIAL: "+" | "-" | "*" | "/" | "\\" | "^" | "~" | ":" | "." | "?" | " " | "\#" | "$" | "&"
     
    %import common.WS
    %ignore WS
"""

#This function is used to extract the line number of the error to ensure
#that the correct line is outputted in the error message even when moving
#to the next line after encountering an error
def extractLineNumber(errorMessage):
    #Using regular expressions to extract the line number from the error message
    match = re.search(r"at line (\d+)", errorMessage)
    if match:
        lineNumber = int(match.group(1))
        return lineNumber
    else:
        return None


#Analyzing Syntax using Lark Tree: This function creates the tree based on the txt  
#file provided and outputs either that the syntax is correct or the errors present
def parsingFile(filepath, fileCount):
    with open(filepath, 'r') as file:
        
        output = f"\n-----File {fileCount}:\n"
        
        text = file.read()
        
        #Count variables to keep track of the number of errors & current line
        errorCount = 0
        lineCount = 0
        
        #Boolean to determine output message contents
        errorPresent = False

        #Parsing while there is still text
        while text:
            try:
                larkTree = parser.parse(text)
                #If no errors, print and break to parse next file
                if not errorPresent: output += "Syntax is Correct\n\n"
                break
            
            except LarkError as e:
                errorPresent = True
                
                # Extract the error message string
                errorMessage = str(e)
                
                # Extract the line number
                lineCount += extractLineNumber(errorMessage)
                
                # Replace the line number with accurate lineCount
                if lineCount is not None:
                    modifiedMessage = re.sub(r"at line (\d+)", f"at line {lineCount}", errorMessage)
                else:
                    modifiedMessage = errorMessage
                
                #Prints the error message - will include the error number, which
                #token is causing the error, and what the parser is expecting 
                #instead so that the user can fix the error
                errorCount += 1
                output += f"\nError {errorCount} - {modifiedMessage}\n"
                
                #To continue parsing after encountering an unexpected token, move
                #to the next line ("\n") and start parsing instead to ensure that the parser
                #can continue to generate valid parse trees
                pos = e.pos_in_stream
                while pos < len(text) and text[pos] != '.':
                    pos += 1
                while pos < len(text) and text[pos] == '.':
                    pos += 1
                text = text[pos:]
    
    
    if errorPresent: output += f"Total Errors in File {fileCount}: {errorCount} error{'s' if errorCount > 1 else ''}\n\n"
    return output


#File Handling: This function reads in the files from the same directory as the
#python file and keeps reading in files and passing them to the parsingFile function
#until there are no files left. Finally, the function writes to an output file
def fileHandling(directory):
    
    #Empty string intialized - will append the output of each file to this
    output = "CMP321 Parser Project\n"

    #Used to determine next file name - assuming the files are in sequence
    fileCounter = 1

    #Filename intialization
    filename = f"{fileCounter}.txt"
    filepath = os.path.join(directory, filename)

    #Looping through available files in directory 
    while os.path.exists(filepath):
        output += parsingFile(filepath, fileCounter)
        fileCounter += 1
        filename = f"{fileCounter}.txt"
        filepath = os.path.join(directory, filename)

    with open("output.txt", 'w') as outputFile:
        outputFile.write(output)
        
       
#Parser Created
parser = Lark(grammar, start='program')

#Start parsing based on directory (current = ".")
fileHandling(".") 












