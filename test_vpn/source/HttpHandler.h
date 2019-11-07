#pragma once
#include <afxinet.h>

class HttpHandler
{
public:
	HttpHandler();
	~HttpHandler();

	BOOL Send(CInternetSession** pis, CHttpFile** phf, CString url);
	BOOL ParseJson(CMap<CString, LPCTSTR, CString, LPCTSTR>& mapContent, CString jsonStr);

	void GetExternalIP(CString& ip, CString url);
	void GetCityAndIsp(CString ip,CString& city,CString& isp);

	//static BOOL DownloadFile(CString serverName, CString objectName, CString path);
};

