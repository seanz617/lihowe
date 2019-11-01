// TestReport.cpp: 实现文件
//

#include "stdafx.h"
#include "MFCApplication1.h"
#include "TestReport.h"
#include "afxdialogex.h"

IMPLEMENT_DYNAMIC(TestReport, CDialogEx)

TestReport::TestReport(CWnd* pParent /*=nullptr*/)
	: CDialogEx(IDD_DIALOG1, pParent)
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
END_MESSAGE_MAP()

afx_msg LRESULT TestReport::OnUpdateReport(WPARAM wParam, LPARAM lParam)
{
	if (lParam != NULL) {
		struct report_data* rd = (report_data*)lParam;
		CString line;

		if (rd->video_length >= 0)
		{
			line.Format(_T("video length : %d"), rd->video_length);
			report.SetItemText(3, 0, line);
		}

		if (rd->play_length >= 0)
		{
			line.Format(_T("play length : %d"), rd->play_length);
			report.SetItemText(4, 0, line);
		}

		delete rd; rd = NULL;
	}
	
	return 0;
}

BOOL TestReport::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	CString external_ip=_T("unknown"),city=_T("unknown"), isp=_T("unknown");
	httpHandler.GetExternalIP(external_ip);
	if (external_ip.GetLength() > 1)
		httpHandler.GetCityAndIsp(external_ip, city, isp);
	else
		external_ip = _T("unknown");

	report.InsertItem(0, city);
	report.InsertItem(1, isp);
	report.InsertItem(2, external_ip);
	report.InsertItem(3, _T(""));
	report.InsertItem(4, _T("video length : 0"));
	report.InsertItem(5, _T("play length : 0"));
	return TRUE;
}