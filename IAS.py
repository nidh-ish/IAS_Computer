from collections import OrderedDict
import re
import linecache

def num_to_bin(x):
    y = bin(int(x))
    if(y[0] == '0'):
        initial = y[2:]
        extra = 12 - len(initial)
        final = '0'*extra  + initial
    else:
        initial = y[3:]
        extra = 11 - len(initial)
        final = '1' + '0'*extra + initial
    return final
    
def int_to_bin(x):
    y = bin(int(x))
    if(y[0] == '-'):
        initial = y[3:]
        extra = 39 - len(initial)
        final = '1' + '0'*extra + initial
    else:
        initial = y[2:]
        extra = 40 - len(initial)
        final = '0'*extra + initial
    return final
    
def bin_to_int(binary):
    binary = str(binary)
    if(binary[0] == '0'):
        binary = int(binary)
        binary1 = binary 
        decimal, i, n = 0, 0, 0
        while(binary != 0): 
            dec = binary % 10
            decimal = decimal + dec * pow(2, i) 
            binary = binary//10
            i += 1
        return decimal
    elif(binary[0] == '1'):
        binary = binary[1:]
        binary = int(binary)
        binary1 = binary
        decimal, i, n = 0, 0, 0
        while(binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary//10
            i += 1
        return -decimal   

def opcode(oprtn, number):
    if(oprtn == 'ADD' and number[0] == 'M'):
        return '00000101'

    elif(oprtn == 'STOR' and (',' not in number)):
        return '00100001'

    elif(oprtn == 'LOAD' and number[0:2] == 'M('):
        return '00000001'

    elif(oprtn == 'LOAD' and number[0:2] == '-M'):
        return '00000010'

    elif(oprtn == 'LOAD' and number[0] == '|'):
        return '00000011'

    elif(oprtn == 'LOAD' and number[0:2] == '-|'):
        return '00000100'

    elif(oprtn == 'LOAD' and number == 'MQ'):
        return '00001010'

    elif(oprtn == 'LOAD' and number[:5] == 'MQ,M('):
        return '00001001'

    elif(oprtn == 'ADD' and number[0] == '|'):
        return '00000111'

    elif(oprtn == 'SUB' and number[0] == 'M'):
        return '00000110'

    elif(oprtn == 'SUB' and number[0] == '|'):
        return '00001000'

    elif(oprtn == 'DIV'):
        return '00001100'

    elif(oprtn == 'LSH'):
        return '00010100'

    elif(oprtn == 'RSH'):
        return '00010101'

    elif(oprtn == 'JUMP' and number[-6:-1] == ',0:19'):
        return '00001101'

    elif(oprtn == 'JUMP' and number[-7:-1] == ',20:39'):
        return '00001110'

    elif(oprtn == 'JUMP+' and number[-6:-1] == ',0:19'):
        return '00001111'

    elif(oprtn == 'JUMP+' and number[-7:-1] == ',20:39'):
        return '00010000'

    elif(oprtn == 'MUL'):
        return '00001011'  

    elif(oprtn == 'STOR' and number[-6:-1] == ',8:19'):
        return '00010010'

    elif(oprtn == 'STOR' and number[-7:-1] == ',28:39'):
        return '00010011'
        
    elif(oprtn == 'HALT'):
        return '11111111'

PC = '000000000001'

pattern = "[0-9]+"

output = open("machinecode.txt", "w+")

while True:

    PC = bin_to_int(PC)

    line = linecache.getline('assemblylang.txt', PC).rstrip("\n")
    if not line:
        break
    line = line.split(" ")
    temp = PC
    PC = num_to_bin(PC)

    if(len(line) == 4):
        left_opcode = opcode(line[0], line[1])
        
        num_left = re.findall(pattern, line[1])

        if(not num_left):
            left_address = '000000000000'

        else:
            left_address = num_to_bin(int(num_left[0]))
        
        left_instruction = left_opcode + left_address
        
        right_opcode = opcode(line[2], line[3])
        
        num_right = re.findall(pattern, line[3])

        if(not num_right):
            right_address = '000000000000'

        else:
            right_address = num_to_bin(int(num_right[0]))

        right_instruction = right_opcode + right_address
        
        instruction = left_instruction + right_instruction
        
        output.write(instruction)
        output.write("\n")
 
        PC = bin_to_int(PC)
        PC = PC + 1
        PC = num_to_bin(PC)

    elif(len(line) == 2):
        right_opcode = opcode(line[0], line[1])
       
        num_right = re.findall(pattern, line[1])

        if(not num_right):
            right_address = '000000000000'

        else:
            right_address = num_to_bin(num_right[0])

        right_instruction = right_opcode + right_address

        instruction = '00000000000000000000' + right_instruction
        output.write(instruction)
        output.write("\n")
        
        PC = bin_to_int(PC)
        PC = PC + 1
        PC = num_to_bin(PC)

    elif(len(line) == 1):
        right_opcode = opcode(line[0], 'nothing')
        right_address = '000000000000'

        right_instruction = right_opcode + right_address

        instruction = '00000000000000000000' + right_instruction
        output.write(instruction)
        output.write("\n")
         
        PC = bin_to_int(PC)
        PC = PC + 1
        PC = num_to_bin(PC)

    elif(len(line)  == 3):
        if(line[2] == 'LSH' or line[2] == 'RSH' or line[2] == 'HALT'):
            left_opcode = opcode(line[0], line[1])
        
            num_left = re.findall(pattern, line[1])

            if(not num_left):
                left_address = '000000000000'

            else:
                left_address = num_to_bin(int(num_left[0]))
        
            left_instruction = left_opcode + left_address
            
            right_opcode = opcode(line[2], 'nothing')
            right_address = '000000000000'
    
            right_instruction = right_opcode + right_address

            instruction = left_instruction + right_instruction
            output.write(instruction)
            output.write("\n")
                
            PC = bin_to_int(PC)
            PC = PC + 1
            PC = num_to_bin(PC)
 
        elif(line[0] == 'RSH' or line[0] == 'LSH' or line[0] == 'HALT'):
            left_opcode = opcode(line[0], 'nothing')
            left_address = '000000000000'
    
            left_instruction = left_opcode + left_address
            
            right_opcode = opcode(line[1], line[2])
        
            num_right = re.findall(pattern, line[2])

            if(not num_right):
                right_address = '000000000000'

            else:
                right_address = num_to_bin(int(num_right[0]))
        
            right_instruction = right_opcode + right_address
            
            instruction = left_instruction + right_instruction
            output.write(instruction)
            output.write("\n")
                
            PC = bin_to_int(PC)
            PC = PC + 1
            PC = num_to_bin(PC)
            
output.close()   

         
memory = OrderedDict()

def sorted_memory(mem):
    d = dict()
    final_memory = sorted(mem.items(), key=lambda x : x[0])
    for i in final_memory:
        d[i[0]] = i[1]
    return d
    
memory = {'000001100100' : '0000000000000000000000000000000000000011', '000001100101' : '1000000000000000000000000000000000000101'}
memory = sorted_memory(memory)

print("-----------------------------------------------------------------------------------------------INITIAL-----------------------------------------------------------------------------------------------------")

print()
print()

for i, j in memory.items():
    print(i, ":", j)
print()
print()

print("------------------------------------------------------------------------------------------------FINAL------------------------------------------------------------------------------------------------------")

print()
print()

class INST_SET:
    def inst_LOAD(self, mar, AC):
        MBR = memory[mar]
        AC = MBR
        return AC

    def inst_LOAD_NEG(self, mar, AC):
        MBR = memory[mar]
        if(MBR[0] == '0'):
            AC = '1' + MBR[1:]
        else:
            AC = '0' + MBR[1:]
        return AC

    def inst_LOAD_MOD(self, mar, AC):
        MBR = memory[mar]
        if(MBR[0] == '0'):
            MBR = MBR
        elif(MBR[0] == '1'):
            MBR = '0' + MBR[1:]
        AC = MBR
        return AC

    def inst_LOAD_NEG_MOD(self, mar, AC):
        MBR = memory[mar]
        if(MBR[0] == '0'):
            MBR = MBR
        elif(MBR[0] == '1'):
            MBR = '0' + MBR[1:] 
        AC = '1' + MBR[1:]
        return AC

    def inst_ADD(self, mar, AC):
        MBR = bin_to_int(memory[mar])
        AC = bin_to_int(AC)
        AC = AC + MBR
        return int_to_bin(AC)

    def inst_STOR(self, mem, mar):
        MBR = AC
        mem[mar] = MBR
        mem = sorted_memory(mem)
 
    def inst_LOAD_MQ(self, MQ, AC):
        AC = MQ
        return AC

    def inst_LOAD_MQ_MX(self, mar, MQ):
        MQ = memory[mar]
        return MQ
    
    def inst_ADD_MOD(self, mar, AC):
        MBR = memory[mar]
        if(MBR[0] == '0'):
            MBR = MBR
        elif(MBR[0] == '1'):
            MBR = '0' + MBR[1:]
        MBR = bin_to_int(MBR)
        AC = bin_to_int(AC)
        AC = AC + MBR
        return int_to_bin(AC)

    def inst_SUB(self, mar, AC):
        MBR = bin_to_int(memory[mar])
        AC = bin_to_int(AC)
        AC = AC - MBR
        return int_to_bin(AC)

    def inst_SUB_MOD(self, mar, AC):
        MBR = memory[mar]
        if(MBR[0] == '0'):
            MBR = MBR
        elif(MBR[0] == '1'):
            MBR = '0' + MBR[1:]
        AC = bin_to_int(AC)
        MBR = bin_to_int(MBR)
        AC = AC - MBR
        return int_to_bin(AC)

    def inst_DIV(self, mar, AC, MQ):
        MBR = bin_to_int(memory[mar])
        MQ = bin_to_int(MQ)
        AC = bin_to_int(AC)
        MQ = AC / MBR
        AC = AC % MBR
        AC = int_to_bin(AC)
        MQ = int_to_bin(MQ)
        return AC, MQ

    def inst_LSH(self, AC):
        AC = bin_to_int(AC)
        AC = AC * 2
        return int_to_bin(AC)

    def inst_RSH(self, AC):
        AC = bin_to_int(AC)
        AC = AC / 2
        return int_to_bin(AC)

    def inst_JUMP_LEFT(self, PC, X):
        PC = bin_to_int(PC)
        X = bin_to_int(X)
        PC = X - 1
        return num_to_bin(PC)

    def inst_JUMP_RIGHT(self, PC, X):
        PC = bin_to_int(PC)
        X = bin_to_int(X)
        PC = X - 1
        return num_to_bin(PC)

    def inst_JUMP_COND_LEFT(self, PC, X, AC):
        AC = bin_to_int(AC)
        PC = bin_to_int(PC)
        X = bin_to_int(X)
        if (int(AC) >= 0):
            PC = X - 1
        return num_to_bin(PC)

    def inst_JUMP_COND_RIGHT(self, PC, X, AC):
        AC = bin_to_int(AC)
        PC = bin_to_int(PC)
        X = bin_to_int(X)
        if(int(AC) >= 0):
           PC = X - 1
        return num_to_bin(PC)

    def inst_MUL(self, mar, MQ, AC):
        product = bin_to_int(memory[mar])
        MQ = bin_to_int(MQ)
        mul = product * MQ
        mul = int_to_bin(mul)
        AC = mul[:20]
        MQ = mul[20:]
        return AC, MQ

    def inst_STOR_LEFT(self, mar, AC, memory):
        final = str(memory[mar])[0:8] + str(AC)[28:] + str(memory[mar])[20:40]
        return final

    def inst_STOR_RIGHT(self, mar, AC, memory):
        final = str(memory[mar])[:28] + str(AC)[28:]
        return final

inst = INST_SET()

PC = '000000000001'
AC = int()
MQ = '0000000000000000000000000000000000001010'
right = True

while True:

    MAR = PC
    temp = bin_to_int(PC)
    
    PC = bin_to_int(PC)
    line = linecache.getline('machinecode.txt', PC).rstrip("\n")
    PC = num_to_bin(PC)
    if not line:
        break
    
    memory[MAR] = line
    MBR = memory[MAR]
    
    left_instruction = MBR[0:20]
    right_instruction = MBR[20:40]

    if(left_instruction  != '00000000000000000000'):

        IBR = MBR[20:40]    
        IR  = MBR[:8]
        MAR = MBR[8:20]

    else:
        
        IR = MBR[20:28]
        MAR = MBR[28:40]
       
    if(right and True):

        if(IR == '00000001'):
            AC = inst.inst_LOAD(MAR, AC)   
            
        elif(IR == '11111111'):
            break;

        elif(IR == '00000101'):
            AC = inst.inst_ADD(MAR, AC)
            
        elif(IR == '00100001'):
            inst.inst_STOR(memory, MAR)

        elif(IR == '00000111'):
            AC = inst.inst_ADD_MOD(MAR, AC)

        elif(IR == '00000010'):
            AC = inst.inst_LOAD_NEG(MAR, AC)
        
        elif(IR == '00000011'):
            AC = inst.inst_LOAD_MOD(MAR, AC)

        elif(IR == '00000100'): 
            AC = inst.inst_LOAD_NEG_MOD(MAR, AC)

        elif(IR == '00001010'):
            AC = inst.inst_LOAD_MQ(MQ, AC)

        elif(IR == '00001001'):
            MQ = inst.inst_LOAD_MQ_MX(MAR, MQ)

        elif(IR == '00000111'):
            AC = inst.inst_ADD_MOD(MAR, AC)

        elif(IR == '00000110'):
            AC = inst.inst_SUB(MAR, AC)

        elif(IR == '00001000'):
            AC = inst.inst_SUB_MOD(MAR, AC)

        elif(IR == '00001100'):
            AC, MQ = inst.inst_DIV(MAR, AC, MQ)

        elif(IR == '00001011'):
            AC, MQ = inst.inst_MUL(MAR, MQ, AC)

        elif(IR == '00010100'):
            AC = inst.inst_LSH(AC)
  
        elif(IR == '00010101'):
            AC = inst.inst_RSH(AC)

        elif(IR == '00001101'):
            PC = inst.inst_JUMP_LEFT(PC, MAR)

        elif(IR == '00010011'):
            memory[MAR] = inst.inst_STOR_RIGHT(MAR, AC, memory)

        elif(IR == '00010010'):
            memory[MAR] = inst.inst_STOR_LEFT(MAR, AC, memory)
    
        elif(IR == '00001110'):
            PC = inst.inst_JUMP_RIGHT(PC, MAR)
            right = False
            
        elif(IR == '00001111'):
            PC = inst.inst_JUMP_COND_LEFT(PC, MAR, AC)

        elif(IR == '00010000'):
            PC = inst.inst_JUMP_COND_RIGHT(PC, MAR, AC)
            if(bin_to_int(PC) - temp >= 1):
                right = False
            else:
                right = True
            
    if(right or True):
        right = True     

        if(left_instruction != '00000000000000000000'):
            IR = IBR[0:8]
            MAR = IBR[8:20]
          
        if(IR == '00000001'):
            AC = inst.inst_LOAD(MAR, AC)   
            
        elif(IR == '11111111'):
            break;

        elif(IR == '00000101'):
            AC = inst.inst_ADD(MAR, AC)

        elif(IR == '00100001'):
            inst.inst_STOR(memory, MAR)

        elif(IR == '00000111'):
            AC = inst.inst_ADD_MOD(MAR, AC)

        elif(IR == '00000010'):
            AC = inst.inst_LOAD_NEG(MAR, AC)
        
        elif(IR == '00000011'):
            AC = inst.inst_LOAD_MOD(MAR, AC)

        elif(IR == '00000100'): 
            AC = inst.inst_LOAD_NEG_MOD(MAR, AC)

        elif(IR == '00001010'):
            AC = inst.inst_LOAD_MQ(MQ, AC)

        elif(IR == '00001001'):
            MQ = inst.inst_LOAD_MQ_MX(MAR, MQ)

        elif(IR == '00000111'):
            AC = inst.inst_ADD_MOD(MAR, AC)

        elif(IR == '00000110'):
            AC = inst.inst_SUB(MAR, AC)

        elif(IR == '00001000'):
            AC = inst.inst_SUB_MOD(MAR, AC)
 
        elif(IR == '00001100'):
            AC, MQ = inst.inst_DIV(MAR, AC, MQ)

        elif(IR == '00001011'):
            AC, MQ = inst.inst_MUL(MAR, MQ, AC)
 
        elif(IR == '00010100'):
            AC = inst.inst_LSH(AC)
    
        elif(IR == '00010101'):
            AC = inst.inst_RSH(AC)

        elif(IR == '00010011'):
            memory[MAR] = inst.inst_STOR_RIGHT(MAR, AC, memory)

        elif(IR == '00010010'):
            memory[MAR] = inst.inst_STOR_LEFT(MAR, AC, memory)
 
        elif(IR == '00001101'):
            PC = inst.inst_JUMP_LEFT(PC, MAR)
  
        elif(IR == '00001110'):
            PC = inst.inst_JUMP_RIGHT(PC, MAR)
            right = False

        elif(IR == '00001111'):
            PC = inst.inst_JUMP_COND_LEFT(PC, MAR, AC)
               
        elif(IR == '00010000'):
            PC = inst.inst_JUMP_COND_RIGHT(PC, MAR, AC)
            if(bin_to_int(PC) - temp >= 1):
                right = False
            else:
                right = True
 
    PC = bin_to_int(PC)
    PC = PC + 1
    PC = num_to_bin(PC)
       
memory = sorted_memory(memory)
for i, j in memory.items():
    print(i, ":", j)
print()
print()
