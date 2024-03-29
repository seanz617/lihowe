#pragma once
class ShellHandler
{
public:
	ShellHandler();
	~ShellHandler();
	CString app;
	CString cmdline;
	CString output;
	DWORD ret_code;
	CWnd* call_wnd;
	UINT callback_msg;
	BOOL wget;
	BOOL run_flag;
	HANDLE ph;
	DWORD Run(CString pApp, CString pCmdline, CWnd* pWnd, UINT pMsg);
	BOOL ParseJson(CMap<CString, LPCTSTR, CString, LPCTSTR>& mapContent, CString jsonStr);

};