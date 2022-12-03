
// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(SET)
    @0
    D=A 
    @i 
    M=D // i= 0
    @LISTEN
    0;JMP 

(LISTEN)
    @KBD
    D=M 
    @WHITE 
    D;JEQ //if kbd > 0 goto white
    @BLACK 
    0;JMP  // else goto black

(BLACK)
    @1
    M=-1 //set ram0 to write black pixel
    @LOOP
    0;JMP 

(WHITE)
    @1
    M=0 // set ram 0 to write white pixel
    @LOOP 
    0;JMP 

(LOOP)
    @i 
    D=M 
    @8192 // number of pixels needed to colour
    D=D-A
    @SET 
    D;JGT // if i - last pixel > 0 go back to set 

    @SCREEN 
    D=A 
    @i 
    D=D+M //address to change pixel (i+SCREEN)

    @temp
    M=D // store address in temp variable
    @1
    D=M //D=-1 or D=0 depending on KBD 
    @temp 
    A=M 
    M=D //change pixel in address
    @i 
    M=M+1 // i++ 
    @LISTEN
    0;JMP



    
    



