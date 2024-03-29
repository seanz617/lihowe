
// MFCApplication1Dlg.cpp: 实现文件
//

#include "stdafx.h"
#include "MFCApplication1.h"
#include "MFCApplication1Dlg.h"
#include "afxdialogex.h"
#include <afxpriv.h>
#include <iostream>
#include "MyTool.h"

using namespace std;

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

void trace_log(CString log)
{
	CStdioFile f;
	BOOL flag = f.Open(_T("D:\\test.txt"), CFile::modeReadWrite);
	f.SeekToEnd();
	f.WriteString(log);
	f.Close();
}

UINT StopPlay(LPVOID pParam)
{
	if (NULL != pParam)
	{
		CMFCApplication1Dlg* wnd = (CMFCApplication1Dlg*)pParam;
		if (wnd->p_media_player != NULL)
		{
			libvlc_media_player_stop(wnd->p_media_player);
			libvlc_media_player_release(wnd->p_media_player);
			wnd->p_media_player = NULL;
		}
		wnd->SendMessage(WM_PLAY_STOPED, 0, NULL);
	}
	return 0;
}

class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_ABOUTBOX };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

// 实现
protected:
	DECLARE_MESSAGE_MAP()
public:
	virtual BOOL OnInitDialog();
};

CAboutDlg::CAboutDlg() : CDialogEx(IDD_ABOUTBOX)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)
END_MESSAGE_MAP()

BOOL CMFCApplication1Dlg::LoadConfig()
{
	STARTUPINFO si;
	PROCESS_INFORMATION pi;
	ZeroMemory(&si, sizeof(STARTUPINFO));
	si.cb = sizeof(STARTUPINFO);
	GetStartupInfo(&si);
	si.wShowWindow = SW_HIDE;
	si.dwFlags = STARTF_USESHOWWINDOW | STARTF_USESTDHANDLES;
	if (CreateProcess(_T("wget.exe"), _T("wget.exe https://vpn-test-data.oss-cn-shanghai.aliyuncs.com/config -O config"), NULL, NULL, TRUE, NULL, NULL, NULL, &si, &pi))
	{
		WaitForSingleObject(pi.hProcess, 15000);
		DWORD ret_code = 0;
		GetExitCodeProcess(pi.hProcess, &ret_code);
		if (ret_code != 0)
			AfxMessageBox(_T("download config file fail! use default config."));
	}
	
	CFileFind finder;
	DWORD pos = 0;
	CString strText = _T("");
	BOOL proxy_flag = FALSE;
	BOOL stun_flag = FALSE;
	BOOL video_flag = FALSE;

	BOOL file_found = finder.FindFile(_T("config"));
	CFileStatus fileStatus;
	ULONGLONG file_size = 0;
	if (file_found)
		if(CFile::GetStatus(_T("config"), fileStatus))
			file_size = fileStatus.m_size;

	if (file_found && file_size > 16)
	{		
		CStdioFile config_file;
		if (config_file.Open(_T("config"), CFile::modeRead))
		{
			config_file.Seek(pos, CFile::begin);
			while (config_file.ReadString(strText))
			{
				if (strText == _T("[proxy server]") && proxy_flag == FALSE)
				{
					proxy_flag = TRUE;
					video_flag = FALSE;
					stun_flag = FALSE;
					continue;
				}
				else if (strText == _T("[video address]") && video_flag == FALSE)
				{
					video_flag = TRUE;
					proxy_flag = FALSE;
					stun_flag = FALSE;
					continue;
				}
				else if (strText == _T("[stun server]") && stun_flag == FALSE)
				{
					stun_flag = TRUE;
					video_flag = FALSE;
					proxy_flag = FALSE;
					continue;
				}

				int index = strText.FindOneOf(_T("="));
				if (index < 0)
					continue;

				if (proxy_flag)
				{
					tc.ProxyInfos[tc.ProxyCount].ProxyServerStun = strText.Right(strText.GetLength() - index - 1).Trim();
					tc.ProxyInfos[tc.ProxyCount].ProxyServer = strText.Left(index).Trim();
					tc.ProxyCount++;
				}
				else if (video_flag)
				{
					tc.VideoInfos[tc.VideoCount].VideoName = strText.Left(index).Trim();
					tc.VideoInfos[tc.VideoCount].VideoAddress = strText.Right(strText.GetLength() - index - 1).Trim();
					tc.VideoCount++;
				}
				else if (stun_flag)
				{
					tc.StunInfos[tc.StunCount].StunName = strText.Left(index).Trim();
					tc.StunInfos[tc.StunCount].StunAddress = strText.Right(strText.GetLength() - index - 1).Trim();
					tc.StunCount++;
				}
			}
			config_file.Close();
		}
	}
	else
	{
		tc.StunCount = 2;
		tc.StunInfos[0].StunName = _T("stun0");
		tc.StunInfos[0].StunAddress = _T("47.98.242.12");
		tc.StunInfos[1].StunName = _T("stun1");
		tc.StunInfos[1].StunAddress = _T("121.40.156.57");

		tc.VideoCount = 4;
		tc.VideoInfos[0].VideoName = _T("oss flv 1");
		tc.VideoInfos[0].VideoAddress = _T("https://vpn-test-data.oss-cn-shanghai.aliyuncs.com/1.flv");
		tc.VideoInfos[1].VideoName = _T("oss flv 2");
		tc.VideoInfos[1].VideoAddress = _T("https://vpn-test-data.oss-cn-shanghai.aliyuncs.com/2.flv");
		tc.VideoInfos[2].VideoName = _T("oss mp4 1");
		tc.VideoInfos[2].VideoAddress = _T("https://vpn-test-data.oss-cn-shanghai.aliyuncs.com/3.mp4");
		tc.VideoInfos[3].VideoName = _T("oss mp4 2");
		tc.VideoInfos[4].VideoAddress = _T("https://vpn-test-data.oss-cn-shanghai.aliyuncs.com/4.mp4");
		
		tc.ProxyCount = 2;
		tc.ProxyInfos[0].ProxyServer = _T("192.168.0.1");
		tc.ProxyInfos[0].ProxyServerStun = _T("127.0.0.1");
		tc.ProxyInfos[1].ProxyServer = _T("192.168.0.2");
		tc.ProxyInfos[1].ProxyServerStun = _T("127.0.0.2");
	}

	return TRUE;
}

