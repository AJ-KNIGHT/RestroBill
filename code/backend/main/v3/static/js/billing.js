
//old code: 

// // Minus button click event listener
// document.querySelectorAll('.number-input .minus').forEach(button => {
//     button.addEventListener('click', function () {
//         this.closest('.number-input').querySelector('input').stepDown();
//     });
// });

// // Plus button click event listener  
// document.querySelectorAll('.number-input .plus').forEach(button => {
//     button.addEventListener('click', function () {
//         this.closest('.number-input').querySelector('input').stepUp();
//     });
// });

// // live search
// function liveSearch(value) {
//     value = value.trim();

//     if (value != "") {
//         $.ajax({
//             url: "search",
//             data: { searchText: value },
//             dataType: "json",

//             success: function (data) {
//                 var res = "";
//                 console.log(data.results)
//                 for (i in data.results) {
//                     // res += "<div class='item'><span>" + data.results[i] + "</span></div>";
//                     res += "<div class='item'><span>" + data.results[i].name +
//                    "</span> <span>  ₹" + data.results[i].price + "</span></div>";
//                 }
//                 $(".list-items").html(res);
//             }
            
//         })
//     }
//     else {
//         $(".list-items").html("");
//     }
// }


// new code:

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
                // console.log(data.results);
                for (let i in data.results) {
                    res += "<div class='item' data-name='" + data.results[i].name + 
                            "' data-price='" + data.results[i].price + 
                            "'><span>" + data.results[i].name + 
                            "</span> <span>  ₹" + data.results[i].price + "</span></div>";
                }
                $(".list-items").html(res);
                
                // Add click event to each item
                $(".list-items .item").on("click", function() {
                    addRow($(this).data("name"), $(this).data("price"));
                });
            }
        });
    } else {
        $(".list-items").html("");
    }
}

// Function to add item to billing table
function addRow(name, price) {
    var rowCount = $(".table-list tbody tr").length;
    const quantity = 1;
    var newRow = `
        <tr>
            <td><div class="remove-icon" onclick='removeRow(this)'><img src="/images/close.png"></div></td>
            <td>${rowCount + 1}</td>
            <td>${name}</td>
            <td>
                <div class="number-input">
                    <button class="minus">-</button>
                    <input type="number" value="${quantity}" min="0" max="100" step="1">
                    <button class="plus">+</button>
                </div>
            </td>
            <td>₹${price}</td>
            <td>₹${(quantity * price).toFixed(2)}</td>
        </tr>
    `;
    $(".table-list tbody").append(newRow);

    // Set the value of the input to an empty string
    $(".list-items").html(""); // Clear the search results
    $(this).val(""); // Clear the input
    
    // Reattach event listeners for the new row's plus and minus buttons
    // qtyListeners();
}


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




// function qtyListeners() {
//     // Minus button click event listener
//     document.querySelectorAll('.number-input .minus').forEach(button => {
//         button.addEventListener('click', function () {
//             this.closest('.number-input').querySelector('input').stepDown();
//             updateTotalPrice(event.target.closest('tr')); 
//         });
//     });

//     // Plus button click event listener  
//     document.querySelectorAll('.number-input .plus').forEach(button => {
//         button.addEventListener('click', function () {
//             this.closest('.number-input').querySelector('input').stepUp();
//         });
//     });
// }

// function qtyListeners() {
//     // Attach event listeners to the parent element for quantity buttons
//     document.querySelector('.table-list tbody').addEventListener('click', function (event) {
//         if (event.target.matches('.minus') || event.target.matches('.plus')) {
//             const input = event.target.closest('.number-input').querySelector('input');
//             const priceCell = event.target.closest('tr').querySelector('td:nth-child(6)'); // Selects the total price cell
//             const price = parseFloat(priceCell.previousElementSibling.textContent.replace('₹', '')); // Get the price per item

//             // Update quantity based on the button clicked
//             if (event.target.matches('.minus')) {
//                 input.stepDown();
//             } else if (event.target.matches('.plus')) {
//                 input.stepUp();
//             }

//             // Update total price based on the new quantity
//             const quantity = parseInt(input.value);
//             const totalPrice = (quantity * price).toFixed(2);
//             priceCell.textContent = `₹${totalPrice}`; // Update the total price cell
//         }
//     });
// }



// enter to select the first item
$(".search input").on("keydown", function(event) {
    if (event.key === "Enter") {
        var firstItem = $(".list-items .item").first();
        if (firstItem.length) {
            addRow(firstItem.data("name"), firstItem.data("price"));
            $(".list-items").html(""); // Clear the search results
            $(this).val(""); // Clear the input
        }
    }
});

// Function to remove a row from the billing table
function removeRow(button) {
    const row = button.closest('tr');
    row.parentNode.removeChild(row);
}

// // Function to refresh the billing table by removing all rows
function refreshTable() {
    const tableBody = document.querySelector('.table-list tbody');
    
    // Remove all rows from the tbody
    while (tableBody.rows.length > 0) {
        tableBody.deleteRow(0);
    }
}

// function updateTotalPrice(row) {
//     const quantityInput = row.querySelector('input[type="number"]');
//     const priceCell = row.querySelector('td:nth-child(6)'); // Assuming the total price is in the 6th cell
//     const pricePerUnit = parseFloat(priceCell.previousElementSibling.textContent.replace('₹', '')); // Get the price from the previous cell

//     const quantity = parseInt(quantityInput.value);
//     const totalPrice = quantity * pricePerUnit;

//     priceCell.textContent = `₹${totalPrice.toFixed(2)}`; // Update the total price cell
// }
