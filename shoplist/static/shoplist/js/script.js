$(function () {

    var $purchaseForm = $('#purchase-form');
    var $purchaseFormContent = $('#purchase-form-content');
    var $token = $purchaseForm.find('[name="csrfmiddlewaretoken"]').serialize();
    var $filterTimer;
    var $isEditMode = false;

    // Переключение режимов: редактирование/просмотр
    var switchEditMode = function (mode) {
        $('.edit-purchase').prop('disabled', mode);
        $('.del-purchase').prop('disabled', mode);
        $('#purchase-filter').prop('disabled', mode);
        $('#add-purchase').prop('disabled', mode);

        var btns = $('.purchase-grp-btn button');
        if (mode) {
            btns.addClass('disabled');
        } else {
            btns.removeClass('disabled');
        }


        $isEditMode = mode;
    };

    // Добавить покупку
    $('#add-purchase').click(function () {
        switchEditMode(true);

        $.get('/create/', function (data) {
            $('#purchase-list').append(data);
        })
    });

    // Редактировать покупку
    $purchaseForm.on('click', '.edit-purchase', function (e) {
        e.preventDefault();

        switchEditMode(true);

        var purchaseLine = $(this).parents('.purchase-line');
        var pId = purchaseLine.data('pid');

        $.get('/' + pId + '/', function (data) {
            purchaseLine.replaceWith(data);
        });
    });

    //Удалить покупку
    $purchaseForm.on('click', '.del-purchase', function (e) {
        e.preventDefault();

        var pId = $(this).parents('.purchase-line').data('pid');

        $.post('/' + pId + '/delete/', $token, function (data) {
            $purchaseFormContent.html(data);
        });
    });

    // Сохранить изменения при добавлении или изменении покупки
    $purchaseForm.submit(function (e) {
        e.preventDefault();

        var actionUrl = '/create/';

        var pkField = $('#id_id');
        if (pkField.attr('value')) {
            actionUrl = '/' + pkField.attr('value') + '/';
        }

        var data = $purchaseForm.serialize();

        $.post(actionUrl, data, function (data) {
            $purchaseFormContent.html(data);
            switchEditMode(false);
        });
    });

    $purchaseForm.on('click', '.ok-purchase', function () {
        $purchaseForm.submit();
    });

    // Отменить добавление покупки
    $purchaseForm.on('click', '.cancel-purchase', function () {
        $.get('/', function (data) {
            $purchaseFormContent.html(data);
            switchEditMode(false);
        });
    });

    // Отфильтровать список
    var filterList = function () {
        clearTimeout($filterTimer);

        var filter = $('#purchase-filter').serialize();

        $.get('/', filter, function (data) {
            $purchaseFormContent.html(data);
        });
    };

    $purchaseForm.on('keypress', '#purchase-filter', function (e) {
        if (e.which === 13) {
            e.preventDefault();
            filterList();
        }
    });

    $purchaseForm.on('input', '#purchase-filter', function () {
        clearTimeout($filterTimer);
        $filterTimer = setTimeout(filterList, 500);
    });

    // Сортировать список
    $purchaseForm.on('click', 'th[data-th-name]', function () {
        if ($isEditMode) return;

        var thName = $(this).data('th-name');

        $.get('/', 'order_by=' + thName, function (data) {
            $purchaseFormContent.html(data);
        });
    });

    // Изменение статуса покупки
    $purchaseForm.on('click', '.purchase-name', function () {
        var pId = $(this).parents('.purchase-line').data('pid');

        $.post('/' + pId + '/change_status/', $token, function (data) {
            $purchaseFormContent.html(data);
        })
    });

    // -------------------------------------------------------------
    var $dictForm = $('#dict-form');
    var $dictFormContent = $('#dict-form-content');
    var $modelName = $dictForm.data('model-name');
    var $dictToken = $dictForm.find('[name="csrfmiddlewaretoken"]').attr('value');

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

    $('#create-dict').click(function () {
        switchEditModeDict(true);

        $.get('/' + $modelName + '/', function (data) {
            $('#dict-list').append(data);
        });
    });

    $dictForm.on('click', '.edit-dict', function (e) {
        e.preventDefault();

        switchEditModeDict(true);

        var dictLine = $(this).parents('.dict-line');
        var pid = dictLine.data('pid');

        $.get('/' + $modelName + '/' + pid + '/', function (data) {
            dictLine.replaceWith(data);
        });
    });

    $dictForm.on('click', '.del-dict', function (e) {
        e.preventDefault();

        var pid = $(this).parents('.dict-line').data('pid');

        $.ajax({
            url: '/' + $modelName + '/' + pid + '/',
            headers: {
                'X-CSRFTOKEN': $dictToken
            },
            type: 'DELETE',
            dataType: 'html',
            success: function (data) {
                $dictFormContent.html(data);
            }
        });
    });

    $dictForm.submit(function (e) {
        e.preventDefault();

        var pid = $('#id_id').attr('value');
        var url = '/' + $modelName + '/';

        if (pid) {
            url += pid + '/';
        }

        var data = $dictForm.serialize();

        $.post(url, data, function (data, status, xhr) {
            if(xhr.responseJSON) {
                $('.dict-new-line').replaceWith(data.response);
            } else {
                $dictFormContent.html(data);
                switchEditModeDict(false);
            }
        });
    });

    // Временное для тестирования валидации
    $dictForm.on('click', '.ok-dict', function () {
        $dictForm.submit();
    });

    $dictForm.on('click', '.cancel-dict', function () {
        $.get('/' + $modelName + '/list/', function (data) {
            $dictFormContent.html(data);
            switchEditModeDict(false);
        });
    });

});