$(function () {

    var $purchaseForm = $('#purchase-form');

    var disableOtherButtons = function () {
        $('.edit-purchase').prop('disabled', true);
        $('.del-purchase').prop('disabled', true);

        $('#purchase-filter').prop('disabled', true);
        $('#purchase-filter-button').prop('disabled', true);
    };

    // Добавить покупку
    $('#add-purchase').click(function (e) {
        e.preventDefault();

        disableOtherButtons();

        if ($('#purchase-new-line').length === 0) {
            $.get('/shoplist/create/', function (data) {
                $('#purchase-list').append(data);
            })
        }
    });

    // Редактировать покупку
    $purchaseForm.on('click', '.edit-purchase', function (e) {
        disableOtherButtons();

        var purchaseLine = $(this).parent().parent();
        var pId = purchaseLine.data('pid');

        $.get('/shoplist/' + pId + '/', function (data) {
            purchaseLine.replaceWith(data);
        });
    });

    //Удалить покупку
    $purchaseForm.on('click', '.del-purchase', function (e) {
        e.preventDefault();

        var purchaseLine = $(this).parent().parent();
        var pId = purchaseLine.data('pid');
        var token = $purchaseForm.find('[name="csrfmiddlewaretoken"]').serialize();

        $.post('/shoplist/' + pId + '/delete/', token, function (data) {
            $('#purchase-list').html(data);
        });
    });

    // Сохранить изменения при добавлении или изменении покупки
    $purchaseForm.submit(function (e) {
        e.preventDefault();

        var actionUrl = '/shoplist/create/';

        var $primaryKeyField = $('#purchase-pk');
        if ($primaryKeyField.length === 1) {
            actionUrl = '/shoplist/' + $primaryKeyField.attr('value') + '/';
        }

        var data = $purchaseForm.serialize();

        $.post(actionUrl, data, function (data) {
            $purchaseForm.html(data)
        });
    });

    // Отменить добавление покупки
    $purchaseForm.on('click', '#cancel-purchase', function (e) {
        $.get('/shoplist/', function (data) {
            $purchaseForm.html(data);
        });
    });

    // Отфильтровать список
    var filterList = function () {
        var filter = $('#purchase-filter').serialize();

        $.get('/shoplist/', filter, function (data) {
            $purchaseForm.html(data);
        });
    };

    $purchaseForm.on('click', '#purchase-filter-button', filterList);
    $purchaseForm.on('keypress', '#purchase-filter', function (e) {
        if (e.which === 13) {
            filterList();
        }
    });

    // Сортировать список
    $purchaseForm.on('click', '.purchase-sort', function () {
        var thName = $(this).data('th-name');

        $.get('/shoplist/', 'order_by=' + thName, function (data) {
            $purchaseForm.html(data);
        });
    });

});