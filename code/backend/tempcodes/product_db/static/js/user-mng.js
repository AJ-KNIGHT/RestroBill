
//    <a href="/update/{{ user.id }}" id="update-popup" class="btn btn-edit">Edit</a>
//    <a href="/delete/{{ user.id }}" class="btn btn-delete">Delete</a>
// user table
function fetchUsers() {
    fetch('/users/get_users')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const userList = document.getElementById('user-list');
            userList.innerHTML = ''; // Clear the existing rows

            data.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.username}</td>
                    <td>
                        <a href="#" class="btn btn-edit" data-user-id="${user.uid}">Edit</a>
                        <a href="/delete/${user.uid}" class="btn btn-delete">Delete</a>
                    </td>
                `;
                userList.appendChild(row); // Append the row to the table body
            });
        })
        .catch(error => {
            console.error('Error fetching user data:', error); // Log any errors
        });
}

// Popup logic
document.addEventListener('DOMContentLoaded', function () {
    fetchUsers();

    let insert_popup = document.querySelector('.popup-container-insert');
    let update_popup = document.querySelector('.popup-container-update');

    // Insert popup
    document.getElementById('insert-popup').addEventListener('click', function () {
        insert_popup.style.display = 'flex';
        document.querySelector('.main').classList.add('show');
    });

    document.getElementById('close-popup-insert').addEventListener('click', function () {
        insert_popup.style.display = 'none';
        document.querySelector('.main').classList.remove('show');
    });

    // Event delegation for dynamically created "Edit" buttons
    document.getElementById('user-list').addEventListener('click', function (event) {
        if (event.target.classList.contains('btn-edit')) {
            event.preventDefault(); // Prevent the default anchor behavior
            const userId = event.target.getAttribute('data-user-id'); // Get the user ID
            // Open the update popup and load user data if necessary
            update_popup.style.display = 'flex';
            document.querySelector('.main').classList.add('show');
            console.log('Editing user with ID:', userId);
            // Load user data for editing here if needed
        }
    });
});
