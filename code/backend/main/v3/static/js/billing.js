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
        document.querySelector(".list-items").style.display = "none";
        // Clear the input field, assuming `this` refers to the input field
        if (typeof this !== 'undefined' && this instanceof HTMLInputElement) {
            this.value = "";
        }
        cart[newSiNo] = {"pid": pid, "qty": quantity};
        qtyListeners();
        reIndexSiNumbers();
    }
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

        // container.addEventListener('click', handleQuantityChange);
        // container.querySelector('input').addEventListener('keypress', handleQuantityChange);
    });
}


function handleQuantityChange(event) {
    const container = event.currentTarget.closest('.number-input');
    const input = container.querySelector('input');
    let quantity = parseInt(input.value, 10);

    if (!isNaN(quantity)) {
        if (event.type === 'keypress' && event.key !== 'Enter') {
            // Ignore non-Enter keypresses
            return;
        } else if (event.type === 'keypress' && event.key === 'Enter') {
            newQuantity = input.value;

        } else {
            // Determine the change in quantity based on the event
            const change = event.target.classList.contains('minus') ? -1 : 1;
            const newQuantity = Math.max(quantity + change, 1); // Allow quantity to be zero
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
document.querySelector(".search input").addEventListener("keydown", function(event) {
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
    updateTotal(0);
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





// print 
document.getElementById("print").addEventListener("click", function() {
    console.log(cart);
    if (isCartEmpty(cart)) {
        alert("The cart is empty.");
    } else {
        $.ajax({
            url: "/print-bill",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(cart),
            dataType: "json",
            success: function(response) {
                console.log(response.message);
            },
            error: function(error) {
                // Handle the error based on the status code
                if (error.status === 401) {
                    alert("Access denied. Please log in.");
                }
            }
        });
    }
});


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