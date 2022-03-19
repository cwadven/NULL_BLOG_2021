let alarm_status = true;

// 알림 관련
function get_notification_ajax() {
    $.ajax({
        // type을 설정합니다.
        type: 'GET',
        url: '/notification',
        success: function (data) {
            if (data) {
                if (alarm_status) {
                    $('#notifications').html('');
                    for (let i = 0; i < data["notification_infos"].length; i++) {
                        let type = data['notification_infos'][i]['notification_type'];
                        let id = data['notification_infos'][i]['id'];
                        let title = data['notification_infos'][i]['title'];
                        let body = data['notification_infos'][i]['body'];
                        let sender = data['notification_infos'][i]['sender'];

                        let svg_img;
                        let url = '<a href=\'/notification/check/' + id + '\'>' + '보기</a>';

                        if (type === 'replynotification') {
                            svg_img = `<svg width="28" height="35" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
                                <path style="text-indent:0;text-align:start;line-height:normal;text-transform:none;block-progression:tb;-inkscape-font-specification:Bitstream Vera Sans" d="M 3 6 L 3 7 L 3 25 L 3 26 L 4 26 L 12.5625 26 L 15.28125 28.71875 L 16 29.40625 L 16.71875 28.71875 L 19.4375 26 L 28 26 L 29 26 L 29 25 L 29 7 L 29 6 L 28 6 L 4 6 L 3 6 z M 5 8 L 27 8 L 27 24 L 19 24 L 18.59375 24 L 18.28125 24.28125 L 16 26.5625 L 13.71875 24.28125 L 13.40625 24 L 13 24 L 5 24 L 5 8 z M 9 11 L 9 13 L 23 13 L 23 11 L 9 11 z M 9 15 L 9 17 L 23 17 L 23 15 L 9 15 z M 9 19 L 9 21 L 19 21 L 19 19 L 9 19 z" color="#000" overflow="visible" font-family="Bitstream Vera Sans"/>
                            </svg>`;
                        } else if (type === 'rereplynotification') {
                            svg_img = `<svg width="28" height="35" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
                                <path style="text-indent:0;text-align:start;line-height:normal;text-transform:none;block-progression:tb;-inkscape-font-specification:Bitstream Vera Sans" d="M 3 6 L 3 7 L 3 25 L 3 26 L 4 26 L 12.5625 26 L 15.28125 28.71875 L 16 29.40625 L 16.71875 28.71875 L 19.4375 26 L 28 26 L 29 26 L 29 25 L 29 7 L 29 6 L 28 6 L 4 6 L 3 6 z M 5 8 L 27 8 L 27 24 L 19 24 L 18.59375 24 L 18.28125 24.28125 L 16 26.5625 L 13.71875 24.28125 L 13.40625 24 L 13 24 L 5 24 L 5 8 z M 9 11 L 9 13 L 23 13 L 23 11 L 9 11 z M 9 15 L 9 17 L 23 17 L 23 15 L 9 15 z M 9 19 L 9 21 L 19 21 L 19 19 L 9 19 z" color="#000" overflow="visible" font-family="Bitstream Vera Sans"/>
                            </svg>`;
                        } else if (type === 'likenotification') {
                            svg_img = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart-fill text-danger" viewBox="0 0 16 16">
                                <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
                            </svg>`;
                        }
                        $('#notifications').append(
                            `<div class="mb-1 py-1 " style="display: flex; align-items: center;border-radius:7px;background-color: #F1F1F1; margin: 1px 1px;">
                                <div class="mx-2 position-relative" style="display:flex; align-items: center; justify-content: center;height:65px; width:65px;border:1px solid rgba(0, 0, 0, 0.2); border-radius:50%;background-color: #FFFFFF; flex-shrink:0;">
                                    ${svg_img}
                                </div>
                                <div style="font-size: 16px; width:100%;">
                                    <div style="font-weight: bold;">${title}</div>
                                    <div class="mr-2" style="font-size: smaller;">${body}</div>
                                    <div class='mt-2' style="display: flex; justify-content: space-between; font-size: 14px;">
                                    <div>${url}</div>
                                    <div style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;width: 160px; text-align: right; margin-right: 9px;">${sender}</div>
                                    </div>
                                </div>
                            </div>`
                        );

                    }

                    if (data['notification_infos'].length === 0) {
                        $('#notifications').append('<div class=\'text-center p-3\'>추가적인 알림이 없습니다.</div>');
                    }

                    alarm_status = false;

                } else {
                    alarm_status = true;
                }
            } else {
                // 만들었다 사라졌다!! 아무것도 없을 경우!!
                if (alarm_status) {
                    $('#notifications').html('소식이 없습니다.');
                    alarm_status = false;
                } else {
                    $('#notifications').html('');
                    alarm_status = true;
                }
            }

        }
    });
}
