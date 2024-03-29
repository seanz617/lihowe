// TestSettings.cpp: 实现文件
//

#include "stdafx.h"
#include "MFCApplication1.h"
#include "TestSettings.h"
#include "afxdialogex.h"

IMPLEMENT_DYNAMIC(TestSettings, CDialogEx)

TestSettings::TestSettings(CWnd* pParent /*=nullptr*/)
	: CDialogEx(IDD_DIALOG2, pParent)
{
}

TestSettings::~TestSettings()
{
}

void TestSettings::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_COMBO1, proxy_list);
	DDX_Control(pDX, IDC_COMBO2, stun_list);
}

BEGIN_MESSAGE_MAP(TestSettings, CDialogEx)
	ON_WM_CTLCOLOR()
	ON_BN_CLICKED(IDC_BUTTON1, &TestSettings::OnBnClickedButton1)
	ON_BN_CLICKED(IDC_BUTTON5, &TestSettings::OnBnClickedButton5)
	ON_WM_DESTROY()
	ON_BN_CLICKED(IDC_BUTTON2, &TestSettings::OnBnClickedButton2)
	ON_WM_TIMER()
	ON_WM_SIZE()
	ON_MESSAGE(WM_CHILD_WND_RESIZE, &TestSettings::OnChildWndResize)
	ON_MESSAGE(WM_LOAD_PVPN_CONFIG, &TestSettings::OnLoadPvpnConfig)
	ON_MESSAGE(WM_UPDATE_PROXY_STUN, &TestSettings::OnUpdateProxyStun)
END_MESSAGE_MAP()

HBRUSH TestSettings::OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor)
{
	HBRUSH hbr = CDialogEx::OnCtlColor(pDC, pWnd, nCtlColor);
	return (HBRUSH)m_brush.GetSafeHandle();
	//return hbr;
}

void TestSettings::StartPvpn()
{
	static int start_pvpn = 0;
	if (start_pvpn > 0) return;
	start_pvpn = 1;

	if (!CheckPvpn())
	{
		ZeroMemory(&StartupInfo, sizeof(StartupInfo));
		StartupInfo.cb = sizeof StartupInfo;
		StartupInfo.wShowWindow = SW_HIDE;
		StartupInfo.dwFlags = STARTF_USESHOWWINDOW | STARTF_USESTDHANDLES;
		for (int i = 0; i < 3; i++)
		{
			CString agent_cmd;
			CString proxy_str = _T(""), stun_str = _T("");
			int a = proxy_list.GetCurSel();
			proxy_str = ptc->ProxyInfos[proxy_list.GetCurSel()].ProxyServer;
			stun_str = ptc->StunInfos[stun_list.GetCurSel()].StunAddress;
			agent_cmd.Format(_T("pvpn.exe agent --udpport 8071 --tcpport 8071 --rpcport 18071 --datadir . --socks-port 19080 --proxy %s --stun %s"),proxy_str,stun_str);
			//AfxMessageBox(agent_cmd);
			BOOL ret = CreateProcess(_T("pvpn.exe"), agent_cmd.GetBuffer(), NULL, NULL, FALSE, 0, NULL, NULL, &StartupInfo, &ProcessInfo);
			if (ret)
			{
				pvpn_pid = ProcessInfo.dwProcessId;
				::CloseHandle(ProcessInfo.hThread);
				break;
			}
		}

		if (!CheckPvpn())
			AfxMessageBox(_T("start vpn client failed"));
	}

	start_pvpn = 0;
}

void TestSettings::StopPvpn()
{
	for (int i = 0; i < 6; i++)
	{
		if (CheckPvpn())
		{
			HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pvpn_pid);
			if (hProcess != NULL)
			{
				TerminateProcess(hProcess, 0);
				::CloseHandle(hProcess);
			}
			else
				break;
			Sleep(500);
		}
		else
			break;
	}
}

BOOL TestSettings::CheckPvpn()
{
	BOOL found_flag = FALSE;
	
	HANDLE hSnapshot = NULL;
	PROCESSENTRY32 pe;
	pe.dwSize = sizeof(PROCESSENTRY32);
	hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
	Process32First(hSnapshot, &pe);
	do
	{
		CString exe_name = pe.szExeFile;
		exe_name = exe_name.Trim();
		if (exe_name == _T("pvpn\.exe"))
		{
			pvpn_pid = pe.th32ProcessID;
			pvpn_parent_pid = pe.th32ParentProcessID;

			found_flag = TRUE;
			break;
		}
	} while (Process32Next(hSnapshot, &pe));
	CloseHandle(hSnapshot);
	
	if ((!found_flag) && WAIT_TIMEOUT == WaitForSingleObject(ProcessInfo.hProcess, 10))
		found_flag = TRUE;

	return found_flag;
}

