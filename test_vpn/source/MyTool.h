#pragma once
class MyTool
{
public:
	MyTool();
	~MyTool();
};

char* Base64Encode(char* src, int srclen);
void SplitStr(CString strSrc, CString strGap, CStringArray &strResult);