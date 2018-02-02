$(function () {

    var $purchaseForm = $('#purchase-form');
    var $purchaseFormContent = $('#purchase-form-content');
    var $filterTimer;
    var $isEditMode = false;

    // Переключение режимов: редактирование/просмотр
    var switchEditMode = function (mode) {
        $('.edit-purchase').prop('disabled', mode);
        $('.del-purchase').prop('disabled', mode);
        $('#purchase-filter').prop('disabled', mode);
        $('#add-purchase').prop('disabled', mode);

        $isEditMode = mode;
    };

    // Добавить покупку
    $('#add-purchase').click(function () {
        switchEditMode(true);

        $.get('/shoplist/create/', function (data) {
            $('#purchase-list').append(data);
        })
    });

    // Редактировать покупку
    $purchaseForm.on('click', '.edit-purchase', function () {
        switchEditMode(true);

        var purchaseLine = $(this).parent().parent();
        var pId = purchaseLine.data('pid');

        $.get('/shoplist/' + pId + '/', function (data) {
            purchaseLine.replaceWith(data);
        });
    });

    //Удалить покупку
    $purchaseForm.on('click', '.del-purchase', function () {
        var purchaseLine = $(this).parent().parent();
        var pId = purchaseLine.data('pid');
        var token = $purchaseForm.find('[name="csrfmiddlewaretoken"]').serialize();

        $.post('/shoplist/' + pId + '/delete/', token, function (data) {
            $purchaseFormContent.html(data);
        });
    });

    // Сохранить изменения при добавлении или изменении покупки
    $purchaseForm.submit(function (e) {
        e.preventDefault();

        var actionUrl = '/shoplist/create/';

        var primaryKeyField = $('#id_id');
        if (primaryKeyField.attr('value')) {
            actionUrl = '/shoplist/' + primaryKeyField.attr('value') + '/';
        }

        var data = $purchaseForm.serialize();

        $.post(actionUrl, data, function (data) {
            $purchaseFormContent.html(data);
            switchEditMode(false);
        });
    });

    // Отменить добавление покупки
    $purchaseForm.on('click', '#cancel-purchase', function () {
        $.get('/shoplist/', function (data) {
            $purchaseFormContent.html(data);
            switchEditMode(false);
        });
    });

    // Отфильтровать список
    var filterList = function () {
        clearTimeout($filterTimer);

        var filter = $('#purchase-filter').serialize();

        $.get('/shoplist/', filter, function (data) {
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

        $.get('/shoplist/', 'order_by=' + thName, function (data) {
            $purchaseFormContent.html(data);
        });
    });
});