CMFCApplication1Dlg::CMFCApplication1Dlg(CWnd* pParent /*=nullptr*/)
	: CDialogEx(IDD_MFCAPPLICATION1_DIALOG, pParent)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CMFCApplication1Dlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_COMBO1, play_list);
	DDX_Control(pDX, IDC_SLIDER1, play_progress);
	DDX_Control(pDX, IDC_TAB1, info_tab);
}

BEGIN_MESSAGE_MAP(CMFCApplication1Dlg, CDialogEx)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_STN_CLICKED(IDC_SURFACE, &CMFCApplication1Dlg::OnStnClickedSurface)
	ON_BN_CLICKED(IDOK, &CMFCApplication1Dlg::OnBnClickedOk)
	ON_BN_CLICKED(IDCANCEL, &CMFCApplication1Dlg::OnBnClickedCancel)
	ON_WM_DESTROY()
	ON_BN_CLICKED(IDC_BUTTON2, &CMFCApplication1Dlg::OnBnClickedButton2)
	ON_BN_CLICKED(IDC_BUTTON4, &CMFCApplication1Dlg::OnBnClickedButton4)
	ON_BN_CLICKED(IDC_BUTTON3, &CMFCApplication1Dlg::OnBnClickedButton3)
	ON_NOTIFY(NM_CUSTOMDRAW, IDC_SLIDER1, &CMFCApplication1Dlg::OnNMCustomdrawSlider1)
	ON_WM_TIMER()
	ON_WM_CTLCOLOR()
	ON_WM_SIZE()
	ON_NOTIFY(TCN_SELCHANGE, IDC_TAB1, &CMFCApplication1Dlg::OnTcnSelchangeTab1)
	ON_MESSAGE(WM_USER_CHANGE_POS, &CMFCApplication1Dlg::OnUserChangePos)
	ON_MESSAGE(WM_PLAY_STOPED, &CMFCApplication1Dlg::OnPlayStoped)
	ON_CBN_SELCHANGE(IDC_COMBO1, &CMFCApplication1Dlg::OnCbnSelchangeCombo1)
	ON_MESSAGE(WM_PLAY_FIRST_FRAME, &CMFCApplication1Dlg::OnPlayFirstFrame)
	ON_MESSAGE(WM_RETRIED_STUN, &CMFCApplication1Dlg::OnRetriedStun)
	ON_MESSAGE(WM_UPDATE_PVPN_STATUS, &CMFCApplication1Dlg::OnUpdatePvpnStatus)
