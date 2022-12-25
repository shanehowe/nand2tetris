from SymbolTable import SymbolTable
from typing import Optional, TextIO

class Parser:
    nxt_addr: int = 16 # Next available address for variable
    line_num: int = 0 # To track labels to jump to

    def __init__(self, file: str) -> None:
        self.file: TextIO = open(file)
        self.current_command: str = self.file.readline().lstrip(" ")
        self.file_name = file.split(".")[0]
    
    def has_more_commands(self) -> bool:
        """
        Peeks the next line in the file
        """
        pos = self.file.tell()
        line = self.file.readline()
        self.file.seek(pos)
        return line != ""
    
    def get_command_type(self) -> str:
        if self.current_command.startswith("@"):
            return "A"
        elif self.current_command.startswith("("):
            return "L"
        else:
            return "C"
    
    def advance(self) -> str:
        if self.current_command.startswith("//"):
            while self.current_command.startswith("//") or self.current_command == "\n":
                self.current_command = self.file.readline().lstrip(" ") 
        else:
            self.current_command = self.file.readline().lstrip(" ")
        
        if self.get_command_type() != "L":
            self.line_num += 1
        
        self.current_command = self.normalize(self.current_command)
        return self.current_command
    
    def symbol(self) -> Optional[int]:
        """
        To be called only when get_command_type returns A or L
        Will really only be used on the first pass,
        after first pass we can just use SymbolTable to look up
        """
        # TODO: Clean this up this method, perhaps first pass method then second pass...
        symbol = self.current_command

        if "@" in symbol:
            if SymbolTable.contains(symbol):
                return SymbolTable.get_symbol(symbol)
            symbol = symbol.replace("@", "")
            # If the rest of the symbol is digit then the programmer is asking
            # for that memory address, no need to allocate ram address 
            if symbol.isdigit():
                SymbolTable.update_symbols(symbol=symbol, address=int(symbol))
                return SymbolTable.get_symbol(symbol)
        else:
            # Clean up label for updating table
            symbol = symbol.replace("(", "")
            symbol = symbol.replace(")", "")
        if self.get_command_type() == "L":
            SymbolTable.update_symbols(symbol=symbol, address=self.line_num)
        elif not SymbolTable.contains(symbol):
            SymbolTable.update_symbols(symbol=symbol, address=self.nxt_addr)
            self.nxt_addr += 1
        
        return SymbolTable.get_symbol(symbol)
    
    def dest(self) -> str:
        """
        Parses the command and returns the dest string
        to be turned to binary in Assembler class
        """
        try: 
            destination, _ = self.current_command.split("=")
            return destination
        except ValueError:
            return ""
    
    def comp(self) -> str:
        """
        Parses the command and returns the comp string
        to be turned to binary in Assembler class
        """
        try:
            _, _comp = self.current_command.split("=")
        except ValueError:
            _comp, _ = self.current_command.split(";")
        
        return _comp
    
    def jump(self) -> str:
        """
        Parses the command and returns the jump string
        to be turned to binary in Assembler class
        """
        try:
            _, _jump = self.current_command.split(";")
        except ValueError:
            _jump = ""
        return _jump
    
    def normalize(self, command: str) -> str:
        """
        Removes inline comments
        """
        return command.split()[0]
    
    def restart(self) -> None:
        self.file.seek(0)
        self.current_command = self.file.readline().lstrip(" ")
