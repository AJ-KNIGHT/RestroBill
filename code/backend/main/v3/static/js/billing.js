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
                document.querySelector(".list-items").innerHTML = res;
                document.querySelector(".list-items").style.display = 'block';
                // Add click event to each item
                document.querySelectorAll(".list-items .item").forEach(function (item) {
                    item.addEventListener("click", function () {
                        const name = item.getAttribute("data-name");
                        const price = item.getAttribute("data-price");
                        const pid = item.getAttribute("data-pid");
                        addRow(name, price, pid);
                    });
                });
            }
        });
    } else {
        document.querySelector(".list-items").style.display = 'none';
    }
}

// add row into billing table
function addRow(name, price, pid) {
    // Check if the item already exists in the table
    const rows = document.querySelectorAll(".table-list tbody tr");
    let existingRow = null;

    rows.forEach(row => {
        if (row.cells[2].textContent === name) {
            existingRow = row;
        }
    });

    if (existingRow) {
        // If item exists, increment the quantity
        const quantityInput = existingRow.querySelector("input[type='number']");
        let currentQuantity = parseInt(quantityInput.value, 10);
        quantityInput.value = currentQuantity + 1;
        updatePrice(existingRow);
    } else {
        // If item doesn't exist, add a new row
        const rowCount = document.querySelectorAll(".table-list tbody tr").length;
        const newSiNo = rowCount + 1;
        const quantity = 1;
        const newRow = document.createElement('tr');
        newRow.id = `row-${newSiNo}`;
        newRow.innerHTML = `
            <td><div class="remove-icon" onclick='removeRow(this)'><img src="/images/close.png" alt="Remove"></div></td>
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
        `;
        document.querySelector(".table-list tbody").appendChild(newRow);
        // Clear the input field, assuming `this` refers to the input field
        if (typeof this !== 'undefined' && this instanceof HTMLInputElement) {
            this.value = "";
        }
        cart[newSiNo] = { "pid": pid, "qty": quantity };
        qtyListeners();
        reIndexSiNumbers();
    }
    document.querySelector(".search input").value = '';
    document.querySelector(".list-items").style.display = "none";
    updateTotal(calculateTotal());
}

function reIndexSiNumbers() {
    const rows = document.querySelectorAll(".table-list tbody tr");
    rows.forEach((row, i) => {
        row.cells[1].textContent = i + 1; // Update SI number based on index
    });
}

function qtyListeners() {
    document.querySelectorAll('.number-input').forEach(container => {
        container.querySelector('.plus').addEventListener('click', handleQuantityChange);
        container.querySelector('.minus').addEventListener('click', handleQuantityChange);
        container.querySelector('input').addEventListener('keypress', handleQuantityChange);
    });
}


function handleQuantityChange(event) {
    const container = event.currentTarget.closest('.number-input');
    const input = container.querySelector('input');
    let quantity = parseInt(input.value, 10);
    let newQuantity = 1;

    if (!isNaN(quantity)) {
        if (event.type === 'keypress' && event.key !== 'Enter') {
            // Ignore non-Enter keypresses
            return;
        } else if (event.type === 'keypress' && event.key === 'Enter') {
            newQuantity = input.value;

        } else {
            // Determine the change in quantity based on the event
            const change = event.target.classList.contains('minus') ? -1 : 1;
            newQuantity = Math.max(quantity + change, 0); // Allow quantity to be zero
            input.value = newQuantity;
        }
        const row = event.currentTarget.closest('tr');
        const siNo = parseInt(row.cells[1].textContent, 10);
        if (newQuantity === 0) {
            const removeIcon = event.currentTarget.closest('tr').querySelector('.remove-icon');
            if (removeIcon) {
                removeRow(removeIcon);
            } else {
                console.error('Remove icon not found');
            }
            return;
        } else {
            cart[siNo].qty = newQuantity;
        }
        updatePrice(row);
        updateTotal(calculateTotal());
    }
}

