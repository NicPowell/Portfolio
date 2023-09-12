#include <xdc/std.h>
#include <xdc/runtime/System.h>

#include <ti/sysbios/BIOS.h>
#include <ti/sysbios/knl/Clock.h>
#include <ti/sysbios/knl/Task.h>

#include <xdc/runtime/Types.h>
#include <xdc/runtime/Timestamp.h>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "gtz.h"

void clk_SWI_Read_Data(UArg arg0);
void clk_SWI_GTZ_All_Freq(UArg arg0);

extern void task0_dtmfGen(void);
extern void task1_dtmfDetect(void);

extern int sample, tdiff, tdiff_final, gtz_out[8];
extern short coef[8];
extern int flag;

short data[NO_OF_SAMPLES];
short *buffer;

/*
 *  ======== main ========
 */
int main() {
	System_printf("\n System Start\n");
	System_flush();

	/* Read binary data file */
	FILE* fp = fopen("../data.bin", "rb");
	if(fp==0) {
		System_printf("Error: Data file not found\n");
		System_flush();
		return 1;
	}
	fread(data, 2, NO_OF_SAMPLES, fp);
	buffer = (short*)malloc(2*8*10000);

	/* Create a Clock Instance */
	Clock_Params clkParams;

	/* Initialise Clock Instance with time period and timeout (system ticks) */
	Clock_Params_init(&clkParams);
	clkParams.period = 1;
	clkParams.startFlag = TRUE;

	/* Instantiate ISR for tone generation  */
	Clock_create(clk_SWI_Read_Data, TIMEOUT, &clkParams, NULL);

	/* Instantiate 8 parallel ISRs for each of the eight Goertzel coefficients */
	Clock_create(clk_SWI_GTZ_All_Freq, TIMEOUT, &clkParams, NULL);


	/* Start SYS_BIOS */
	BIOS_start();
}

/*
 *  ====== clk_SWI_Generate_DTMF =====
 *  Dual-Tone Generation
 *  ==================================
 */
void clk_SWI_Read_Data(UArg arg0) {
	static int tick;
	tick = Clock_getTicks();
	sample = data[tick%NO_OF_SAMPLES]; //
}

/*
 *  ====== clk_SWI_GTZ =====
 *  gtz sweep
 *  ========================
 */
void clk_SWI_GTZ_All_Freq(UArg arg0) {
	// define variables for timing
	static int start, stop;

	// define feedback times as N
	static int N = 0;

   	//Record start time
	start = Timestamp_get32();

	sample = sample >> 8;
	static int Goertzel_Value=0;
	short input = (short) (sample);
	input = input >> 4;
	static short delay[8]={0};//Creates an array of all the delay values with starting value 0
	static short delay_1[8] = {0};//Creates an array of all the delay1 values with starting value 0
	static short delay_2[8] = {0};//Creates an array of all the delay2 values with starting value 0

	int prod1, prod2, prod3;
	int i;

	/* TODO 1. Complete the feedback loop of the GTZ algorithm*/
	/* ========================= */
	for (i = 0; i < 8; i++){	//looping through each coefficient for the feedback loop
		prod1 = (delay_1[i]*coef[i])>>14;
		delay[i] = input + (short)prod1 - delay_2[i];
		delay_2[i] = delay_1[i];
		delay_1[i] = delay[i];
	}//storing the values of delay in an array to make them transferable to the feedforward loop
	/* ========================= */
	N++;
	//because of the static int the N++ iterates each time function is called
	//Record stop time
	stop = Timestamp_get32();
	//Record elapsed time
	tdiff = stop-start;

	if (N == 206) {// When we have completed 205 feedback loops we move onto feedfoward
	   	//Record start time
		start = Timestamp_get32();

		/* TODO 2. Complete the feed forward loop of the GTZ algorithm*/
		/* ========================= */
		for (i = 0; i < 8; i++){//looping through feed forward for each coefficient.
			prod1 = (delay_1[i] * delay_1[i]);
			prod2 = (delay_2[i] * delay_2[i]);
			prod3 = (delay_1[i] * coef[i])>>14;
			prod3 = prod3 * delay_2[i];
			Goertzel_Value = (prod1 + prod2 - prod3);
			Goertzel_Value <<=8;//scale up for a suitable value to create a cut off
			delay_1[i] = delay_2[i] = 0;
			gtz_out[i] = Goertzel_Value;//Storing each gtz value corresponding to each coefficient
		}
		/* ========================= */
		flag = 1;
		N = 0;
		// resets N to 0 so for the next coefficient to repeat process
		//Record stop time
		stop = Timestamp_get32();
		//Record elapsed time
		tdiff_final = stop-start;
	//time taken to run the feed forward
	}
}