#include <iostream>
#include <fstream>
#include <memory.h>
#include <string.h>
#include "stdlib.h"
#include "time.h"

#define random(x) (rand()%x)

using namespace std;

int main(int argc, char** argv)
{
	srand((int)time(0));
	int len=1024;
	int total = atoi(argv[2]);
	cout<<"generating file "<<argv[1]<<" with size "<<total<<"kb"<<endl;
	char data[len];
	memset(data, 0, len);
    	fstream afile;
    	afile.open(argv[1], ios::app|ios::out|ios::in);
	for(int i=0; i < total; i++)
	{
		for(int i=0; i < len - 1; i++)
			data[i] = 'a' + random(26);
		afile<<data;
	}
	afile.close();
	return 0;
}
