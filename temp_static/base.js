function set_board_group_constant_at_session_storage(board_group_id, board_set) {
    // session storage set
    sessionStorage.setItem('board_group_' + board_group_id, JSON.stringify(board_set));
}

function get_board_group_constant_at_session_storage(board_group_id) {
    // session storage search
    let board_set;
    try {
        const board_set_json = sessionStorage.getItem('board_group_' + board_group_id);
        board_set = JSON.parse(board_set_json);
    } catch (e) {
        board_set = null;
    }
    return board_set;
}

function display_board_group_constant(board_set) {
    $('#from_board_group').css('display', 'flex');
    $('#from_board_group').html('');

    board_set.forEach(function (data) {
        $('#from_board_group').append(
            `<a style="word-break: keep-all;" class="nav-link" href="/${data.url}">${data.name}</a>`
        );
    });
}

function get_board_set_from_board_group(board_group_id) {
    const board_set = get_board_group_constant_at_session_storage(board_group_id);

    if (board_set) {
        display_board_group_constant(board_set);
    } else {
        $.ajax({
            type: 'GET',
            url: '/board-group/' + board_group_id + '/constant',
            success: function (data) {
                display_board_group_constant(data['board_set']);
                set_board_group_constant_at_session_storage(board_group_id, data['board_set']);
            }
        });
    }
}