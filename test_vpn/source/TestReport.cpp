// TestReport.cpp: 实现文件
//

#include "stdafx.h"
#include "MFCApplication1.h"
#include "TestReport.h"
#include "afxdialogex.h"
#include "MyTool.h"

/*
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
*/

//CString get_ip_url[2] = { _T("http://ipinfo.io/ip"), _T("http://whatismyip.akamai.com/")};

UINT GetCityAndISP(LPVOID pParam)
{
	if (pParam != NULL)
	{
		TestReport* ptr = (TestReport*)pParam;
		
		ptr->city = _T("");

		HttpHandler httpHandler;
		//CString external_ip = _T("ip unknown"), city = _T("city unknown"), isp = _T("isp unknown");
		CString city = _T(""), isp = _T("");

		/*
		for (int i = 0; i < get_ip_url->GetLength(); i++)
		{
			httpHandler.GetExternalIP(external_ip, get_ip_url[i]);
			if (external_ip.GetLength() > 2)
				break;
		}

		*/
		
		if (ptr->ip.GetLength() > 2)
		{
			httpHandler.GetCityAndIsp(ptr->ip, city, isp);
			if (city.GetLength() > 0)
			{
				ptr->city = city;
				ptr->SendMessage(WM_UPDATE_CITY_ISP, NULL);
			}
		}
	}
	return 0;
}

IMPLEMENT_DYNAMIC(TestReport, CDialogEx)

TestReport::TestReport(CWnd* pParent /*=nullptr*/) : CDialogEx(IDD_DIALOG1, pParent)
{
	latency = 0.0f;
	download_bandwidth = 0.0f;
	upload_bandwidth = 0.0f;
	packet_loss = 0.0f;
	isVpn = _T("");
	isp = _T("");
	ip = _T("");
	city = _T("");
}

TestReport::~TestReport()
{
}

void TestReport::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_LIST1, report);
	DDX_Control(pDX, IDC_COMBO1, play_result);
	DDX_Control(pDX, IDC_COMBO2, play_result_screen);
	DDX_Control(pDX, IDC_COMBO3, play_result_finish);
}

BEGIN_MESSAGE_MAP(TestReport, CDialogEx)
	ON_MESSAGE(WM_UPDATE_REPORT, &TestReport::OnUpdateReport)
	ON_MESSAGE(WM_UPDATE_CITY_ISP, &TestReport::OnUpdateCityIsp)
	ON_MESSAGE(WM_UPDATE_SPEED_TEST, &TestReport::OnUpdateSpeedTest)
	ON_MESSAGE(WM_CHILD_WND_RESIZE, &TestReport::OnChildWndResize)
	ON_WM_CTLCOLOR()
	ON_WM_SIZE()
	ON_MESSAGE(WM_SET_PLAY_FIRST_FRAME, &TestReport::OnSetPlayFirstFrame)
END_MESSAGE_MAP()

afx_msg LRESULT TestReport::OnUpdateReport(WPARAM wParam, LPARAM lParam)
{
	if (lParam != NULL) {
		struct report_data* rd = (report_data*)lParam;
		CString line;

		if (rd->video_length >= 0)
		{
			line.Format(_T("video length : %d"), rd->video_length);
			report.SetItemText(9, 0, line);
		}

		if (rd->play_length >= 0)
		{
			line.Format(_T("play length : %d"), rd->play_length);
			report.SetItemText(10, 0, line);
		}

		delete rd; rd = NULL;
	}
	return 0;
}

BOOL TestReport::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	m_brush.CreateSolidBrush(RGB(255, 255, 255));

	report.SetColumnWidth(0, 400);
	report.InsertItem(0, _T("ip ..."));
	report.SetColumnWidth(1, 400);
	report.InsertItem(1, _T("isp ..."));
	report.SetColumnWidth(2, 400);
	report.InsertItem(2, _T("is vpn ..."));
	report.SetColumnWidth(3, 400);
	report.InsertItem(3, _T("location ..."));
	report.SetColumnWidth(4, 400);
	report.InsertItem(4, _T("latency ..."));
	report.SetColumnWidth(5, 400);
	report.InsertItem(5, _T("download bandwidth ..."));
	report.SetColumnWidth(6, 400);
	report.InsertItem(6, _T("upload bandwidth ..."));
	report.SetColumnWidth(7, 400);
	report.InsertItem(7, _T("packet loss ..."));
	report.InsertItem(8, _T(""));
	report.SetColumnWidth(9, 400);
	report.InsertItem(9, _T("video length : 0"));
	report.SetColumnWidth(10, 400);
	report.InsertItem(10, _T("play length : 0"));
	report.InsertItem(11, _T("play first frame : 0"));

	play_result_finish.AddString(_T("播放完成"));
	play_result_finish.AddString(_T("中途停止播放"));
	play_result_finish.SetCurSel(0);

	play_result.AddString(_T("流畅"));
	play_result.AddString(_T("轻微卡顿"));
	play_result.AddString(_T("严重卡顿"));
	play_result.SetCurSel(0);

	play_result_screen.AddString(_T("无花屏"));
	play_result_screen.AddString(_T("轻微花屏"));
	play_result_screen.AddString(_T("严重花屏"));
	play_result_screen.SetCurSel(0);

