import PySimpleGUI as gui

def mainWindow():
    gui.theme("DarkTeal2")
    layout = [[gui.Text("Arquivo")],
              [gui.Input(), gui.FileBrowse("Procurar", key='fileSelect')],
              [gui.Text("Conteúdo do arquivo")],
              [gui.Output(key='fileReading', size=(100, 10))],
              [gui.Text("Código binário")],
              [gui.Output(key='result', size=(100, 10))],
              [gui.Button("Gerar código binário")],
              [gui.Button("Salvar arquivo .bin")],
              [gui.Button("Sair")]
              ]

    window = gui.Window("Assembler MIPS", layout, size=(800, 600), resizable=True, element_justification='c')

    # Variables
    labels = list()
    labelsIndex = list()

    instructions = list()
    instructionsIndex = list()

    binCode = list()
    commandWords = list()

    document = ""
    result = ""

    while True:
        event, values = window.read()

        if event == gui.WINDOW_CLOSED or event == "Sair":
            break
        if event == "Gerar código binário":
            # Variables
            labels = list()
            labelsIndex = list()

            instructions = list()
            instructionsIndex = list()

            binCode = list()
            commandWords = list()

            document = ""
            result = ""
            directory = values['fileSelect']
            file = open(directory, 'r')
            lines = file.readlines()

            def getLines():
                address = 4194304
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
                    address = address + 4

            def labelTable(lbl, currentAddress):
                for index in range(0, len(labels)):
                    if lbl == labels[index]:
                        destiny = labelsIndex[index] - currentAddress
                        destiny /= 4
                        destiny = bin(int(destiny)).zfill(16)
                        if destiny.find('-') != -1:
                            destiny = destiny.replace('b', '0')
                            destiny = destiny.replace('-', '0')
                            destiny = destiny.replace('0', '2')
                            destiny = destiny.replace('1', '0')
                            destiny = destiny.replace('2', '1')
                            return destiny
                        else:
                            destiny = destiny.replace('b', '0')
                            return destiny

            def jumpFunc(lbl):
                for index in range(0, len(labels)):
                    if lbl == labels[index]:
                        destiny = labelsIndex[index]
                        destiny /= 4
                        destiny = bin(int(destiny)).zfill(26)
                        if destiny.find('-') != -1:
                            destiny = destiny.replace('b', '0')
                            destiny = destiny.replace('-', '0')
                            destiny = destiny.replace('0', '2')
                            destiny = destiny.replace('1', '0')
                            destiny = destiny.replace('2', '1')
                            return destiny
                        else:
                            destiny = destiny.replace('b', '0')
                            return destiny

            # Function to return de value of each register
            def registerTable(reg, codeFormat):
                if reg == "$zero":
                    return "00000"
                if reg == "$s0" or reg == "$16":
                    return "10000"
                if reg == "$s1" or reg == "$17":
                    return "10001"
                if reg == "$s2" or reg == "$18":
                    return "10010"
                if reg == "$s3" or reg == "$19":
                    return "10011"
                if reg == "$s4" or reg == "$20":
                    return "10100"
                if reg == "$s5" or reg == "$21":
                    return "10101"
                if reg == "$s6" or reg == "$22":
                    return "10111"
                if reg == "$s7" or reg == "$23":
                    return "11000"
                if reg == "$t0" or reg == "$8":
                    return "01000"
                if reg == "$t1" or reg == "$9":
                    return "01001"
                if reg == "$t2" or reg == "$10":
                    return "01010"
                if reg == "$t3" or reg == "$11":
                    return "01011"
                if reg == "$t4" or reg == "$12":
                    return "01100"
                if reg == "$t5" or reg == "$13":
                    return "01101"
                if reg == "$t6" or reg == "$14":
                    return "01110"
                if reg == "$t7" or reg == "$15":
                    return "01111"
                if isinstance(reg, int):
                    if codeFormat == "R":
                        reg = format(reg, 'b').zfill(5)
                        if reg.find('-') != -1:
                            reg.replace('b', '0')
                            reg.replace('-', '0')
                            reg.replace('0', '2')
                            reg.replace('1', '0')
                            reg.replace('2', '1')
                        return reg
                    if codeFormat == "I":
                        reg = format(reg, 'b').zfill(16)
                        if reg.find('-') != -1:
                            reg = reg.replace('b', '0')
                            reg = reg.replace('-', '0')
                            reg = reg.replace('0', '2')
                            reg = reg.replace('1', '0')
                            reg = reg.replace('2', '1')
                        return reg

            # Function to turn the command lines into binary code
            def assemblerTable(commandLines):
                lineCount = 0
                # Run through the program instruction lines
                while lineCount < len(commandLines):
                    # Run through each term in the line and remove the commas
                    for word in str(commandLines[lineCount]).replace(',', '').replace('(', ' ').replace(')',
                                                                                                        ' ').split():
                        commandWords.append(word)
                    lineCount += 1

                wordCount = 0
                currentAddress = 4194304
                while wordCount < len(commandWords):
                    # ----------- R FORMAT -------------
                    # SLL
                    if commandWords[wordCount] == "sll":
                        opCode = "000000"
                        rd = registerTable(commandWords[wordCount + 1], "R")
                        rs = registerTable(commandWords[wordCount + 2], "R")
                        sa = int(commandWords[wordCount + 3])
                        sa = registerTable(sa, "R")
                        rt = "01010"
                        funcCode = "000000"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3
                        else:
                            break

                    # SRL
                    elif commandWords[wordCount] == "srl":
                        opCode = "000000"
                        rd = registerTable(commandWords[wordCount + 1], "R")
                        rs = "00000"
                        sa = int(commandWords[wordCount + 3])
                        sa = registerTable(sa, "R")
                        rt = "01010"
                        funcCode = "000010"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3
                        else:
                            break

                    # JR
                    elif commandWords[wordCount] == "jr":
                        opCode = "000000"
                        rs = registerTable(commandWords[wordCount + 1], "R")
                        rd = "00000"
                        sa = "00000"
                        rt = "00000"
                        funcCode = "001000"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 2) <= len(commandWords):
                            wordCount = wordCount + 1

                    # MFHI
                    elif commandWords[wordCount] == "mfhi":
                        opCode = "000000"
                        rd = registerTable(commandWords[wordCount + 1], "R")
                        rs = "00000"
                        sa = "00000"
                        rt = "00000"
                        funcCode = "010000"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 2) <= len(commandWords):
                            wordCount = wordCount + 1

                    # MFLO
                    elif commandWords[wordCount] == "mflo":
                        opCode = "000000"
                        rd = registerTable(commandWords[wordCount + 1], "R")
                        rs = "00000"
                        sa = "00000"
                        rt = "00000"
                        funcCode = "010010"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 2) <= len(commandWords):
                            wordCount = wordCount + 1

                    # MULT
                    elif commandWords[wordCount] == "mult":
                        opCode = "000000"
                        rs = registerTable(commandWords[wordCount + 1], "R")
                        rt = registerTable(commandWords[wordCount + 2], "R")
                        sa = "00000"
                        rd = "00000"
                        funcCode = "011000"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 3) <= len(commandWords):
                            wordCount = wordCount + 2

                    # MULTU
                    elif commandWords[wordCount] == "multu":
                        opCode = "000000"
                        rs = registerTable(commandWords[wordCount + 1], "R")
                        rt = registerTable(commandWords[wordCount + 2], "R")
                        sa = "00000"
                        rd = "00000"
                        funcCode = "011001"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 3) <= len(commandWords):
                            wordCount = wordCount + 2

                    # DIV
                    elif commandWords[wordCount] == "div":
                        opCode = "000000"
                        rs = registerTable(commandWords[wordCount + 1], "R")
                        rt = registerTable(commandWords[wordCount + 2], "R")
                        sa = "00000"
                        rd = "00000"
                        funcCode = "011010"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 3) <= len(commandWords):
                            wordCount = wordCount + 2

                    # DIVU
                    elif commandWords[wordCount] == "divu":
                        opCode = "000000"
                        rs = registerTable(commandWords[wordCount + 1], "R")
                        rt = registerTable(commandWords[wordCount + 2], "R")
                        sa = "00000"
                        rd = "00000"
                        funcCode = "011011"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 3) <= len(commandWords):
                            wordCount = wordCount + 2

                    # ADD
                    elif commandWords[wordCount] == "add":
                        opCode = "000000"
                        rd = registerTable(commandWords[wordCount + 1], "R")
                        rs = registerTable(commandWords[wordCount + 2], "R")
                        rt = registerTable(commandWords[wordCount + 3], "R")
                        sa = "00000"
                        funcCode = "100000"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # ADDU
                    elif commandWords[wordCount] == "addu":
                        opCode = "000000"
                        rd = registerTable(commandWords[wordCount + 1], "R")
                        rs = registerTable(commandWords[wordCount + 2], "R")
                        rt = registerTable(commandWords[wordCount + 3], "R")
                        sa = "00000"
                        funcCode = "100001"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # SUB
                    elif commandWords[wordCount] == "sub":
                        opCode = "000000"
                        rd = registerTable(commandWords[wordCount + 1], "R")
                        rs = registerTable(commandWords[wordCount + 2], "R")
                        rt = registerTable(commandWords[wordCount + 3], "R")
                        sa = "00000"
                        funcCode = "100010"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # SUBU
                    elif commandWords[wordCount] == "subu":
                        opCode = "000000"
                        rd = registerTable(commandWords[wordCount + 1], "R")
                        rs = registerTable(commandWords[wordCount + 2], "R")
                        rt = registerTable(commandWords[wordCount + 3], "R")
                        sa = "00000"
                        funcCode = "100011"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # AND
                    elif commandWords[wordCount] == "and":
                        opCode = "000000"
                        rd = registerTable(commandWords[wordCount + 1], "R")
                        rs = registerTable(commandWords[wordCount + 2], "R")
                        rt = registerTable(commandWords[wordCount + 3], "R")
                        sa = "00000"
                        funcCode = "100100"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # OR
                    elif commandWords[wordCount] == "or":
                        opCode = "000000"
                        rd = registerTable(commandWords[wordCount + 1], "R")
                        rs = registerTable(commandWords[wordCount + 2], "R")
                        rt = registerTable(commandWords[wordCount + 3], "R")
                        sa = "00000"
                        funcCode = "100101"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # SLT
                    elif commandWords[wordCount] == "slt":
                        opCode = "000000"
                        rd = registerTable(commandWords[wordCount + 1], "R")
                        rs = registerTable(commandWords[wordCount + 2], "R")
                        rt = registerTable(commandWords[wordCount + 3], "R")
                        sa = "00000"
                        funcCode = "101010"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # SLTU
                    elif commandWords[wordCount] == "sltu":
                        opCode = "000000"
                        rd = registerTable(commandWords[wordCount + 1], "R")
                        rs = registerTable(commandWords[wordCount + 2], "R")
                        rt = registerTable(commandWords[wordCount + 3], "R")
                        sa = "00000"
                        funcCode = "101011"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # MUL
                    elif commandWords[wordCount] == "mul":
                        opCode = "011100"
                        rd = registerTable(commandWords[wordCount + 1], "R")
                        rs = registerTable(commandWords[wordCount + 2], "R")
                        rt = registerTable(commandWords[wordCount + 3], "R")
                        sa = "00000"
                        funcCode = "000010"
                        binCode.append(opCode + str(rs) + str(rt) + str(rd) + str(sa) + funcCode)
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # ----------- I FORMAT -------------
                    # BEQ
                    elif commandWords[wordCount] == "beq":
                        opCode = "000100"
                        rs = registerTable(commandWords[wordCount + 1], "I")
                        rt = registerTable(commandWords[wordCount + 2], "I")
                        imm = labelTable((commandWords[wordCount + 3]), currentAddress)
                        binCode.append(opCode + str(rs) + str(rt) + str(imm))
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # BNE
                    elif commandWords[wordCount] == "bne":
                        opCode = "000101"
                        rs = registerTable(commandWords[wordCount + 1], "I")
                        rt = registerTable(commandWords[wordCount + 2], "I")
                        imm = labelTable((commandWords[wordCount + 3]), currentAddress)
                        binCode.append(opCode + str(rs) + str(rt) + str(imm))
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # ADDI
                    elif commandWords[wordCount] == "addi":
                        opCode = "001000"
                        rs = registerTable(commandWords[wordCount + 2], "I")
                        rt = registerTable(commandWords[wordCount + 1], "I")
                        imm = commandWords[wordCount + 3]
                        imm = registerTable(int(imm), "I")
                        binCode.append(opCode + str(rs) + str(rt) + str(imm))
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # ADDIU
                    elif commandWords[wordCount] == "addiu":
                        opCode = "001001"
                        rs = registerTable(commandWords[wordCount + 2], "I")
                        rt = registerTable(commandWords[wordCount + 1], "I")
                        imm = commandWords[wordCount + 3]
                        imm = registerTable(int(imm), "I")
                        binCode.append(opCode + str(rs) + str(rt) + str(imm))
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # SLTI
                    elif commandWords[wordCount] == "slti":
                        opCode = "001010"
                        rs = registerTable(commandWords[wordCount + 2], "I")
                        rt = registerTable(commandWords[wordCount + 1], "I")
                        imm = commandWords[wordCount + 3]
                        imm = registerTable(int(imm), "I")
                        binCode.append(opCode + str(rs) + str(rt) + str(imm))
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # SLTIU
                    elif commandWords[wordCount] == "sltiu":
                        opCode = "001011"
                        rs = registerTable(commandWords[wordCount + 2], "I")
                        rt = registerTable(commandWords[wordCount + 1], "I")
                        imm = commandWords[wordCount + 3]
                        imm = registerTable(int(imm), "I")
                        binCode.append(opCode + str(rs) + str(rt) + str(imm))
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # ANDI
                    elif commandWords[wordCount] == "andi":
                        opCode = "001100"
                        rs = registerTable(commandWords[wordCount + 2], "I")
                        rt = registerTable(commandWords[wordCount + 1], "I")
                        imm = commandWords[wordCount + 3]
                        imm = registerTable(int(imm), "I")
                        binCode.append(opCode + str(rs) + str(rt) + str(imm))
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # ORI
                    elif commandWords[wordCount] == "ori":
                        opCode = "001101"
                        rs = registerTable(commandWords[wordCount + 2], "I")
                        rt = registerTable(commandWords[wordCount + 1], "I")
                        imm = commandWords[wordCount + 3]
                        imm = registerTable(int(imm), "I")
                        binCode.append(opCode + str(rs) + str(rt) + str(imm))
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # LUI
                    elif commandWords[wordCount] == "lui":
                        opCode = "001111"
                        rs = "00000"
                        rt = registerTable(commandWords[wordCount + 1], "I")
                        imm = commandWords[wordCount + 2]
                        imm = registerTable(int(imm), "I")
                        binCode.append(opCode + str(rs) + str(rt) + str(imm))
                        if (wordCount + 3) <= len(commandWords):
                            wordCount = wordCount + 2

                    # LW
                    elif commandWords[wordCount] == "lw":
                        opCode = "100011"
                        rs = registerTable(commandWords[wordCount + 3], "I")
                        rt = registerTable(commandWords[wordCount + 1], "I")
                        imm = commandWords[wordCount + 2]
                        imm = registerTable(int(imm), "I")
                        binCode.append(opCode + str(rs) + str(rt) + str(imm))
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # SW
                    elif commandWords[wordCount] == "sw":
                        opCode = "101011"
                        rs = registerTable(commandWords[wordCount + 3], "I")
                        rt = registerTable(commandWords[wordCount + 1], "I")
                        imm = commandWords[wordCount + 2]
                        imm = registerTable(int(imm), "I")
                        binCode.append(opCode + str(rs) + str(rt) + str(imm))
                        if (wordCount + 4) <= len(commandWords):
                            wordCount = wordCount + 3

                    # ----------- J FORMAT -------------
                    # J
                    elif commandWords[wordCount] == "j":
                        opCode = "000010"
                        iAddress = jumpFunc((commandWords[wordCount + 1]))
                        binCode.append(opCode + str(iAddress))
                        if (wordCount + 2) <= len(commandWords):
                            wordCount = wordCount + 1
                    # JAL
                    elif commandWords[wordCount] == "jal":
                        opCode = "000011"
                        iAddress = jumpFunc((commandWords[wordCount + 1]))
                        binCode.append(opCode + str(iAddress))
                        if (wordCount + 2) <= len(commandWords):
                            wordCount = wordCount + 1

                    currentAddress += 4
                    wordCount += 1

            getLines()
            assemblerTable(instructions)

            file.close()

            for k in range(0, len(lines)):
                document += lines[k]
                print(lines[k])

            for j in range(0, len(binCode)):
                result += binCode[j] + "\n"

            window.Element('fileReading').update(value=document)
            window.Element("result").update(value=result)
        if event == "Salvar arquivo .bin":

            binFile = open("program.bin", 'w')
            if binFile.write(result):
                gui.popup("Código binário salvo com sucesso em program.bin", no_titlebar=True, auto_close=True,
                          auto_close_duration=3, button_type=5)
            else:
                gui.popup("Impossível salvar arquivo na situação atual", no_titlebar=True, auto_close=True,
                          auto_close_duration=3, button_type=5)
            binFile.close()


mainWindow()
