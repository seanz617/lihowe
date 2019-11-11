#include "stdafx.h"
#include "PlaySlider.h"

PlaySlider::PlaySlider()
{
	user_flag = FALSE;
}

PlaySlider::~PlaySlider()
{
}

BEGIN_MESSAGE_MAP(PlaySlider, CSliderCtrl)
	ON_WM_LBUTTONUP()
	ON_MESSAGE(WM_CHANGE_PLAY_POS, &PlaySlider::OnChangePlayPos)
END_MESSAGE_MAP()

void PlaySlider::OnLButtonUp(UINT nFlags, CPoint point)
{
	CSliderCtrl::OnLButtonUp(nFlags, point);
	CRect rectClient, rectChannel;
	GetClientRect(rectClient);
	GetChannelRect(rectChannel);
	int nMax = 1000;
	int nMin = 0;
	//GetRange(nMin, nMax);
	int nPos = (nMax - nMin)*(point.x - rectClient.left - rectChannel.left) / (rectChannel.right - rectChannel.left);
	SendMessage(WM_CHANGE_PLAY_POS,nPos,NULL);
	user_flag = TRUE;
	GetParent()->SendMessage(WM_USER_CHANGE_POS, nPos, LPARAM(this));
}

afx_msg LRESULT PlaySlider::OnChangePlayPos(WPARAM wParam, LPARAM lParam)
{
	if ((user_flag && lParam != NULL) || !user_flag)
	{
		SetPos(wParam);
	}
	return 0;
}