END_MESSAGE_MAP()

BOOL CMFCApplication1Dlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	pvpn_flag = FALSE;

	continue_flag = FALSE;
	auto_stop_flag = FALSE;
	last_play_url = -1;
	play_url = -1;

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != nullptr)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	SetIcon(m_hIcon, TRUE);
	SetIcon(m_hIcon, FALSE);

	if (!LoadConfig())
	{
		EndDialog(IDCANCEL);
		return FALSE;
	}
	
	const char* vlc_args[] = { "-I","dummy","-vvv" };
	p_instance = libvlc_new(sizeof(vlc_args) / sizeof(vlc_args[0]), vlc_args);
	p_player_mutex = CreateMutex(NULL, FALSE, NULL);

	m_brush.CreateSolidBrush(RGB(255, 255, 255));
	m_black_brush.CreateSolidBrush(RGB(0, 0, 0));

	for (int i = 0; i < tc.VideoCount; i++)
		play_list.AddString(CW2W(tc.VideoInfos[i].VideoName));
	play_list.SetCurSel(0);
	m_VideoPath = tc.VideoInfos[0].VideoAddress;

	play_progress.SetRange(0, 1000);
	play_progress.SetPageSize(1);
	play_progress.SetPos(0);

	CRect rect;
	GetDlgItem(IDOK)->GetWindowRect(&rect);
	start_btn_width = rect.right - rect.left;
	GetDlgItem(IDC_BUTTON2)->GetWindowRect(&rect);
	pause_btn_width = rect.right - rect.left;
	
	info_tab.InsertItem(0, _T("Report"));
	info_tab.InsertItem(1, _T("Pvpn"));
	info_tab.InsertItem(2, _T("Wget"));

	dlg_test_report.Create(IDD_DIALOG1, &info_tab);
	dlg_test_settings.Create(IDD_DIALOG2, &info_tab);
	dlg_test_wget.Create(IDD_DIALOG3, &info_tab);
	
	CRect rc;
	info_tab.GetClientRect(&rc);
	CRect rcTabItem;
	info_tab.GetItemRect(0, rcTabItem);
	rc.top += rcTabItem.Height() + 4;
	rc.left += 4;
	rc.bottom -= 4;
	rc.right = rc.right + 200;

	dlg_test_report.MoveWindow(&rc);
	dlg_test_settings.MoveWindow(&rc);
	dlg_test_wget.MoveWindow(&rc);

	dlg_test_report.ShowWindow(SW_SHOW);
	dlg_test_settings.ShowWindow(SW_HIDE);
	dlg_test_wget.ShowWindow(SW_HIDE);

	dlg_test_settings.parent_wnd = this;
	dlg_test_settings.SendMessage(WM_LOAD_PVPN_CONFIG,0,LPARAM(&tc));

	change_flag = TRUE;
	return TRUE;
}

