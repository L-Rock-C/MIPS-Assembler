L0: 	addi $8, $9, 3
L1: 	beq $8, $9, L0
    	bne $8, $9, L3
	addiu $8, $9, 3
	slti $8, $9, 3
	sltiu $8, $9, 3
L3:	andi $8, $9, 3
	ori $8, $9, 3
	lui $8, 3
	lw $8, 4($9)
	sw $8, 4($9)

