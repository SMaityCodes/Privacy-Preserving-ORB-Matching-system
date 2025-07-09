/**  ALL COPYRIGHTS RESERVED BY MANASA PJ & S MAITY **/  

pragma circom 2.0.0;


template IntDivision(){
	signal input a, b;  // dividend and divisor
	signal output q, r, q_rounded;
	if(b == 0) log("DIVISION BY ZERO EROORRRRRRR !!!");
	q <-- a \ b;
	r <-- a % b;
	a === b * q + r;
	
	component lt = LessThan(32);  // For 32-bit numbers
	lt.in[0] <== 2 * r;  
	lt.in[1] <== b;  
	signal isLte <== lt.out;  
	q_rounded <== q + (1-lt.out);
	// log("q = ", q, ", r = ", r, "r < 0.5?", isLte);	
}
