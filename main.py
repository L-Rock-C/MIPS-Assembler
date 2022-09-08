# Read file
file = open('example3.asm', 'r')
lines = file.readlines()


# Variables
labels = list()
labelsIndex = list()

instructions = list()
instructionsIndex = list()


def getLines():
    address = 0
    for line in lines:
        if line.find(":") > 0:
            labelStr = ""
            instrStr = ""
            endLabel = False
            # Set the value and index of labels and instructions
            for letter in line.strip():
                if not endLabel:
                    if letter == ":":
                        labels.append(labelStr)
                        labelsIndex.append(address)
                        endLabel = True
                    else:
                        labelStr += letter
                else:
                    instrStr = line.strip(labelStr)
                    labelStr += ":"

            instructions.append(instrStr.strip())
            instructionsIndex.append(address)
        else:
            instructions.append(line.strip())
            instructionsIndex.append(address)
        address += 1


def runAssembler():
    i = 0
    binCode = ""
    while i < len(instructionsIndex):
        for tag in instructions[i].split():
            if tag == "sll":
                opcode = "000000"
                binCode += opcode
            if tag == "$s0,":
                rs = "01001"
                binCode += rs
            if tag == "$s1,":
                rt = "01010"
                binCode += rt
            if tag == "$s2,":
                rd = "01000"
                binCode += rd
            if tag == int:
                sa = bin(int(tag))
                binCode += sa
            func = "100000"
            binCode += func

        i += 1
    print(binCode)

getLines()
runAssembler()
