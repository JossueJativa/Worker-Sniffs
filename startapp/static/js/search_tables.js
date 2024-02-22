try{document.getElementById("inpSearch5").addEventListener("input", e => {
    const searchInput = e.target.value.toLowerCase();
    
    // Buscar en la tabla de callcenters
    searchTable("searchtable_callcenters", searchInput, 5); // Indicar la columna a buscar
    
    // Buscar en la tabla de tecnics
    searchTable("searchtable_tecnics", searchInput, 5); // Indicar la columna a buscar
});
}catch(e){}

try{document.getElementById("inpSearch1").addEventListener("input", e => {
    const searchInput = e.target.value.toLowerCase();
    
    // Buscar en la tabla de callcenters
    searchTable("searchtable_callcenters", searchInput, 1);
});
}catch(e){}

try{document.getElementById("inpSearch2").addEventListener("input", e => {
    const searchInput = e.target.value.toLowerCase();
    
    // Buscar en la tabla de callcenters
    searchTable("searchtable_callcenters", searchInput, 2);
});
}catch(e){}

try{
    document.addEventListener('DOMContentLoaded', function () {
        var checkboxes = document.querySelectorAll('.checkbox-producto');
        var totalPriceInput = document.getElementById('total_price');

        checkboxes.forEach(function (checkbox) {
            checkbox.addEventListener('change', function () {
                updateTotalPrice();
            });
        });

        function updateTotalPrice() {
            var totalPrice = 0;
            checkboxes.forEach(function (checkbox) {
                if (checkbox.checked) {
                    totalPrice += parseFloat(checkbox.getAttribute('data-precio'));
                }
            });
            totalPrice = totalPrice*1.12;
            totalPriceInput.value = totalPrice.toFixed(2); // Ajusta el número de decimales según sea necesario
        }
    });
}catch(e){}

function searchTable(tableId, searchInput, columnIndex) {
    const tabla = document.getElementById(tableId);
    const tr = tabla.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++) {
        const td = tr[i].getElementsByTagName("td")[columnIndex]; // Utilizar el índice de la columna
        
        if (td) {
            const txtValue = td.textContent || td.innerText;
            const txtValueLowerCase = txtValue.toLowerCase();

            if (txtValueLowerCase.includes(searchInput)) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

try{
    window.onload = function() {
        var installationDate = new Date(document.getElementById('date_instalation').value);
        var today = new Date();
        var timeDifference = installationDate.getTime() - today.getTime();
        var daysDifference = Math.floor(timeDifference / (1000 * 3600 * 24));
        document.getElementById('days_since_installation').value = daysDifference;
    }
}
catch(e){}