void CMFCApplication1Dlg::update_play_progress()
{
	if (p_media_player != NULL)
	{
		WaitForSingleObject(p_player_mutex, INFINITE);
		float video_length = libvlc_media_player_get_length(p_media_player) + 1000;
		ReleaseMutex(p_player_mutex);

		video_length /= 1000.0;
		play_end_time = GetTickCount();
		struct report_data* rd = new struct report_data;
		rd->video_length = int(video_length);
		rd->play_length = int((play_end_time - play_start_time ) / 1000);
		dlg_test_report.SendMessage(WM_UPDATE_REPORT,0,LPARAM(rd));

		int slider_pos = play_progress.GetPos();

		float play_pos = 0.0;
		libvlc_state_t state = libvlc_Error;
		if (p_media_player != NULL)
		{
			play_pos = libvlc_media_player_get_position(p_media_player);
			state = libvlc_media_player_get_state(p_media_player);
		}

		if (state == libvlc_Playing)
		{
			slider_pos = (int)(play_pos * 1000);
			play_progress.SendMessage(WM_CHANGE_PLAY_POS, slider_pos, NULL);
		}
		if (state == libvlc_Ended)
		{
			last_play_url = play_url;
			CString vl = dlg_test_report.report.GetItemText(9, 0);
			CString pl = dlg_test_report.report.GetItemText(10, 0);
			int vli = vl.Find(_T(":"));
			int pli = pl.Find(_T(":"));
			int video_length = _ttoi(vl.Mid(vli + 1).Trim());
			int play_length = _ttoi(pl.Mid(pli + 1).Trim());

			if (pvpn_flag && video_length < 2 && play_length > video_length && last_play_url == play_url)
			{
				auto_stop_flag = TRUE;
				continue_flag = !continue_flag;
				if (continue_flag)
					dlg_test_settings.SendMessage(WM_RETRY_STUN, 0, NULL);
				else
				{
					auto_stop_flag = FALSE;
					continue_flag = FALSE;
				}
			}
			else
			{
				auto_stop_flag = FALSE;
			}
				
			OnBnClickedButton3();
		}
	}
}

void CMFCApplication1Dlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialogEx::OnSysCommand(nID, lParam);
	}
}

void CMFCApplication1Dlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this);

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CRect rect;
		GetDlgItem(IDC_SURFACE)->GetClientRect(&rect);
		FillRect(GetDlgItem(IDC_SURFACE)->GetDC()->GetSafeHdc(), &rect, CBrush(RGB(0, 0, 0)));
		CDialogEx::OnPaint();
	}
}

HCURSOR CMFCApplication1Dlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}

void CMFCApplication1Dlg::OnStnClickedSurface()
{
}

