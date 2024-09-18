function updateTotal() {
    const tableBody = document.getElementById('productTableBody');
    const rows = tableBody.getElementsByTagName('tr');
    let total = 0;
    
    for (let i = 0; i < rows.length; i++) {
        const priceCell = rows[i].getElementsByTagName('td')[1];
        if (priceCell) {
            const priceValue = parseFloat(priceCell.textContent);
            if (!isNaN(priceValue)) {
                total += priceValue;
            }
        }
    }

    document.getElementById('totalAmount').textContent = total.toFixed(2);
}

function addProductToTable() {
    const productName = document.getElementById('productName').value;
    const productPrice = document.getElementById('productPrice').value;

    if (productName && productPrice) {
        const tableBody = document.getElementById('productTableBody');
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <th scope="row">${tableBody.children.length + 1}</th>
            <td>${productName}</td>
            <td>${productPrice}</td>
            <td>
                <button type="button" class="btn btn-danger delete-btn"><i class="fa-solid fa-trash"></i></button>
            </td>
        `;
        tableBody.appendChild(newRow);

        document.getElementById('productName').value = '';
        document.getElementById('productPrice').value = '';

        const deleteButton = newRow.querySelector('.delete-btn');
        deleteButton.addEventListener('click', function () {
            tableBody.removeChild(newRow);
            updateTotal();
        });

        updateTotal();
    }
}


document.getElementById('productForm').addEventListener('submit', function (event) {
    event.preventDefault();
    addProductToTable();
});

document.getElementById('generateInvoice').addEventListener('click', function () {
    const totalAmount = document.getElementById('totalAmount').textContent;
    const tableBody = document.getElementById('productTableBody');
    const invoiceTableBody = document.getElementById('invoiceTableBody');
    invoiceTableBody.innerHTML = '';

    for (const row of tableBody.children) {
        const productName = row.getElementsByTagName('td')[0].textContent;
        const productPrice = row.getElementsByTagName('td')[1].textContent;

        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${productName}</td>
            <td>${productPrice}</td>
        `;
        invoiceTableBody.appendChild(newRow);
    }

    document.getElementById('invoiceTotal').textContent = totalAmount;

    $('#invoiceModal').modal('show');
});

function printInvoice() {
    const invoiceContent = document.querySelector('.invoice').innerHTML;

    const printWindow = window.open('', '', 'width=600,height=600');
    printWindow.document.open();
    printWindow.document.write('<html><head><title>Invoice</title></head><body>');
    printWindow.document.write(invoiceContent);
    printWindow.document.write('</body></html>');
    printWindow.document.close();

    printWindow.print();

    printWindow.close();
}

document.getElementById('printButton').addEventListener('click', function () {
    printInvoice();
});

