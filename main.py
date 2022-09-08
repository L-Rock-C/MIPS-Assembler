L1: add $t0, $s1, $s2
L2: addi $t1, $s3, 7
	beq $t0, $t1, L1
	j L2

# Read file
file = open('exemple1.asm', 'r')
lines = file.readlines()

# Variables
labels = list()
labelsIndex = list()

# Get labels
# Run through each line
def getLabel():
    count = 0
    for line in lines:
        # Check if there's a label
        if line.find(":") > 0:
            tempStr = ""
            # Set the label value and index
            for letter in line:
                tempStr += letter
                if letter == ":":
                    labels.append(tempStr.strip(":"))
                    labelsIndex.append(count)
                    break
        count += 1


def getInstruction():
    for line in lines:
        


getLabel()


