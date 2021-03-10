IAS Computer

Program contents : 

In the beginning there are three functions that are used to convert integer to 12 bits binary, integer to 40 bits binary, and binary to integer. Then, there is a function named Opcode. That gives us the  opcode for the assembly instructions. The program contains a class of instruction, in which all the 21 instructions are defined. 

How the program runs : 

The program is basically divided into two halfs. The first half of the program acts as an assembler and coverts the assembly language instructions to the correspondig 40 bits instructions. The input is taken from a file named "assemblylang" that contains assembly language instructions  and the output is stored in a file named "machinecode.txt". Now, in the second half, input is read from the file "machinecode.txt" and it performs the given instructions. PC is initialized to 1 in the beginning of the program. MQ is initialised to 10. Data content is stored in the memory in thr beginning of the program. Here, memory is in the form of a dictionary. Then finally, the sorted memory is printed.

How to run the program : 

Put up assembly language instructions in the file "assemblylang.txt".(Be careful with spaces, only one space is enough. No extra spaces to be given in between). Sample input is already given inside the file. Now we call the program. (python3 IAS.py). 

Output : 

As soon as we call the program, it reads input from the file "assemblylang.txt" converts it to machine language and stored it in a new file "machinecode.txt". If this file was already there then, the contents will be overwritten or else a new file will be created. The initial and final memory is printed.