void CMFCApplication1Dlg::OnBnClickedOk()
{
	static int singleton = 0;
	if (singleton > 0)
		return;
	singleton = 1;

	auto_stop_flag = FALSE;

	int nIndex = play_list.GetCurSel();
	play_url = nIndex;
	if (last_play_url != play_url)
		continue_flag = FALSE;

	m_VideoPath = tc.VideoInfos[nIndex].VideoAddress;
	CW2A ascii(m_VideoPath, CP_UTF8);
	
	play_progress.SendMessage(WM_CHANGE_PLAY_POS, 0, NULL);

	if (p_instance != NULL)
	{
		p_media = NULL; p_media_player = NULL;

		if (m_VideoPath.Find(_T("http")) == -1)
			p_media = libvlc_media_new_path(p_instance, ascii.m_psz);
		else
		{
			if (dlg_test_settings.CheckPvpn())
			{
				char play_url_with_proxy[2048];
				memset(play_url_with_proxy, 0, 2048);
				char* play_address_base64 = (char*)Base64Encode(ascii.m_psz, strlen(ascii.m_psz));
				sprintf_s(play_url_with_proxy, "http://127.0.0.1:18071/proxy/%s", play_address_base64);
				p_media = libvlc_media_new_location(p_instance, play_url_with_proxy);
			}
			else
				p_media = libvlc_media_new_location(p_instance, ascii.m_psz);	
		}
			
		if (p_media != NULL)
		{
			libvlc_media_add_option(p_media, "--network-caching=300");
			p_media_player = libvlc_media_player_new_from_media(p_media);
			if (p_media_player != NULL)
			{
				libvlc_media_parse(p_media);
				libvlc_media_player_set_media(p_media_player, p_media);
				libvlc_media_release(p_media);

				HWND hwnd = GetDlgItem(IDC_SURFACE)->GetSafeHwnd();
				libvlc_media_player_set_hwnd(p_media_player, hwnd);
				libvlc_media_player_play(p_media_player);
				SetTimer(WM_PLAY_FIRST_FRAME, 100, 0);
			}
		}
	}

	if (p_instance != NULL && p_media_player != NULL)
	{
		play_start_time = GetTickCount();
		play_end_time = play_start_time;
		dlg_test_report.SendMessage(WM_SET_PLAY_FIRST_FRAME, 0, NULL);

		GetDlgItem(IDOK)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_BUTTON3)->ShowWindow(SW_SHOW);
		GetDlgItem(IDC_BUTTON4)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_BUTTON2)->ShowWindow(SW_SHOW);
		stop_timer = FALSE;
		SetTimer(WM_PLAY_POS_CHANGED,1000,0);
	}

	singleton = 0;
}

void CMFCApplication1Dlg::OnEndReached(const libvlc_event_t* p_event, void* p_data)
{
	last_play_url = play_url;
	CString vl = dlg_test_report.report.GetItemText(9, 0);
	CString pl = dlg_test_report.report.GetItemText(10, 0);
	int vli = vl.Find(_T(":"));
	int pli = pl.Find(_T(":"));
	int video_length = _ttoi(vl.Mid(vli + 1).Trim());
	int play_length = _ttoi(pl.Mid(pli + 1).Trim());

	if (pvpn_flag && video_length < 2 && play_length > video_length && last_play_url == play_url)
	{
		auto_stop_flag = TRUE;
		continue_flag = !continue_flag;
		if(continue_flag)
			dlg_test_settings.SendMessage(WM_RETRY_STUN, 0, NULL);
	}
	else
	{
		auto_stop_flag = FALSE;
	}
		
	OnBnClickedButton3();
}

void CMFCApplication1Dlg::OnBnClickedCancel()
{
	KillTimer(WM_PLAY_POS_CHANGED);
	stop_timer = TRUE;

	auto_stop_flag = FALSE;
	continue_flag = FALSE;

	AfxBeginThread(StopPlay, this, THREAD_PRIORITY_NORMAL, 0, 0, NULL);

	DWORD pid = -1;
	for (int i = 0; i < 6; i++)
	{
		pid = CheckProc(_T("wget.exe"));
		if (pid > 0)
		{
			HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
			if (hProcess != NULL)
			{
				TerminateProcess(hProcess, 0);
				::CloseHandle(hProcess);
			}
		}
		else
			break;
		Sleep(100);
	}
	
	for (int i = 0; i < 6; i++)
	{
		pid = CheckProc(_T("speedtest.exe"));
		if (pid > 0)
		{
			HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
			if (hProcess != NULL)
			{
				TerminateProcess(hProcess, 0);
				::CloseHandle(hProcess);
			}
		}
		else
			break;
		Sleep(100);
	}
	
	/*
	if (p_instance != NULL)
	{
		libvlc_release(p_instance);
		p_instance = NULL;
	}
	*/

	CDialogEx::OnCancel();
}

void CMFCApplication1Dlg::OnDestroy()
{
	CDialogEx::OnDestroy();
}

