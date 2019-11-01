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
			report.SetItemText(0, 0, line);
		}

		if (rd->play_length >= 0)
		{
			line.Format(_T("play length : %d"), rd->play_length);
			report.SetItemText(1, 0, line);
		}

		delete rd; rd = NULL;
	}
	
	return 0;
}

BOOL TestReport::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	report.InsertItem(0, _T("video length : 0"));
	report.InsertItem(1, _T("play length : 0"));

	return TRUE;
}
