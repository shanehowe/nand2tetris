from Parse import Parser
from typing import Optional
import sys


class Assembler:
    _dest: dict = {
        '':'000','M':'001','D':'010','MD':'011',
        'A':'100','AM':'101','AD':'110','AMD':'111'
        }
    _comp: dict = {
        '0':'0101010','1':'0111111','-1':'0111010','D':'0001100',
        'A':'0110000','M':'1110000','!D':'0001101','!A':'0110001',
        '!M':'1110001','-D':'0001111','-A':'0110011','-M':'1110011',
        'D+1':'0011111','A+1':'0110111','M+1':'1110111','D-1':'0001110',
        'A-1':'0110010','M-1':'1110010','D+A':'0000010','D+M':'1000010',
        'D-A':'0010011','D-M':'1010011','A-D':'0000111','M-D':'1000111',
        'D&A':'00000000','D&M':'1000000','D|A':'0010101','D|M':'1010101'
        }
    _jump: dict = {
            '':'000','JGT':'001','JEQ':'010','JGE':'011',
            'JLT':'100','JNE':'101','JLE':'110','JMP':'111'
            }
    def __init__(self, parser: Parser) -> None:
        self.parser = parser
    
    def first_pass(self) -> None:
        while self.parser.has_more_commands():
            self.parser.advance()
            if self.parser.get_command_type() == "L":
                self.parser.symbol()
    
    def second_pass(self) -> None:
        outfile_name = f"{self.parser.file_name}.hack"
        outfile = open(outfile_name, "w")
        self.parser.restart()

        while self.parser.has_more_commands():
            self.parser.advance()
            if self.parser.current_command.startswith("("):
                continue

            if self.parser.get_command_type() == "A":
                symbol = self.parser.symbol()
                binary = str(bin(symbol)[2:])
                line = binary.zfill(16)
            elif self.parser.get_command_type() == "C":
                comp = self.bin_comp()
                dest = self.bin_dest()
                jump = self.bin_jump()
                line = f"111{comp}{dest}{jump}"

            outfile.write(line + "\n")
        
        outfile.close()
        self.parser.file.close()
    
    def assemble(self) -> None:
        self.first_pass()
        self.second_pass()

    
    def bin_dest(self) -> Optional[str]:
        dest_key = self.parser.dest()
        return self._dest.get(dest_key)
    
    def bin_comp(self) -> Optional[str]:
        comp_key = self.parser.comp()
        return self._comp.get(comp_key)
    
    def bin_jump(self) -> Optional[str]:
        jump_key = self.parser.jump()
        return self._jump.get(jump_key)
    

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 Assembler.py filename.asm")
    
    parser = Parser(sys.argv[1])
    assembler = Assembler(parser)
    assembler.assemble()


if __name__ == "__main__":
    main()
