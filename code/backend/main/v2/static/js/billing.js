
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
//                 $(".list-items").show();
//             }

//         })
//     }
//     else {
//             // $(".list-items").html(""); // Clear the search results
//         $(".list-items").hide();
//     }
// }


// new code:
let cart = {};

// live search
function liveSearch(value) {
    value = value.trim();
    if (value != "") {
        $.ajax({
            url: "/search",
            data: { searchText: value },
            dataType: "json",
            success: function (data) {
                var res = "";
                // console.log(data.results);
                for (let i in data.results) {
                    res += "<div class='item' data-name='" + data.results[i].name +
                        "' data-pid='" + data.results[i].pid +
                        "' data-price='" + data.results[i].price +
                        "'><span>" + data.results[i].name +
                        "</span> <span>  ₹" + data.results[i].price + "</span></div>";
                }
                $(".list-items").html(res);
                $(".list-items").show();

                // Add click event to each item
                $(".list-items .item").on("click", function () {
                    addRow($(this).data("name"), $(this).data("price"), $(this).data("pid"));
                });
            }
        });
    } else {
        $(".list-items").hide();
    }
}


function addRow(name, price, pid) {
    // Check if the item already exists in the table
    const existingRow = $(".table-list tbody tr").filter(function () {
        return $(this).find("td:nth-child(3)").text() === name;
    });

    if (existingRow.length) {
        // If item exists, increment the quantity
        const quantityInput = existingRow.find("input[type='number']");
        const currentQuantity = parseInt(quantityInput.val());
        quantityInput.val(currentQuantity + 1);
        updateTotalPrice(existingRow);
    } else {
        // If item doesn't exist, add a new row

        var rowCount = $(".table-list tbody tr").length;
        const newSiNo = rowCount + 1;
        const quantity = 1;
        var newRow = `
            <tr id="row-${newSiNo}">
                <td><div class="remove-icon" onclick='removeRow(this)'><img src="/images/close.png"></div></td>
                <td>${newSiNo}</td>
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
        // $(".list-items").html(""); // Clear the search results
        $(".list-items").hide();
        $(this).val(""); // Clear the input

        // Update cart object with SI number as key and [pid, quantity] as value
        cart[newSiNo] = {"pid": pid, "qty": quantity};

        // Reattach event listeners for the new row's plus and minus buttons
        qtyListeners();
        reIndexSiNumbers();
    }
}

function reIndexSiNumbers() {
    $(".table-list tbody tr").each(function (i, row) {
        $(row).find("td:nth-child(2)").text(i + 1); // Update SI number based on index
    });
}

//1
// function qtyListeners() {
//     // Attach event listeners to all minus, plus, and input elements within the number-input class
//     $('.number-input').on('click keypress', '.minus, .plus, input', handleQuantityChange);

//     function handleQuantityChange(event) {
//         const input = $(this).closest('.number-input').find('input');
//         const quantity = parseInt(input.val());
        

//         if (!isNaN(quantity)) {
//             if (event.type === 'keypress' && event.key !== 'Enter') {
//                 // Ignore non-Enter keypresses
//                 return;
//             }

//             const change = $(this).hasClass('minus') ? -1 : (event.type === 'click' ? 1 : 0);
//             const newQuantity = Math.max(quantity + change, 1); // Ensure minimum quantity is 1
//             input.val(newQuantity);

//             // Update cart quantity based on the SI number
//             const siNo = parseInt($(this).closest('tr').find('td:nth-child(2)').text());
//             cart[siNo].qty = newQuantity;

//             updateTotalPrice($(this).closest('tr')); // Update total price based on the row
//         }
//     }
// };

// test

function qtyListeners() {
    // Attach event listeners to all minus, plus, and input elements within the number-input class
    $('.number-input').on('click keypress', '.minus, .plus, input', handleQuantityChange);

    function handleQuantityChange(event) {
        const row = $(event.target).closest('tr');
        const siNo = row.attr('id').replace('row-', ''); // Extract SI number from the ID
    
        const input = row.find('input[type="number"]');
        const quantity = parseInt(input.val());
    
        if (!isNaN(quantity)) {
            if (event.type === 'keypress' && event.key !== 'Enter') {
                // Ignore non-Enter keypresses
                return;
            }
    
            const change = $(this).hasClass('minus') ? -1 : (event.type === 'click' ? 1 : 0);
            const newQuantity = Math.max(quantity + change, 1); // Ensure minimum quantity is 1
            console.log(newQuantity)
            input.val(newQuantity);
    
            // Update cart quantity based on the SI number
            cart[siNo].qty = newQuantity;
    
            updateTotalPrice(row); // Update total price based on the row
        }
    }
};

// enter to select the first item
$(".search input").on("keydown", function (event) {
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
    const rowToRemove = $(button).closest('tr');
    const siNo = parseInt(rowToRemove.find("td:nth-child(2)").text());
    delete cart[siNo];

    rowToRemove.remove();
    // Re-index remaining SI numbers
    $(".table-list tbody tr").each(function (i, row) {
        $(row).find("td:nth-child(2)").text(i + 1); // Update SI number based on index
    });
}

// // Function to refresh the billing table by removing all rows
function refreshTable() {
    const tableBody = document.querySelector('.table-list tbody');
    cart = {};

    // Remove all rows from the tbody
    while (tableBody.rows.length > 0) {
        tableBody.deleteRow(0);
    }
}

function updateTotalPrice(row) {
    const $row = $(row);
    const quantity = parseInt($row.find('input[type="number"]').val());
    const pricePerUnit = parseFloat($row.find('td:nth-child(5)').text().replace('₹', ''));
    const totalPrice = quantity * pricePerUnit;
    $row.find('td:nth-child(6)').text(`₹${totalPrice.toFixed(2)}`);
}

// Check if the cart is empty
function isCartEmpty(cart) {
    return Object.keys(cart).length === 0;
}

$("#print").click(function() {
    if (isCartEmpty(cart)) {
        alert("The cart is empty.");
    } else {
        // Proceed with the AJAX request
        $.ajax({
            url: "/print-bill",
            type: "POST",
            data: JSON.stringify(cart),
            contentType: "application/json",
            dataType: "json",
            success: function(response) {
                console.log(response.message);
            },
            error: function(error) {
                console.error(error);
            }
        });
        alert("Printing...");
    }
});

// $("#print").click(function() {
//     $.ajax({
//         url: "/print-bill",
//         type: "POST",
//         contentType: "application/json",
//         data: JSON.stringify(cart),
//         dataType: "json",
//         success: function(response) {
//             console.log(response.message);
//         },
//         error: function(error) {
//             console.error("Error:", error.status, error.statusText);
//             // Handle the error based on the status code
//             if (error.status === 401) {
//                 alert("Access denied. Please log in.");
//             } else {
//                 alert("An error occurred. Please try again.");
//             }
//         }
//     });
// });





// keyboard shortcuts
// $(document).keydown(function(event) {
//     if (event.ctrlKey) {
//       switch (event.key) {
//         case 'o':
//           // Handle Ctrl+S for saving
//           console.log("Ctrl+o pressed");
//           break;
//         case '.':
//           // Handle Ctrl+N for creating a new item
//           console.log("Ctrl+. pressed");
//           break;
//         case 'd':
//           // Handle Ctrl+D for deleting the selected item
//           console.log("Ctrl+d pressed");
//           break;
//         // Add more shortcuts as needed
//       }
//     }
//   });