const converterParaSelect2 = () => $(".campo-select")
    .each(
        function (_, element) {
            const elementId = element.id;
            $(`#${elementId}`).select2();
        }
    );

const alterarEstilizacaoSelect2 = () => {
    $('.select2-container--default .select2-selection--single').css({
        "height": "40px",
        "border": "1px solid rgb(131 133 136)",
        "display": "flex",
        "align-items": "center"
    });

    $('.select2-container--default .select2-selection--single .select2-selection__arrow').css({
        "top": "7px"
    });
}

$(document).ready(function () {
    converterParaSelect2();
    alterarEstilizacaoSelect2();
});