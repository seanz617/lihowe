#pragma once
#include <afxcmn.h>
class PlaySlider : public CSliderCtrl
{
public:
	PlaySlider();
	~PlaySlider();
	DECLARE_MESSAGE_MAP()
	afx_msg void OnLButtonUp(UINT nFlags, CPoint point);

public:
	BOOL user_flag;
protected:
	afx_msg LRESULT OnChangePlayPos(WPARAM wParam, LPARAM lParam);
};