void CMFCApplication1Dlg::OnBnClickedButton2()
{
	libvlc_state_t state = libvlc_Error;
	if (p_media_player != NULL && libvlc_media_player_is_playing(p_media_player))
	{
		libvlc_media_player_pause(p_media_player);
		Sleep(300);
		state = libvlc_media_player_get_state(p_media_player);
	}

	if (state == libvlc_Paused)
	{
		GetDlgItem(IDC_BUTTON2)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_BUTTON4)->ShowWindow(SW_SHOW);
	}
}

void CMFCApplication1Dlg::OnBnClickedButton4()
{
	libvlc_state_t state = libvlc_Error;
	if (p_media_player != NULL && libvlc_media_player_can_pause(p_media_player))
	{
		libvlc_media_player_pause(p_media_player);
		Sleep(300);
		state = libvlc_media_player_get_state(p_media_player);
	}

	if (state == libvlc_Playing)
	{
		GetDlgItem(IDC_BUTTON4)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_BUTTON2)->ShowWindow(SW_SHOW);
	}
}

void CMFCApplication1Dlg::OnBnClickedButton3()
{
	static int stop_play = 0;
	if (stop_play > 0)
		return;
	stop_play = 1;

	KillTimer(WM_PLAY_POS_CHANGED);
	stop_timer = TRUE;

	KillTimer(WM_PLAY_FIRST_FRAME);

	play_end_time = GetTickCount();
	struct report_data* rd = new struct report_data;
	rd->video_length = -1;
	rd->play_length = int((play_end_time - play_start_time) / 1000);
	dlg_test_report.SendMessage(WM_UPDATE_REPORT, 0, LPARAM(rd));

	play_progress.SendMessage(WM_CHANGE_PLAY_POS, 0, NULL);

	AfxBeginThread(StopPlay, this, THREAD_PRIORITY_NORMAL, 0, 0, NULL);

	/*
	if (p_instance != NULL)
	{
		libvlc_release(p_instance);
		trace_log(_T("444444\r\n"));
		p_instance = NULL;
	}

	Sleep(100);
	*/
	
	stop_play = 0;
}

void CMFCApplication1Dlg::OnNMCustomdrawSlider1(NMHDR *pNMHDR, LRESULT *pResult)
{
	LPNMCUSTOMDRAW pNMCD = reinterpret_cast<LPNMCUSTOMDRAW>(pNMHDR);
	*pResult = 0;
}

void CMFCApplication1Dlg::OnTimer(UINT_PTR nIDEvent)
{
	switch (nIDEvent)
	{
	case WM_PLAY_POS_CHANGED:
		if (stop_timer == TRUE)
			return;
		update_play_progress();
		break;
	case WM_PLAY_FIRST_FRAME:
		OnPlayFirstFrame(0, NULL);
		break;
	default:break;
	}

	CDialogEx::OnTimer(nIDEvent);
}

HBRUSH CMFCApplication1Dlg::OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor)
{
	HBRUSH hbr = CDialogEx::OnCtlColor(pDC, pWnd, nCtlColor);

	if (nCtlColor == IDC_SURFACE)
		return (HBRUSH)m_black_brush.GetSafeHandle();
	else
		return (HBRUSH)m_brush.GetSafeHandle();

	return hbr;
}

void CMFCApplication1Dlg::OnSize(UINT nType, int cx, int cy)
{
	CDialogEx::OnSize(nType, cx, cy);
	if (nType == SIZE_MAXIMIZED)
	{
		ReSize(IDC_COMBO1,0.8);
		ReSize(IDOK,0.8);
		ReSize(IDC_BUTTON3,0.8);

		ReSize(IDC_BUTTON2, 0.8);
		ReSize(IDC_BUTTON4, 0.8);
		ReSize(IDC_SLIDER1, 0.8);

		ReSize(IDC_SURFACE, 0.8);
		
		ReSize(IDC_TAB1, 0.8);

		ReSizeChild(0.8);
	}
	else if (nType == SIZE_RESTORED)
	{
		ReSize(IDC_COMBO1, 0.7);
		ReSize(IDOK, 0.7);
		ReSize(IDC_BUTTON3, 0.7);

		ReSize(IDC_BUTTON2, 0.7);
		ReSize(IDC_BUTTON4, 0.7);
		ReSize(IDC_SLIDER1, 0.7);

		ReSize(IDC_SURFACE, 0.7);

		ReSize(IDC_TAB1, 0.7);

		ReSizeChild(0.7);
	}
}

