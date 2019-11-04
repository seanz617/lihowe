// TestReport.cpp: 实现文件
//

#include "stdafx.h"
#include "MFCApplication1.h"
#include "TestReport.h"
#include "afxdialogex.h"

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

CString get_ip_url[2] = { _T("http://ipinfo.io/ip"), _T("http://whatismyip.akamai.com/")};

UINT GetCityAndISP(LPVOID pParam)
{
	if (pParam != NULL)
	{
		TestReport* ptr = (TestReport*)pParam;
		
		ptr->city = _T("");
		ptr->isp = _T("");
		ptr->ip = _T("");

		HttpHandler httpHandler;
		CString external_ip = _T("ip unknown"), city = _T("city unknown"), isp = _T("isp unknown");
		
		for (int i = 0; i < get_ip_url->GetLength(); i++)
		{
			httpHandler.GetExternalIP(external_ip, get_ip_url[i]);
			if (external_ip.GetLength() > 2)
				break;
		}
		
		if (external_ip.GetLength() > 2)
			httpHandler.GetCityAndIsp(external_ip, city, isp);
		else
			external_ip = _T("ip unknown");

		ptr->city = city;
		ptr->isp = isp;
		ptr->ip = external_ip;
		
		ptr->SendMessage(WM_UPDATE_CITY_ISP, NULL);
	}
	return 0;
}

IMPLEMENT_DYNAMIC(TestReport, CDialogEx)

TestReport::TestReport(CWnd* pParent /*=nullptr*/) : CDialogEx(IDD_DIALOG1, pParent)
{
}

TestReport::~TestReport()
{
}

void TestReport::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_LIST1, report);
}

BEGIN_MESSAGE_MAP(TestReport, CDialogEx)
	ON_MESSAGE(WM_UPDATE_REPORT, &TestReport::OnUpdateReport)
	ON_MESSAGE(WM_UPDATE_CITY_ISP, &TestReport::OnUpdateCityIsp)
	ON_MESSAGE(WM_UPDATE_SPEED_TEST, &TestReport::OnUpdateSpeedTest)
	ON_MESSAGE(WM_CHILD_WND_RESIZE, &TestReport::OnChildWndResize)
	ON_WM_CTLCOLOR()
	ON_WM_SIZE()
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
	report.InsertItem(1, _T("city ..."));
	report.SetColumnWidth(2, 400);
	report.InsertItem(2, _T("isp ..."));

	report.InsertItem(3, _T(""));

	report.SetColumnWidth(4, 400);
	report.InsertItem(4, _T("Latency ..."));
	report.SetColumnWidth(5, 400);
	report.InsertItem(5, _T("Upload Bandwidth ..."));
	report.SetColumnWidth(6, 400);
	report.InsertItem(6, _T("Download Bandwidth ..."));
	report.SetColumnWidth(7, 400);
	report.InsertItem(7, _T("Package Loss ..."));

	report.InsertItem(8, _T(""));

	report.SetColumnWidth(9, 400);
	report.InsertItem(9, _T("video length : 0"));
	report.SetColumnWidth(10, 400);
	report.InsertItem(10, _T("play length : 0"));

	CWinThread* get_city_isp_thread = AfxBeginThread(GetCityAndISP, this, THREAD_PRIORITY_NORMAL, 0, 0, NULL);

	sh_speed_test.Run(_T("speedtest.exe"), _T("speedtest.exe"), this, WM_UPDATE_SPEED_TEST);

	return TRUE;
}

afx_msg LRESULT TestReport::OnUpdateCityIsp(WPARAM wParam, LPARAM lParam)
{
	report.SetItemText(0, 0, ip);
	report.SetItemText(1, 0, city);
	report.SetItemText(2, 0, isp);
	return 0;
}


afx_msg LRESULT TestReport::OnUpdateSpeedTest(WPARAM wParam, LPARAM lParam)
{
	CStringArray sa;
	SplitStr(sh_speed_test.output,_T("\r\n"),sa);
	for (int i = 0; i < sa.GetSize(); i++)
	{
		CString tmp = sa.GetAt(i);
		int index = tmp.Find(_T("("));
		if (index > 0)
			tmp = tmp.Left(index);

		if (tmp.Find(_T("Latency:")) >= 0)
			report.SetItemText(4, 0, tmp.Trim());
		else if (tmp.Find(_T("Upload:")) >= 0)
			report.SetItemText(5, 0, tmp.Trim());
		else if (tmp.Find(_T("Download:")) >= 0)
			report.SetItemText(6, 0, tmp.Trim());
		else if (tmp.Find(_T("Packet Loss:")) >= 0)
			report.SetItemText(7, 0, tmp.Trim());
	}
	return 0;
}

afx_msg LRESULT TestReport::OnChildWndResize(WPARAM wParam, LPARAM lParam)
{
	int width = int(wParam) - 40;
	
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