function updatePrice(row) {
    const quantity = parseInt(row.querySelector("input[type='number']").value, 10);
    const price = parseFloat(row.cells[4].textContent.replace('₹', ''));
    row.cells[5].textContent = `₹${(quantity * price).toFixed(2)}`;
}

function removeRow(element) {
    const row = element.closest('tr'); // Find the closest <tr> ancestor
    if (row) {
        row.remove(); // Remove the entire row
        reIndexSiNumbers(); // Call function to re-index the rows
        updateTotal(calculateTotal());
    } else {
        console.error('Row not found');
    }
}


// enter to select the first item
document.querySelector(".search input").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        const firstItem = document.querySelector(".list-items .item");
        if (firstItem) {
            const name = firstItem.getAttribute("data-name");
            const price = firstItem.getAttribute("data-price");
            const pid = firstItem.getAttribute("data-pid");
            addRow(name, price, pid);
            document.querySelector(".list-items").innerHTML = "";
            this.value = "";
        }
    }
});


// // Function to refresh the billing table by removing all rows
function refreshTable() {
    const tableBody = document.querySelector('.table-list tbody');
    cart = {};

    // Remove all rows from the tbody
    while (tableBody.rows.length > 0) {
        tableBody.deleteRow(0);
    }
    updateTotal("0.00");
}

// Check if the cart is empty
function isCartEmpty(cart) {
    return Object.keys(cart).length === 0;
}

function calculateTotal() {
    let total = 0;
    const rows = document.querySelectorAll(".table-list tbody tr");
    rows.forEach(row => {
        const priceCell = row.cells[5].textContent.replace('₹', '');
        total += parseFloat(priceCell);
    });
    return total.toFixed(2); // Return the total with two decimal places
}

function updateTotal(newprice) {
    const totalElement = document.getElementById("total");
    totalElement.textContent = `₹${newprice}`;
}

// profile popup toggle
const profile_icon = document.querySelector(".profile-icon");
const profile = document.querySelector(".profile-div");

profile_icon.addEventListener("click", function (event) {
    event.stopPropagation(); // Prevent this click from triggering the window click listener
    if (profile.classList.contains("show")) {
        profile.classList.remove("show"); // Close profile-div
    } else {
        profile.classList.add("show"); // Open profile-div
    }
});

// Close profile-div when clicking outside of it
window.addEventListener("click", function (event) {
    if (!profile.contains(event.target) && event.target !== profile_icon) {
        profile.classList.remove("show"); // Close profile-div
    }
});

// popup vars
const checkout_popup = document.querySelector('.popup-container');
const body_container = document.querySelector('.container');
var inputAmount = document.getElementById('input-amount');
var change = document.getElementById('change');
var discountInput = document.getElementById('input-discount');
var totalAmount_main = document.getElementById('total-Amount')
var totalAmount = 0;
var payment = document.getElementById('payment');

// Popup logic
document.getElementById('checkout').onclick = function () {
    if (Object.keys(cart).length === 0) {
        alert("Cart is empty");
    } else {
        checkout_popup.style.display = "flex";
        body_container.classList.add("blur");
        totalAmount_main.value = document.getElementById('total').textContent;
        totalAmount = Number(totalAmount_main.value.replace(/₹/g, '').trim());
        inputAmount.value = totalAmount; // Set inputAmount to totalAmount
        payment.value = "Select payment type";
        change.value = "₹0.00";
        discountInput.value = "0.0";
    }
}

document.getElementById('close-popup').onclick = function () {
    checkout_popup.style.display = "none";
    body_container.classList.remove("blur");
    inputAmount.value = "";
}

// When the user clicks anywhere outside of the popup, close it
window.addEventListener("click", function (event) {
    if (event.target === checkout_popup) {
        checkout_popup.style.display = "none";
        body_container.classList.remove("blur");
    }
});

