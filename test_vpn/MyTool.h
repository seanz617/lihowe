#pragma once

#include <TlHelp32.h>

class MyTool
{
public:
	MyTool();
	~MyTool();
};

char* Base64Encode(char* src, int srclen);
void SplitStr(CString strSrc, CString strGap, CStringArray &strResult);
DWORD CheckProc(CString proc_name);
CString UrlEncode(CString strUnicode);