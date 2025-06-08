/**  ALL COPYRIGHTS RESERVED BY MANASA PJ & S MAITY **/  

pragma circom 2.0.0;


template IntDivision(){
	signal input a, b;  // dividend and divisor
	signal output q, r, q_rounded;
	if(b == 0) log("DIVISION BY ZERO EROORRRRRRR !!!");
	q <-- a \ b;
	r <-- a % b;
	a === b * q + r;
	
	component lte = LessEqThan(32);  // For 32-bit numbers
	lte.in[0] <== 2 * r;  
	lte.in[1] <== b;  
	signal isLte <== lte.out;  
	q_rounded <== q + (1-lte.out);
	// log("q = ", q, ", r = ", r, "r<=0.5?", isLte);	
}
