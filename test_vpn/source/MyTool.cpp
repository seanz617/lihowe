#include "stdafx.h"
#include "MyTool.h"


MyTool::MyTool()
{
}


MyTool::~MyTool()
{
}

char* base64 = (char *)"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
char* Base64Encode(char* src, int srclen)
{
	int n, buflen, i, j;
	static char *dst;
	char* buf = src;
	buflen = n = srclen;
	dst = (char*)malloc(buflen / 3 * 4 + 3);
	memset(dst, 0, buflen / 3 * 4 + 3);
	for (i = 0, j = 0; i <= buflen - 3; i += 3, j += 4) {
		dst[j] = (buf[i] & 0xFC) >> 2;
		dst[j + 1] = ((buf[i] & 0x03) << 4) + ((buf[i + 1] & 0xF0) >> 4);
		dst[j + 2] = ((buf[i + 1] & 0x0F) << 2) + ((buf[i + 2] & 0xC0) >> 6);
		dst[j + 3] = buf[i + 2] & 0x3F;
	}
	if (n % 3 == 1) {
		dst[j] = (buf[i] & 0xFC) >> 2;
		dst[j + 1] = ((buf[i] & 0x03) << 4);
		dst[j + 2] = 64;
		dst[j + 3] = 64;
		j += 4;
	}
	else if (n % 3 == 2) {
		dst[j] = (buf[i] & 0xFC) >> 2;
		dst[j + 1] = ((buf[i] & 0x03) << 4) + ((buf[i + 1] & 0xF0) >> 4);
		dst[j + 2] = ((buf[i + 1] & 0x0F) << 2);
		dst[j + 3] = 64;
		j += 4;
	}
	for (i = 0; i < j; i++)
		dst[i] = base64[(int)dst[i]];
	dst[j] = 0;
	return dst;
}

void SplitStr(CString strSrc, CString strGap, CStringArray &strResult)
{
	int nPos = strSrc.Find(strGap);
	CString strLeft = _T("");

	while (0 <= nPos)
	{
		strLeft = strSrc.Left(nPos);
		if (!strLeft.IsEmpty())
		{
			strResult.Add(strLeft);
		}

		strSrc = strSrc.Right(strSrc.GetLength() - nPos - strGap.GetLength());
		nPos = strSrc.Find(strGap);
	}

	if (!strSrc.IsEmpty())
	{
		strResult.Add(strSrc);
	}
}
