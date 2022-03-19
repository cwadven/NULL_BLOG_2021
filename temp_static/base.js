function get_board_set_from_board_group(board_group_id) {
    $.ajax({
        type: 'GET',
        url: '/board-group/' + board_group_id + '/constant',
        success: function (data) {
            $('#from_board_group').css('display', 'flex');
            $('#from_board_group').html('');

            data['board_set'].forEach(function (data){
                $('#from_board_group').append(
                    `<div class="nav-item">
                        <a style="word-break: keep-all;" class="nav-link" href="/${data.url}">${data.name}</a>
                    </div>`
                );
            });
        }
    });
}