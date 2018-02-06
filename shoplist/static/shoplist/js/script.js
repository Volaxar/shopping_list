$(function () {

    var $dictForm = $('#dict-form');
    var $dictFormContent = $('#dict-form-content');
    var $modelName = $dictForm.data('model-name');
    var $token = $dictForm.find('[name="csrfmiddlewaretoken"]').attr('value');

    var $filterTimer;
    var $isEditMode = false;

    // Переключение режимов: редактирование/просмотр
    var switchEditModeDict = function (mode) {
        $('.dis-prop').prop('disabled', mode);

        var disItems = $('.dis-class');
        if (mode) {
            disItems.addClass('disabled');
        } else {
            disItems.removeClass('disabled');
        }

        $isEditMode = mode;
    };

    // Добавить элемент списка
    $('#create-dict').click(function () {
        switchEditModeDict(true);

        $.get('/' + $modelName + '/', function (data) {
            $('#dict-list').append(data);
        });
    });

    // Редактировать элемент списка
    $dictForm.on('click', '.edit-dict', function (e) {
        e.preventDefault();

        switchEditModeDict(true);

        var dictLine = $(this).parents('.dict-line');
        var pid = dictLine.data('pid');

        $.get('/' + $modelName + '/' + pid + '/', function (data) {
            dictLine.replaceWith(data);
        });
    });

    // Удалить элемент списка
    $dictForm.on('click', '.del-dict', function (e) {
        e.preventDefault();

        var pid = $(this).parents('.dict-line').data('pid');

        $.ajax({
            url: '/' + $modelName + '/' + pid + '/',
            headers: {
                'X-CSRFTOKEN': $token
            },
            type: 'DELETE',
            dataType: 'html',
            success: function (data) {
                $dictFormContent.html(data);
            }
        });
    });

    // Сохранить изменения
    $dictForm.submit(function (e) {
        e.preventDefault();

        var pid = $('#id_id').attr('value');
        var url = '/' + $modelName + '/';

        if (pid) {
            url += pid + '/';
        }

        var data = $dictForm.serialize();

        $.post(url, data, function (data, status, xhr) {
            if (xhr.responseJSON) {
                $('.dict-new-line').replaceWith(data.response);
            } else {
                $dictFormContent.html(data);
                switchEditModeDict(false);
            }
        });
    });

    // Отменить изменения
    $dictForm.on('click', '.cancel-dict', function () {
        $.get('/' + $modelName + '/list/', function (data) {
            $dictFormContent.html(data);
            switchEditModeDict(false);
        });
    });

    // Отфильтровать список
    var filterList = function () {
        clearTimeout($filterTimer);

        var filter = $('#purchase-filter').serialize();

        $.get('/purchase/list/', filter, function (data) {
            $dictFormContent.html(data);
        });
    };

    // Фильтрация при нажатии Enter
    $dictForm.on('keypress', '#purchase-filter', function (e) {
        if (e.which === 13) {
            e.preventDefault();
            filterList();
        }
    });

    // Фильрация по таймеру
    $dictForm.on('input', '#purchase-filter', function () {
        clearTimeout($filterTimer);
        $filterTimer = setTimeout(filterList, 500);
    });

    // Сортировать список
    $dictForm.on('click', 'th.mn-purchase', function () {
        if ($isEditMode) return;

        var thName = $(this).data('th-name');

        $.get('/purchase/list/', 'order_by=' + thName, function (data) {
            $dictFormContent.html(data);
        });
    });

    // Изменение статуса покупки
    $dictForm.on('click', '.mn-purchase > td:not(.click-ignore)', function () {
        if ($isEditMode) return;

        var pId = $(this).parent().data('pid');

        $.ajax({
            url: '/purchase/' + pId + '/',
            type: 'PATCH',
            headers: {
                'X-CSRFTOKEN': $token
            },
            success: function (data) {
                $dictFormContent.html(data);
            }
        })
    });

});