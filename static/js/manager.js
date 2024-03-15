function previewImage(input) {
    var preview = document.getElementById('preview');
    var previewContainer = document.getElementById('imagePreview');
    
    // Verificar si se seleccionó un archivo
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result;
            previewContainer.style.display = 'block'; // Mostrar el contenedor de la vista previa
        };

        reader.readAsDataURL(input.files[0]);
    } else {
        preview.src = '';
        previewContainer.style.display = 'none'; // Ocultar el contenedor de la vista previa si no hay archivo seleccionado
    }
}

function togglePasswordVisibility(inputId) {
    var passwordInput = document.getElementById(inputId);
    var toggleButton = document.querySelector(`[onclick="togglePasswordVisibility('${inputId}')"]`);

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleButton.innerHTML = `
            <span class="material-symbols-outlined">
                visibility_off
            </span>
        `;
    } else {
        passwordInput.type = "password";
        toggleButton.innerHTML = `
            <span class="material-symbols-outlined">
                visibility
            </span>
        `;
    }
}

function editWorker(id) {
    var urlUser = `http://127.0.0.1:8000/api/user/${id}`;
    fetch(urlUser)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            document.getElementById('background').style.display = 'block';
            var edit_container = document.getElementById('edit_container');

            edit_container.innerHTML =
            `
            <h3 class="title_edit">Cambiar estado del trabajador</h3>
            <div class="edit_info">
                <input type="text" name="id" id="id" class="form-control" value="${data.id}" hidden>
                <div class="input_info">
                    <label for="first_name">Nombre/s</label>
                    <input type="text" name="first_name" id="first_name" class="form-control" value="${data.first_name}" required>
                </div>
                <div class="input_info">
                    <label for="last_name">Apellido/s</label>
                    <input type="text" name="last_name" id="last_name" class="form-control" value="${data.last_name}" required>
                </div>
                <div class="input_info">
                    <label for="email">Email</label>
                    <input type="text" name="email" id="email" class="form-control" value="${data.email}" required>
                </div>
                <div class="input_info">
                    <label for="identity">Cédula/RUC/Pasaporte</label>
                    <input type="text" name="identity" id="identity" class="form-control" value="${data.identity}" required>
                </div>
                <div class="input_info">
                    <label for="phone">Celular</label>
                    <input type="text" name="phone" id="phone" class="form-control" value="${data.phone}" required>
                </div>
                <div class="input_info">
                    <label for="status">Seleccionar estado</label>
                    <select name="status" id="status" required>
                        <option value="0">Seleccionar</option>
                        <option value="Disponible" ${data.work_status === "Disponible" ? 'selected' : ''}>Disponible</option>
                        <option value="Despedido" ${data.work_status === "Despedido" ? 'selected' : ''}>Despedido</option>
                        <option value="Vacaciones" ${data.work_status === "Vacaciones" ? 'selected' : ''}>Vacaciones</option>
                        <option value="Enfermo" ${data.work_status === "Enfermo" ? 'selected' : ''}>Enfermo</option>
                        <option value="Re-ingreso" ${data.work_status === "Re-ingreso" ? 'selected' : ''}>Re-ingreso</option>
                        <option value="Pasante" ${data.work_status === "Pasante" ? 'selected' : ''}>Pasante</option>
                        <option value="Interno" ${data.work_status === "Interno" ? 'selected' : ''}>Interno</option>
                    </select>
                </div>
            </div>
            <div class="buttons_edit">
                <button type="submit" class="btn btn-success">Guardar</button>
                <button type="reset" class="btn btn-danger" onclick="closeEdit()">Cancelar</button>
            </div>
            `;
        })
}

function closeEdit(){
    document.getElementById('background').style.display = 'none';
}

function editClient(id) {
    var urlClient = `http://127.0.0.1:8000/api/client/${id}`;

    fetch(urlClient)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            document.getElementById('background').style.display = 'block';
            var edit_container = document.getElementById('edit_container');

            edit_container.innerHTML =
            `
            <h3 class="title_edit">Editar información del cliente</h3>
            <div class="edit_info">
                <input type="text" name="id" id="id" class="form-control" value="${data.id}" hidden>
                <div class="input_info">
                    <label for="username">Usuario</label>
                    <input type="text" name="username" id="username" class="form-control" value="${data.username}" required>
                </div>
                <div class="input_info">
                    <label for="identity">Cédula/RUC/Pasaporte</label>
                    <input type="text" name="identity" id="identity" class="form-control" value="${data.identity}" required>
                </div>
                <div class="input_info">
                    <label for="phone">Celular</label>
                    <input type="text" name="phone" id="phone" class="form-control" value="${data.phone}" required>
                </div>
                <div class="input_info">
                    <label for="date_instalation">Escoger fecha de instalación</label>
                    <input type="date" name="date_instalation" id="date_instalation" class="form-control" value="${data.date_instalation}" required>
                </div>
                <div class="input_info">
                    <label for="phone">Parte del día</label>
                    <select name="part_of_day" id="part_of_day" class="select_worker">
                        <option value="0">Seleccionar</option>
                        <option value="mañana" ${data.part_of_day === "mañana" ? 'selected' : ''}>Mañana</option>
                        <option value="tarde" ${data.part_of_day === "tarde" ? 'selected' : ''}>Tarde</option>
                    </select>
                </div>
                <div class="input_info">
                    <label for="options_to_give_instalation">Parte del día</label>
                    <select name="options_to_give_instalation" id="options_to_give_instalation" class="select_worker">
                        <option value="0">Seleccionar</option>
                        <option value="Recoger" ${data.options_to_give_instalation === "Recoger" ? 'selected' : ''}>Recoger</option>
                        <option value="Delivery" ${data.options_to_give_instalation === "Delivery" ? 'selected' : ''}>Delivery</option>
                    </select>
                </div>
            </div>
            <div class="buttons_edit">
                <button type="submit" class="btn btn-success">Guardar</button>
                <button type="reset" class="btn btn-danger" onclick="closeEdit()">Cancelar</button>
            </div>
            `
        })
}