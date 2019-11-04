#include "stdafx.h"
#include "ShellHandler.h"

UINT RunCmd(LPVOID pParam)
{
	if (NULL != pParam)
	{
		ShellHandler* psh = (ShellHandler*)pParam;

		SECURITY_ATTRIBUTES sa;
		sa.nLength = sizeof(SECURITY_ATTRIBUTES);
		sa.lpSecurityDescriptor = NULL;
		sa.bInheritHandle = TRUE;
		HANDLE hRead, hWrite;
		if (!CreatePipe(&hRead, &hWrite, &sa, 0))
			return 10000;

		STARTUPINFO si;
		PROCESS_INFORMATION pi;
		ZeroMemory(&si, sizeof(STARTUPINFO));
		si.cb = sizeof(STARTUPINFO);
		GetStartupInfo(&si);
		si.hStdError = hWrite;
		si.hStdOutput = hWrite;
		si.wShowWindow = SW_HIDE;
		si.dwFlags = STARTF_USESHOWWINDOW | STARTF_USESTDHANDLES;
		if (!CreateProcess(psh->app, psh->cmdline.GetBuffer(), NULL, NULL, TRUE, NULL, NULL, NULL, &si, &pi))
			return 10001;
		CloseHandle(hWrite);

		char buffer[4096] = { 0 };
		DWORD bytesRead;
		psh->output = _T("");
		while (true)
		{
			if (ReadFile(hRead, buffer, 4095, &bytesRead, NULL) == NULL)
				break;

			CString temp;
			temp = buffer;
			psh->output += temp;
			memset(buffer, 0, 4096);
		}
		CloseHandle(hRead);

		GetExitCodeProcess(pi.hProcess, &(psh->ret_code));
		
		psh->call_wnd->SendMessage(psh->callback_msg,0,NULL);

		return psh->ret_code;
	}
}

ShellHandler::ShellHandler()
{
}

ShellHandler::~ShellHandler()
{
}

DWORD ShellHandler::Run(CString pApp, CString pCmdline, CWnd* pWnd, UINT pMsg)
{
	app = pApp;
	cmdline = pCmdline;
	call_wnd = pWnd;
	callback_msg = pMsg;

	CWinThread* run_cmd_thread = AfxBeginThread(RunCmd, this, THREAD_PRIORITY_NORMAL, 0, 0, NULL);
	//WaitForSingleObject(run_cmd_thread->m_hThread,180000);
	
	return ret_code;
}
