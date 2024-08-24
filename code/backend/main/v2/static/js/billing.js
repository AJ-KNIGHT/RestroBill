
// Minus button click event listener
document.querySelectorAll('.number-input .minus').forEach(button => {
    button.addEventListener('click', function () {
        this.closest('.number-input').querySelector('input').stepDown();
    });
});

// Plus button click event listener  
document.querySelectorAll('.number-input .plus').forEach(button => {
    button.addEventListener('click', function () {
        this.closest('.number-input').querySelector('input').stepUp();
    });
});

// live search
function liveSearch(value) {
    value = value.trim();

    if (value != "") {
        $.ajax({
            url: "search",
            data: { searchText: value },
            dataType: "json",

            success: function (data) {
                var res = "";
                console.log(data.results)
                for (i in data.results) {
                    // res += "<div class='item'><span>" + data.results[i] + "</span></div>";
                    res += "<div class='item'><span>" + data.results[i].name +
                    "  ₹" + data.results[i].price + "</span></div>";
                }
                $(".list-items").html(res);
            }
        })
    }
    else {
        $(".list-items").html("");
    }
}