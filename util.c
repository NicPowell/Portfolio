#include <xdc/std.h>
#include <xdc/runtime/System.h>

#include <ti/sysbios/BIOS.h>
#include <ti/sysbios/knl/Clock.h>
#include <ti/sysbios/knl/Task.h>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "gtz.h"

int tdiff,tdiff_final;

int sample, gtz_out[8];
int flag = 0;

short coef[8] = //697	770		852		941		1209	1336	1477  1633
			{ 0x6D02, 0x68AD, 0x63FC, 0x5EE7, 0x4A70, 0x4090, 0x3290, 0x23CE }; // goertzel coefficients
void task1_dtmfDetect();
void task2_dtmfGenerate(char* keys);
extern short* buffer;

void task1_dtmfDetect() {
	int i, n, k,h;
	char pad[4][4] = {{'1','2','3','A'},{'4','5','6','B'},{'7','8','9','C'},{'*','0','#','D'}};
    char result[8];

	for(n=0;n<8;n++) {
		while (!flag) Task_sleep(210);
		/* TODO 3. Complete code to detect the 8 digits based on the GTZ output */
		/* ========================= */


		for (i = 0; i < 8; i++) {
			//printf("i=%d, gtz_out=%d\n, coef=%d\n", i, gtz_out[i], coef[i]);
		    int gtz_cutoff = 200000;
		for (h = 0; h < 4; h++) {
		    if (gtz_out[h] > gtz_cutoff){
				for (k = 0; k < 4; k++) {
					if (gtz_out[k+4] > gtz_cutoff){
						result[n] = pad[h][k];}
				}}}
//4 loops that check for every value based off the gtz value and assign the result to high gtz outputs
//if the output is higher than the gtz cutoff we move to the next value
//the first loop goes through each result(each tone)
// second loop searches each coefficient
//third loop goes through each row of the digit pad
//fourth loop goes through each digit in the first row of the pad
}

		printf("The corresponding key is %c\n", result[n]);



		flag = 0;
}
	printf("\nDetection finished\n");
	printf("Generating audio\n");
	task2_dtmfGenerate(result);
	printf("Finished\n");
	printf("Detected DTMF tones: ");
}

void task2_dtmfGenerate(char* keys)
{
	int fs = 10000;
	float tone_length = 0.5;
	int n_tones = 8;
	int samples_per_tone = (int) (tone_length * fs);
	int samples_total = samples_per_tone * n_tones;
	int i, n;
	char digit;
	for(n=0;n<n_tones;n++) {
		digit = keys[n];
		int freq1, freq2;
		 switch (digit) {
		 	 case '1': freq1 = 697; freq2 = 1209; break;//if the key is 1 then freq1 is assigned to 697 and freq2 is 1209
		     case '2': freq1 = 697; freq2 = 1336; break;
		     case '3': freq1 = 697; freq2 = 1477; break;
		     case '4': freq1 = 770; freq2 = 1209; break;
		     case '5': freq1 = 770; freq2 = 1336; break;
		     case '6': freq1 = 770; freq2 = 1477; break;
		     case '7': freq1 = 852; freq2 = 1209; break;
		     case '8': freq1 = 852; freq2 = 1336; break;
		     case '9': freq1 = 852; freq2 = 1477; break;
		     case '*': freq1 = 941; freq2 = 1209; break;
		     case '0': freq1 = 941; freq2 = 1336; break;
		     case '#': freq1 = 941; freq2 = 1477; break;
		     case 'A': freq1 = 697; freq2 = 1633; break;
		     case 'B': freq1 = 770; freq2 = 1633; break;
		     case 'C': freq1 = 852; freq2 = 1633; break;
		     case 'D': freq1 = 941; freq2 = 1633; break;
		     default: freq1 = 0; freq2 = 0; break;
		 }
		 //sample = (int) 32768.0*sin(2.0*PI*freq1*TICK_PERIOD*tick) + 32768.0*sin(2.0*PI*freq2*TICK_PERIOD*tick);
		 // Generate two sine waves with the corresponding frequencies
		 float t, dt, a1, a2;
		 for (i = 0; i < samples_per_tone; i++) {
		     t = (float)i / fs;
		     dt = 2.0 * PI * t;
		     a1 = sin(dt * freq1);
		     a2 = sin(dt * freq2);
		     buffer[i + n * samples_per_tone] = (short)(a1 + a2) * 16384;
		 }
		/* buffer[..] = ... */
		/* ========================= */
	}

	/* Writing the data to a wav file */
	FILE* fp = fopen("../answer.wav", "wb");
	int datasize = samples_total*2;
	int filesize = 36+datasize;
	int headersize = 16;
	int datatype = 1;
	int nchannel = 1;
	int byterate = fs*2;
	int align = 2;
	int bitpersample = 16;

	fwrite("RIFF", 1, 4, fp);
	fwrite(&filesize, 4, 1, fp);
	fwrite("WAVE", 1, 4, fp);
	fwrite("fmt ", 1, 4, fp);
	fwrite(&headersize, 4, 1, fp);
	fwrite(&datatype, 2, 1, fp);
	fwrite(&nchannel, 2, 1, fp);
	fwrite(&fs, 4, 1, fp);
	fwrite(&byterate, 4, 1, fp);
	fwrite(&align, 2, 1, fp);
	fwrite(&bitpersample, 2, 1, fp);
	fwrite("data", 1, 4, fp);
	fwrite(&datasize, 4, 1, fp);
	fwrite(buffer, 2, samples_total, fp);
	fclose(fp);