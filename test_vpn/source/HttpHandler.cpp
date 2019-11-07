#include "stdafx.h"
#include "HttpHandler.h"

HttpHandler::HttpHandler()
{
}


HttpHandler::~HttpHandler()
{
}

BOOL HttpHandler::Send(CInternetSession** pis, CHttpFile** phf, CString url)
{
	*pis = new CInternetSession(AfxGetAppName(), 1, PRE_CONFIG_INTERNET_ACCESS);
	//(*pis)->SetOption(INTERNET_OPTION_CONNECT_TIMEOUT, 1000*10);
	//(*pis)->SetOption(INTERNET_OPTION_CONNECT_BACKOFF, 1000);
	//(*pis)->SetOption(INTERNET_OPTION_CONNECT_RETRIES, 3);
	//(*pis)->SetOption(INTERNET_OPTION_DATA_RECEIVE_TIMEOUT, 1000);

	CHttpConnection *pHttpConn = NULL;
	CString strUrl;
	DWORD dwServiceType;
	CString strServer, strObj, strUser, strPwd;
	INTERNET_PORT nPort;

	if (!AfxParseURLEx(url, dwServiceType, strServer, strObj, nPort, strUser, strPwd, ICU_NO_ENCODE))
		return FALSE;

	if (!pHttpConn)
		pHttpConn = (*pis)->GetHttpConnection(strServer);

	int nVal = 1000;
	(*pis)->SetOption(INTERNET_OPTION_CONNECT_TIMEOUT, &nVal, sizeof(nVal));
	*phf = pHttpConn->OpenRequest(_T("GET"), strObj);

	try
	{
		(*phf)->SendRequest();
	}
	catch (CInternetException *pEx)
	{
		pEx->Delete();
		delete (*phf); *phf = NULL;
		return FALSE;
	}

	DWORD dwRet;
	(*phf)->QueryInfoStatusCode(dwRet);
	if (dwRet != HTTP_STATUS_OK)
		return FALSE;

	return TRUE;
}

BOOL HttpHandler::ParseJson(CMap<CString, LPCTSTR, CString, LPCTSTR>& mapContent, CString msgJson)
{
	CStringArray strArray;
	CString strTemp = msgJson;

	strTemp.Remove('"');
	strTemp.Remove('{');
	strTemp.Remove('}');
	int strTempLength = strTemp.GetLength();

	int index = 0;
	while (true) {
		index = strTemp.Find(',');
		if (-1 == index) {
			strArray.Add(strTemp);
			break;
		}
		strArray.Add(strTemp.Left(index));
		strTemp = strTemp.Right(strTemp.GetLength() - index - 1);
	}
	int length = strArray.GetSize();
	CString strMap;
	int subIndex = 0;
	CString strKey("");
	CString strValue("");
	for (int i = 0; i < length; i++) {
		strMap = strArray.GetAt(i);
		subIndex = strMap.Find(':');
		strKey = strMap.Left(subIndex);
		strValue = strMap.Right(strMap.GetLength() - subIndex - 1);
		mapContent.SetAt(strKey, strValue);
	}
	return TRUE;
}

void HttpHandler::GetCityAndIsp(CString ip,CString& city,CString& isp)
{
	CInternetSession* pis = NULL;
	CHttpFile* phf = NULL;

	CString url;
	url.Format(_T("http://ip-api.com/json/%s"),ip);
	
	if (Send(&pis, &phf, url))
	{
		int numread = 0;
		char buf[4096] = { 0 };
		while ((numread = phf->Read(buf, sizeof(buf) - 1)) > 0)
		{
			CString tmp(buf);
			CMap<CString, LPCTSTR, CString, LPCTSTR> my_Map;
			ParseJson(my_Map, tmp);
			my_Map.Lookup(_T("city"), city);
			my_Map.Lookup(_T("isp"), isp);
		}
		pis->Close();
		delete pis; pis = NULL;
		phf->Close();
		delete phf; phf = NULL;
	}
}

void HttpHandler::GetExternalIP(CString& ip,CString url)
{
	CInternetSession* pis = NULL;
	CHttpFile* phf = NULL;

	ip = _T("");
	if (Send(&pis, &phf, url))
	{
		int numread = 0;
		char buf[64] = { 0 };
		while ((numread = phf->Read(buf, sizeof(buf) - 1)) > 0)
			ip += buf;
		pis->Close();
		delete pis; pis = NULL;
		phf->Close();
		delete phf; phf = NULL;
	}
}

/*
BOOL HttpHandler::DownloadFile(CString serverName, CString objectName, CString path)
{
	HINTERNET hOpen = 0;
	HINTERNET hConnect = 0;
	HINTERNET hRequest = 0;
	BOOL bResult = FALSE;

	do {
		hOpen = WinHttpOpen(_T("DownloadFile"), WINHTTP_ACCESS_TYPE_DEFAULT_PROXY, WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, 0);
		if (!hOpen) {
			break;
		}
		hConnect = WinHttpConnect(hOpen, serverName, INTERNET_DEFAULT_HTTPS_PORT, 0);
		if (!hConnect) {
			wprintf(L"WinHttpConnect failed (0x%.8X)\n", GetLastError());
			break;
		}
		hRequest = WinHttpOpenRequest(hConnect, L"GET", objectName, NULL, WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES, WINHTTP_FLAG_SECURE);
		if (!hRequest)
		{
			wprintf(L"WinHttpOpenRequest failed (0x%.8X)\n", GetLastError());
			break;
		}
		if (!WinHttpSendRequest(hRequest, WINHTTP_NO_ADDITIONAL_HEADERS, 0, WINHTTP_NO_REQUEST_DATA, 0, 0, 0))
		{
			wprintf(L"WinHttpSendRequest failed (0x%.8X)\n", GetLastError());
			break;
		}
		if (!WinHttpReceiveResponse(hRequest, 0))
		{
			wprintf(L"WinHttpReceiveResponse failed (0x%.8X)\n", GetLastError());
			break;
		}

		TCHAR szContentLength[32] = { 0 };
		DWORD cch = 64;
		DWORD dwHeaderIndex = WINHTTP_NO_HEADER_INDEX;
		BOOL haveContentLength = WinHttpQueryHeaders(hRequest, WINHTTP_QUERY_CONTENT_LENGTH, NULL,
			&szContentLength, &cch, &dwHeaderIndex);
		DWORD dwContentLength;
		if (haveContentLength) dwContentLength = _wtoi(szContentLength);

		BYTE Buffer[4096];
		HANDLE hFile = CreateFile(path, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, 0, NULL);
		if (hFile == INVALID_HANDLE_VALUE) {
			wprintf(L"CreateFile(%s) failed (0x%.8X)\n", path, GetLastError());
			break;
		}

		DWORD dwSize, dwWrite;
		while (WinHttpQueryDataAvailable(hRequest, &dwSize) && dwSize) {
			if (dwSize > 4096) dwSize = 4096;

			WinHttpReadData(hRequest, Buffer, dwSize, &dwSize);
			WriteFile(hFile, Buffer, dwSize, &dwWrite, NULL);
		}
		CloseHandle(hFile);
		bResult = TRUE;
	} while (FALSE);

	if (hRequest) WinHttpCloseHandle(hRequest);
	if (hConnect) WinHttpCloseHandle(hConnect);
	if (hOpen) WinHttpCloseHandle(hOpen);

	return bResult;
}
*/