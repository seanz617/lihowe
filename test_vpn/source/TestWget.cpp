// TestWget.cpp: 实现文件
//

#include "stdafx.h"
#include "MFCApplication1.h"
#include "TestWget.h"
#include "afxdialogex.h"
#include "MyTool.h"

IMPLEMENT_DYNAMIC(TestWget, CDialogEx)

BOOL TestWget::CheckWget()
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
		if (exe_name == _T("wget\.exe"))
		{
			wget_pid = pe.th32ProcessID;
			wget_parent_pid = pe.th32ParentProcessID;

			found_flag = TRUE;
			break;
		}
	} while (Process32Next(hSnapshot, &pe));
	CloseHandle(hSnapshot);
	return found_flag;
}

TestWget::TestWget(CWnd* pParent /*=nullptr*/)
	: CDialogEx(IDD_DIALOG3, pParent)
{
	current_address = _T("");
}

TestWget::~TestWget()
{
}

void TestWget::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_PROGRESS1, progress);
	DDX_Control(pDX, IDC_BUTTON1, info_text);
	DDX_Control(pDX, IDC_EDIT1, wget_result);
	DDX_Control(pDX, IDC_COMBO1, connect_type);
}

BEGIN_MESSAGE_MAP(TestWget, CDialogEx)
	ON_MESSAGE(WM_CHILD_WND_RESIZE, &TestWget::OnChildWndResize)
	ON_BN_CLICKED(IDC_BUTTON1, &TestWget::OnBnClickedButton1)
	ON_MESSAGE(WM_WGET_STATUS, &TestWget::OnWgetStatus)
	ON_BN_CLICKED(IDC_BUTTON2, &TestWget::OnBnClickedButton2)
	ON_WM_CTLCOLOR()
END_MESSAGE_MAP()

afx_msg LRESULT TestWget::OnChildWndResize(WPARAM wParam, LPARAM lParam)
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

BOOL TestWget::OnInitDialog()
{
	CDialogEx::OnInitDialog();
	m_brush.CreateSolidBrush(RGB(255, 255, 255));
	connect_type.AddString(_T("direct"));
	connect_type.AddString(_T("vpn"));
	connect_type.SetCurSel(0);
	return TRUE;
}

void TestWget::OnBnClickedButton1()
{
	sh.wget = TRUE;
	if (current_address.Find(_T("http")) >= 0)
	{
		CString url = current_address;
		int ct_index = connect_type.GetCurSel();
		if (ct_index == 1)
		{
			CW2A ascii(current_address, CP_UTF8);
			
			char wget_url_with_proxy[2048];
			memset(wget_url_with_proxy, 0, 2048);
			char* wget_address_base64 = (char*)Base64Encode(ascii.m_psz, strlen(ascii.m_psz));
			CString strData = CA2T(wget_address_base64);
			url.Format(_T("http://127.0.0.1:18071/proxy/%s"), strData);
		}

		sh.Run(_T("wget.exe"), _T("wget.exe " + url), this, WM_WGET_STATUS);
		GetDlgItem(IDC_BUTTON1)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_BUTTON2)->ShowWindow(SW_SHOW);
		wget_result.SetWindowText(_T(""));
	}
}

afx_msg LRESULT TestWget::OnWgetStatus(WPARAM wParam, LPARAM lParam)
{
	if(wParam >= 0 && wParam <= 100)
		progress.SetPos(wParam);
	if (wParam == 100)
	{
		progress.SetPos(wParam);
		if (sh.ret_code != 0)
			wget_result.SetWindowText(sh.output);
		else
		{
			CStringArray sa;
			SplitStr(sh.output, _T("\r\n"), sa);
			CString line = sa.GetAt(sa.GetSize() - 1);
			int speed_index_start = line.Find(_T("("));
			int speed_index_end = line.Find(_T(")"));
			int size_index_start = line.Find(_T("["));
			int size_index_end = line.Find(_T("]"));
			CString speed, size;
			if (speed_index_start >= 0 && speed_index_end >= 0 && speed_index_end > speed_index_start)
				speed = line.Mid(speed_index_start + 1, speed_index_end - speed_index_start - 1);
			if (size_index_start >= 0 && size_index_end >= 0 && size_index_end > size_index_start)
				size = line.Mid(size_index_start + 1, size_index_end - size_index_start - 1);
			wget_result.SetWindowText(_T("avg download speed : "+speed+_T("\r\ndownload/file size : ")+size));
		}
		GetDlgItem(IDC_BUTTON2)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_BUTTON1)->ShowWindow(SW_SHOW);
	}
	return 0;
}

void TestWget::OnBnClickedButton2()
{
	if (sh.run_flag)
	{
		sh.run_flag = FALSE;
		for (int i = 0; i < 6; i++)
		{
			if (CheckWget())
			{
				HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, wget_pid);
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
	if (!CheckWget())
	{
		GetDlgItem(IDC_BUTTON2)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_BUTTON1)->ShowWindow(SW_SHOW);
	}
}

HBRUSH TestWget::OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor)
{
	HBRUSH hbr = CDialogEx::OnCtlColor(pDC, pWnd, nCtlColor);
	return (HBRUSH)m_brush.GetSafeHandle();
}