BOOL TestSettings::OnInitDialog()
{
	CDialogEx::OnInitDialog();
	m_brush.CreateSolidBrush(RGB(255, 255, 255));
	
	pvpn_pid = -1;
	pvpn_parent_pid = -1;

	return TRUE;
}

void TestSettings::OnBnClickedButton1()
{
	StartPvpn();
	if (CheckPvpn())
	{
		GetDlgItem(IDC_BUTTON1)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_BUTTON5)->ShowWindow(SW_SHOW);
	}
}

void TestSettings::OnBnClickedButton5()
{
	StopPvpn();
	if (!CheckPvpn())
	{
		GetDlgItem(IDC_BUTTON1)->ShowWindow(SW_SHOW);
		GetDlgItem(IDC_BUTTON5)->ShowWindow(SW_HIDE);
	}
}

void TestSettings::OnDestroy()
{
	CDialogEx::OnDestroy();
	KillTimer(WM_CHECK_PVPN_PROC);
	StopPvpn();
}

void TestSettings::OnBnClickedButton2()
{
	static int update_setting = 0;
	if (update_setting > 0 || !CheckPvpn())
		return;
	update_setting = 1;

	CString cmdline;
	CString proxy = ptc->ProxyInfos[proxy_list.GetCurSel()].ProxyServer;
	CString stun = ptc->StunInfos[stun_list.GetCurSel()].StunAddress;
	cmdline.Format(_T("pvpn.exe set-proxy-peer --proxy=%s --stun=%s --rpcport=18071"), proxy, stun);
	//AfxMessageBox(cmdline);
	sh_update_proxy_stun.Run(_T("pvpn.exe"), cmdline,this,WM_UPDATE_PROXY_STUN);

	update_setting = 0;
}

void TestSettings::OnTimer(UINT_PTR nIDEvent)
{
	if (!CheckPvpn())
	{
		GetDlgItem(IDC_BUTTON1)->ShowWindow(SW_SHOW);
		GetDlgItem(IDC_BUTTON5)->ShowWindow(SW_HIDE);
	}

	CDialogEx::OnTimer(nIDEvent);
}

void TestSettings::OnSize(UINT nType, int cx, int cy)
{
	CDialogEx::OnSize(nType, cx, cy);
}

afx_msg LRESULT TestSettings::OnChildWndResize(WPARAM wParam, LPARAM lParam)
{
	int width = int(wParam);

	HWND hwndChild = ::GetWindow(m_hWnd, GW_CHILD);
	while (hwndChild)
	{
		CRect rect;
		int ctl_id = ::GetDlgCtrlID(hwndChild);
		GetDlgItem(ctl_id)->GetWindowRect(rect);
		ScreenToClient(rect);

		POINT OldTLPoint = rect.TopLeft();
		POINT OldBRPoint = rect.BottomRight();

		POINT TLPoint, BRPoint;
		TLPoint = OldTLPoint;
		BRPoint.x = long(OldTLPoint.x + width);
		BRPoint.y = OldBRPoint.y;

		rect.SetRect(TLPoint, BRPoint);
		GetDlgItem(ctl_id)->MoveWindow(rect, TRUE);
		hwndChild = ::GetWindow(hwndChild, GW_HWNDNEXT);
	}
	return 0;
}

afx_msg LRESULT TestSettings::OnLoadPvpnConfig(WPARAM wParam, LPARAM lParam)
{
	ptc = (struct TestConfig*)lParam;
	int proxy_count = ptc->ProxyCount;
	for (int i = 0; i < proxy_count; i++)
		proxy_list.AddString(ptc->ProxyInfos[i].ProxyServer);
	if(proxy_count > 0) proxy_list.SetCurSel(0);

	int stun_count = ptc->StunCount;
	for (int i = 0; i < stun_count; i++)
		stun_list.AddString(ptc->StunInfos[i].StunName);
	if(stun_count > 0) stun_list.SetCurSel(0);

	StartPvpn();

	if (CheckPvpn())
	{
		GetDlgItem(IDC_BUTTON1)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_BUTTON5)->ShowWindow(SW_SHOW);
	}

	SetTimer(WM_CHECK_PVPN_PROC, 3000, NULL);
	return 0;
}

afx_msg LRESULT TestSettings::OnUpdateProxyStun(WPARAM wParam, LPARAM lParam)
{
	return 0;
}