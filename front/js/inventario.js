document.addEventListener("DOMContentLoaded", () => {
    
    // 1. FILTRADO: Búsqueda en tiempo real
    const searchInput = document.getElementById('input-search-product');
    const tableRows = document.querySelectorAll('#table-inventory tbody tr');

    if (searchInput) {
        searchInput.addEventListener('input', () => {
            const searchTerm = searchInput.value.toLowerCase();
            
            tableRows.forEach(row => {
                const rowText = row.innerText.toLowerCase();
                row.style.display = rowText.includes(searchTerm) ? '' : 'none';
            });
        });
    }

    const filterCategory = document.getElementById('filter-category');
    const filterStatus = document.getElementById('filter-status');

    function applyFilters() {
        const catValue = filterCategory.value;
        const statusValue = filterStatus.value;

        tableRows.forEach(row => {
           
            const cat = row.cells[2].innerText.toLowerCase();
            const status = row.cells[6].innerText.toLowerCase(); 

            const matchesCat = (catValue === 'todos' || cat.includes(catValue));
            const matchesStatus = (statusValue === 'todos' || status.includes(statusValue));

            row.style.display = (matchesCat && matchesStatus) ? '' : 'none';
        });
    }

    if (filterCategory) filterCategory.addEventListener('change', applyFilters);
    if (filterStatus) filterStatus.addEventListener('change', applyFilters);

    const deleteButtons = document.querySelectorAll('.action-delete');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            if(confirm("¿Estás seguro de dar de baja este producto?")) {
                e.target.closest('tr').remove();
            }
        });
    });
});