void CMFCApplication1Dlg::ReSizeChild(float ban)
{
	if (change_flag)
	{
		CRect rect;
		::GetWindowRect(m_hWnd, &rect);
		ScreenToClient(rect);
		LONG dlg_width = LONG((rect.right - rect.left) * (1 - ban)) - 40;
		dlg_test_settings.SendMessage(WM_CHILD_WND_RESIZE, dlg_width, NULL);
		dlg_test_report.SendMessage(WM_CHILD_WND_RESIZE, dlg_width, NULL);
		dlg_test_wget.SendMessage(WM_CHILD_WND_RESIZE, dlg_width, NULL);
	}
}

void CMFCApplication1Dlg::ReSize(int nID,float ban)
{
	if (change_flag == FALSE)
		return;

	CRect rect;
	::GetWindowRect(m_hWnd, &rect);
	ScreenToClient(rect);
	LONG dlg_width = rect.right - rect.left;
	LONG dlg_height = rect.bottom - rect.top;

	GetDlgItem(nID)->GetWindowRect(&rect);
	ScreenToClient(rect);

	CPoint OldTLPoint, TLPoint;
	OldTLPoint = rect.TopLeft();

	CPoint OldBRPoint, BRPoint; 
	OldBRPoint = rect.BottomRight();

	switch (nID) {
	case IDC_COMBO1:
		TLPoint = OldTLPoint;
		BRPoint.x = long(ban * dlg_width - start_btn_width - 5);
		BRPoint.y = OldBRPoint.y;
		break;
	case IDOK:
	case IDC_BUTTON3:
		TLPoint.x = long(ban * dlg_width - start_btn_width);
		TLPoint.y = OldTLPoint.y;
		BRPoint.x = long(ban * dlg_width);
		BRPoint.y = long(OldBRPoint.y);
		break;
	case IDC_SLIDER1:
		TLPoint.x = long(pause_btn_width + 5);
		TLPoint.y = OldTLPoint.y;
		BRPoint.x = long(ban * dlg_width);
		BRPoint.y = long(OldBRPoint.y);
		break;
	case IDC_SURFACE:
		TLPoint = OldTLPoint;
		BRPoint.x = long(ban * dlg_width);
		BRPoint.y = long(dlg_height - 67);
		break;
	case IDC_BUTTON2:
	case IDC_BUTTON4:
		TLPoint = OldTLPoint;
		BRPoint = OldBRPoint;
		break;
	case IDC_TAB1:
		TLPoint.x = long(ban * dlg_width) + 5;
		TLPoint.y = OldTLPoint.y;
		BRPoint.x = long(dlg_width - 5);
		BRPoint.y = long(OldTLPoint.y + dlg_height);
		rect.SetRect(TLPoint, BRPoint);
		break;
	default:
		break;
	}
	rect.SetRect(TLPoint, BRPoint);
	GetDlgItem(nID)->MoveWindow(rect, TRUE);
}

BOOL CAboutDlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();
	return TRUE;
}

