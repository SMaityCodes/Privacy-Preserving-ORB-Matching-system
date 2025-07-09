const circomlibjs = require("circomlibjs");
const fs = require("fs").promises;

const FIELD_PRIME = BigInt("21888242871839275222246405745257275088548364400416034343698204186575808495617");


//  Maps each integer to Cirom's modular domian Zp
function modField(x) {
  return ((BigInt(x) % FIELD_PRIME) + FIELD_PRIME) % FIELD_PRIME;
}

function bitsToBigInt(bits) {
  const bitString = bits.join('');
  return BigInt('0b' + bitString);
}


function CalMerkleRoot(Leaves, poseidon) {
  	let currentLevel = Leaves.map(leaf => leaf.toString());
        while (currentLevel.length > 1) {
            const nextLevel = [];
            for (let i = 0; i < currentLevel.length; i += 2) {
                const hash = poseidon.F.toString(poseidon([
                    BigInt(currentLevel[i]), 
                    BigInt(currentLevel[i+1] || "0")
                ]));
                nextLevel.push(hash);
            }
            currentLevel = nextLevel;
        }

        const merkleRoot = currentLevel[0];
  	return (merkleRoot);
}


(async () => {
    try {
        // Initialize Poseidon once
        const poseidon = await circomlibjs.buildPoseidon();
        
        // Read and process input file
        const input = JSON.parse(await fs.readFile("circomInput.json", "utf8"));
        
        const in1 = input.in1;
  	const in2 = input.in2;
  	const LeftLeavesIn1 = []; const RightLeavesIn1 = [];
  	const LeftLeavesIn2 = []; const RightLeavesIn2 = [];
  	
  	//console.log('--- in1 ---');
	  in1.forEach((row, rowIndex) => {
	    const left128 = bitsToBigInt(row.slice(0, 128));
	    const right128 = bitsToBigInt(row.slice(128, 256));
	    //console.log(`Row ${rowIndex}:`);
	    //console.log(`  Left 128 bits:  ${left128}`);
	    //console.log(`  Right 128 bits: ${right128}`);
	    LeftLeavesIn1.push(left128);
	    RightLeavesIn1.push(right128);
	  });
	  
	 //console.log('\n--- in2 ---');
	  in2.forEach((row, rowIndex) => {
	    const left128 = bitsToBigInt(row.slice(0, 128));
	    const right128 = bitsToBigInt(row.slice(128, 256));
	    //console.log(`Row ${rowIndex}:`);
	    //console.log(`  Left 128 bits:  ${left128}`);
	    //console.log(`  Right 128 bits: ${right128}`);
	    LeftLeavesIn2.push(left128);
	    RightLeavesIn2.push(right128);
	  });
	  //console.log(leaves.toString());
	  
        
        
         
	//console.log("No. of Leaves in LeftLeavesIn1:", LeftLeavesIn1.length);
	//console.log("No. of Leaves in RightLeavesIn1:", RightLeavesIn1.length);
	//console.log("No. of Leaves in LeftLeavesIn2:", LeftLeavesIn1.length);
	//console.log("No. of Leaves in RightLeavesIn2:", RightLeavesIn2.length);
	
        while (LeftLeavesIn1.length < 128) LeftLeavesIn1.push(0n);//Pad to 128 leaves
        while (RightLeavesIn1.length < 128) RightLeavesIn1.push(0n);//Pad to 128 leaves
        while (LeftLeavesIn2.length < 128) LeftLeavesIn2.push(0n);//Pad to 128 leaves
        while (RightLeavesIn2.length < 128) RightLeavesIn2.push(0n);//Pad to 128 leaves
        
	//console.log("Flattened Array:", LeftLeavesIn1); 
	
	
        // Compute Merkle root
        const merkleRoot1 = CalMerkleRoot(LeftLeavesIn1, poseidon);
        const merkleRoot2 = CalMerkleRoot(RightLeavesIn1, poseidon);
        const merkleRoot3 = CalMerkleRoot(LeftLeavesIn2, poseidon);
        const merkleRoot4 = CalMerkleRoot(RightLeavesIn2, poseidon);
        console.log("Merkle Root of LeftLeavesIn1:", merkleRoot1);
        console.log("Merkle Root of RightLeavesIn1:", merkleRoot2);
        console.log("Merkle Root of LeftLeavesIn2:", merkleRoot3);
        console.log("Merkle Root of RightLeavesIn2:", merkleRoot4);
        
	
        // Save to input.json
        await fs.writeFile(
            "circomInputWithHash.json",
            JSON.stringify({...input, In1LeftHash: merkleRoot1, In1RightHash: merkleRoot2, In2LeftHash: merkleRoot3, In2RightHash: merkleRoot4 }, null, 2)
        );
        
    } catch (error) {
        console.error("Error:", error);
        process.exit(1);
    }
})();