// Change box set value
// Add an event listener for input changes on inputAmount
inputAmount.addEventListener('input', function() {
    let amount = Number(this.value);
    let discountValue = Number(discountInput.value) || 0; // Get discount value or 0 if empty

    // Calculate effective total after discount
    let effectiveTotal = totalAmount - discountValue;
    if (amount >= effectiveTotal) {
        change.value = "₹" + (amount - effectiveTotal).toFixed(2);
    } else {
        change.value = "₹0.00"; // Reset change if amount is less than effective total
    }
});

// Update total amount based on discount input
discountInput.addEventListener('input', function() {
    let discountValue = Number(this.value) || 0; // Get discount value or 0 if empty

    // Ensure discount does not exceed total amount
    if (discountValue > totalAmount) {
        alert("Discount cannot exceed total amount.");
        this.value = "0.0";
        discountValue = "0.0";
    }
    totalAmount_main.value = "₹" + (totalAmount - discountValue).toFixed(2);
    totalAmount = Number(totalAmount_main.value.replace(/₹/g, '').trim());
    inputAmount.value = Number(totalAmount_main.value.replace(/₹/g, '').trim());
    inputAmount.dispatchEvent(new Event('input'));
});

function print_validate() {
    if (inputAmount.value < totalAmount) {
        alert("Tendered Amount is less than Total Amount");
    } else if (payment.value === "Select payment type") {
        alert("Payment type is not selected");
    }
    else {
        alert("print");
    }
}


// print
document.getElementById("print").addEventListener("click", function () {
    print_validate();
});

//// print
//document.getElementById("print").addEventListener("click", function () {
    //if (isCartEmpty(cart)) {
        //alert("The cart is empty.");
    //} else {
        //$.ajax({
            //url: "/print-bill",
            //type: "POST",
            //contentType: "application/json",
            //data: JSON.stringify(cart),  // Send the cart data to the backend
            //dataType: "json",
            //success: function (response) {
                //// console.log(response);

                //// var newTab =  window.open();
                //// newTab.document.write(response.data);
                //// newTab.document.close();
                //// Assuming the response contains a success message or the bill URL

                //if (response) {
                    //// 1. Show success message
                    //alert("Bill printed successfully!");
                    //// if (response.bill_url) {
                    ////     window.open(response.bill_url, '_blank');
                    //// }

                    //// if (response.billDetails && response.billDetails.length > 0) {
                    ////     printBill(response.billDetails);  // Call the printBill function
                    //// } else {
                    ////     alert("No products to print.");
                    //// }

                    //// 3. Clear the cart and reset the billing table
                    //refreshTable();  // Clears the table
                    //updateTotal(0);  // Resets the total to 0
                    //cart = {};  // Reset the cart
                //} else {
                    //// If there's an error message in the response, display it
                    //alert("Error: " + response.message);
                //}
            //},
            //error: function (error) {
                //// Handle the error based on the status code
                //if (error.status === 401) {
                    //alert("Access denied. Please log in.");
                //} else {
                    //alert("An error occurred while printing the bill.");
                //}

                //// console.log("error");
            //}
        //});
    //}
//});


// function printBill(billDetails) {
//     let billWindow = window.open('', '_blank');
//     billWindow.document.write('<html><head><title>Bill</title></head><body>');
//     billWindow.document.write('<h1>Restaurant Bill</h1>');
//     billWindow.document.write('<table border="1" style="width:100%"><tr><th>Item</th><th>Quantity</th><th>Price</th><th>Total</th></tr>');

//     billDetails.forEach(item => {
//         billWindow.document.write(`<tr>
//             <td>${item.name}</td>
//             <td>${item.qty}</td>
//             <td>₹${item.price}</td>
//             <td>₹${item.total}</td>
//         </tr>`);
//     });

//     billWindow.document.write('</table>');
//     billWindow.document.write(`<h2>Total: ₹${billDetails.reduce((sum, item) => sum + item.total, 0)}</h2>`);
//     billWindow.document.write('</body></html>');
//     billWindow.document.close();
//     billWindow.print();
// }


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