void CMFCApplication1Dlg::OnTcnSelchangeTab1(NMHDR *pNMHDR, LRESULT *pResult)
{
	switch (info_tab.GetCurSel())
	{
	case 0:
		dlg_test_report.ShowWindow(SW_SHOW);
		dlg_test_settings.ShowWindow(SW_HIDE);
		dlg_test_wget.ShowWindow(SW_HIDE);
		dlg_test_report.SetFocus();
		break;
	case 1:
		dlg_test_report.ShowWindow(SW_HIDE);
		dlg_test_settings.ShowWindow(SW_SHOW);
		dlg_test_wget.ShowWindow(SW_HIDE);
		dlg_test_settings.SetFocus();
		break;
	case 2:
		dlg_test_report.ShowWindow(SW_HIDE);
		dlg_test_settings.ShowWindow(SW_HIDE);
		dlg_test_wget.ShowWindow(SW_SHOW);
		dlg_test_wget.SetFocus();
		break;
	default:
		break;
	}
	*pResult = 0;
}

afx_msg LRESULT CMFCApplication1Dlg::OnUserChangePos(WPARAM wParam, LPARAM lParam)
{
	if (p_media_player != NULL)
	{
		libvlc_state_t state = libvlc_media_player_get_state(p_media_player);
		if (p_media_player != NULL && state == libvlc_Playing)
			libvlc_media_player_set_position(p_media_player, (double)(wParam / 1000.0));
	}
	play_progress.user_flag = FALSE;
	return 0;
}

//>wget -q -O - "http://myexternalip.com/raw"
//wget -q -O - "http://ip-api.com/json/116.231.144.251"

afx_msg LRESULT CMFCApplication1Dlg::OnPlayStoped(WPARAM wParam, LPARAM lParam)
{
	if (!pvpn_flag)
	{
		auto_stop_flag = FALSE;

		GetDlgItem(IDOK)->ShowWindow(SW_SHOW);
		GetDlgItem(IDC_BUTTON2)->ShowWindow(SW_SHOW);
		GetDlgItem(IDC_BUTTON3)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_BUTTON4)->ShowWindow(SW_HIDE);
		return 0;
	}
	if ((!auto_stop_flag) || (!continue_flag))
	{
		auto_stop_flag = FALSE;

		GetDlgItem(IDOK)->ShowWindow(SW_SHOW);
		GetDlgItem(IDC_BUTTON2)->ShowWindow(SW_SHOW);
		GetDlgItem(IDC_BUTTON3)->ShowWindow(SW_HIDE);
		GetDlgItem(IDC_BUTTON4)->ShowWindow(SW_HIDE);
	}

	return 0;
}

void CMFCApplication1Dlg::OnCbnSelchangeCombo1()
{
	int nIndex = play_list.GetCurSel();
	m_VideoPath = tc.VideoInfos[nIndex].VideoAddress;
	dlg_test_wget.current_address = m_VideoPath;
}

afx_msg LRESULT CMFCApplication1Dlg::OnPlayFirstFrame(WPARAM wParam, LPARAM lParam)
{
	libvlc_state_t state = libvlc_Error;
	if (p_media_player != NULL && libvlc_media_player_is_playing(p_media_player))
	{
		KillTimer(WM_PLAY_FIRST_FRAME);
		LONG play_first_frame = GetTickCount();
		dlg_test_report.SendMessage(WM_SET_PLAY_FIRST_FRAME, play_first_frame - play_start_time, NULL);
	}
	return 0;
}

afx_msg LRESULT CMFCApplication1Dlg::OnRetriedStun(WPARAM wParam, LPARAM lParam)
{
	if (pvpn_flag && auto_stop_flag && continue_flag && last_play_url == play_url && GetDlgItem(IDC_BUTTON3)->IsWindowVisible())
	{
		auto_stop_flag = FALSE;
		OnBnClickedOk();
	}
	else
	{
		auto_stop_flag = FALSE;
		OnBnClickedButton3();
	}

	return 0;
}

afx_msg LRESULT CMFCApplication1Dlg::OnUpdatePvpnStatus(WPARAM wParam, LPARAM lParam)
{
	pvpn_flag = (BOOL)wParam;
	if (pvpn_flag)
		dlg_test_report.report.SetItemText(2, 0, _T("is vpn : true"));
	else
		dlg_test_report.report.SetItemText(2, 0, _T("is vpn : false"));
	return 0;
}