#ifndef DEBUG
	sh_speed_test.Run(_T("speedtest.exe"), _T("speedtest.exe --accept-license --format=json"), this, WM_UPDATE_SPEED_TEST);
#endif

	return TRUE;
}

afx_msg LRESULT TestReport::OnUpdateCityIsp(WPARAM wParam, LPARAM lParam)
{
	report.SetItemText(3, 0, _T("location : ") + city);
	return 0;
}

afx_msg LRESULT TestReport::OnUpdateSpeedTest(WPARAM wParam, LPARAM lParam)
{
	CStringArray sa;
	if (sh_speed_test.ret_code == 0)
	{
		SplitStr(sh_speed_test.output, _T(","), sa);

		for (int i = 0; i < sa.GetSize(); i++)
		{
			CString tmp = sa.GetAt(i);
			tmp.Trim(_T("{"));
			tmp.Trim(_T("}"));
			tmp.Replace(_T("\""), _T(""));

			int latency_index = tmp.Find(_T("latency:"));
			int download_index = tmp.Find(_T("download:{bandwidth:"));
			int upload_index = tmp.Find(_T("upload:{bandwidth:"));
			int packetLoss_index = tmp.Find(_T("packetLoss:"));
			int isp_index = tmp.Find(_T("isp:"));
			int isVpn_index = tmp.Find(_T("isVpn:"));
			int externalIp_index = tmp.Find(_T("externalIp:"));

			CString value;
			if (latency_index >= 0)
			{
				value = tmp.Right(tmp.GetLength() - latency_index - 8);
				latency = _ttof(value);
				value.Format(_T("latency : %.fms"), latency);
				report.SetItemText(4, 0, value);
			}
			else if (download_index >= 0)
			{
				value = tmp.Right(tmp.GetLength() - download_index - 20);
				download_bandwidth = float(_ttol(value) / 1024 / 1024);
				value.Format(_T("download bandwidth : %.1fMB/s"), download_bandwidth);
				report.SetItemText(5, 0, value);
			}
			else if (upload_index >= 0)
			{
				value = tmp.Right(tmp.GetLength() - upload_index - 18);
				upload_bandwidth = float(_ttol(value) / 1024 / 1024);
				value.Format(_T("upload bandwidth : %.1fMB/s"), upload_bandwidth);
				report.SetItemText(6, 0, value);
			}
			else if (packetLoss_index >= 0)
			{
				value = tmp.Right(tmp.GetLength() - packetLoss_index - 11);
				packet_loss = _ttof(value);
				value.Format(_T("packet loss : %.1f"),packet_loss);
				report.SetItemText(7, 0, value);
			}
			else if (isp_index >= 0)
			{
				value = tmp.Right(tmp.GetLength() - isp_index - 4);
				isp = value;
				report.SetItemText(1, 0, _T("isp : ") + value);
			}
			else if (externalIp_index >= 0)
			{
				ip = tmp.Right(tmp.GetLength() - externalIp_index - 11);
				report.SetItemText(0, 0, _T("ip : ") + ip);
				CWinThread* get_city_isp_thread = AfxBeginThread(GetCityAndISP, this, THREAD_PRIORITY_NORMAL, 0, 0, NULL);
			}
			else if (isVpn_index >= 0)
			{
				isVpn = tmp.Right(tmp.GetLength() - isVpn_index - 6);
				report.SetItemText(2, 0, _T("is vpn : ") + isVpn);
			}
		}
	}
	else
	{
		report.SetItemText(0, 0, _T("ip : error"));
		report.SetItemText(1, 0, _T("isp : error"));
		report.SetItemText(2, 0, _T("is vpn : error"));
		report.SetItemText(3, 0, _T("location : error"));
		report.SetItemText(4, 0, _T("latency : error"));
		report.SetItemText(5, 0, _T("download bandwidth : error"));
		report.SetItemText(6, 0, _T("upload bandwidth : error"));
		report.SetItemText(7, 0, _T("package loss : error"));
	}
	return 0;
}

afx_msg LRESULT TestReport::OnChildWndResize(WPARAM wParam, LPARAM lParam)
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

HBRUSH TestReport::OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor)
{
	HBRUSH hbr = CDialogEx::OnCtlColor(pDC, pWnd, nCtlColor);
	return (HBRUSH)m_brush.GetSafeHandle();
}

void TestReport::OnSize(UINT nType, int cx, int cy)
{
	CDialogEx::OnSize(nType, cx, cy);
}

afx_msg LRESULT TestReport::OnSetPlayFirstFrame(WPARAM wParam, LPARAM lParam)
{
	CString tmp;
	tmp.Format(_T("play first frame : %dms"), LONG(wParam));
	report.SetItemText(11, 0, tmp);
	return 0;
}