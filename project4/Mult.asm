// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Usage: Put a number in ram0 and number in ram1
//        Product of ram0 & ram1 is stored in ram3
    @2
    M=0 // Ensure product is set to 0
    @1 
    D=M

    @i 
    M=D // Initialize i for loop

    @0 
    D=M
    @END
    D;JEQ // if num being multiplied is 0 jump to end



(LOOP)
    @i
    D=M 
    @END 
    D;JEQ // if i == 0 goto END
    @0
    D=M
    @2
    M=D+M // Repeatedly add number in ram0 to ram2
    @i
    M=M-1 // i -= 1
    @LOOP
    0;JMP

(END)
    @END // Infinite loop
    0;JMP



      