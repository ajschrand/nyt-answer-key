function loadGame(game) {
    window.location.href = `./${game}.html`;
}

document.addEventListener('DOMContentLoaded', () => {
    let currentRow = document.querySelector('.wordle-row');
    let currentBoxIndex = 0;

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Backspace') {
            if (currentBoxIndex > 0) {
                currentBoxIndex--;
                currentRow.children[currentBoxIndex].textContent = '';
            }
        } else if (event.key === 'Enter') {
            if (currentBoxIndex === 5) {
                lockRow(currentRow);
                addNewRow();
            }
        } else if (/^[a-zA-Z]$/.test(event.key)) {
            if (currentBoxIndex < 5) {
                currentRow.children[currentBoxIndex].textContent = event.key.toUpperCase();
                currentBoxIndex++;
            }
        } 
    });

    function addNewRow() {
        const newRow = document.createElement('div');
        newRow.className = 'wordle-row';
        for (let i = 0; i < 5; i++) {
            const newBox = document.createElement('div');
            newBox.className = 'wordle-box';
            newBox.addEventListener('click', cycleBoxColor);
            newRow.appendChild(newBox);
        }
        document.getElementById('wordle-container').appendChild(newRow);
        currentRow = newRow;
        currentBoxIndex = 0;
    }

    function cycleBoxColor(event) {
        const box = event.target;
        if (box.classList.contains('cycle-2')) {
            box.classList.remove('cycle-2');
        } else if (box.classList.contains('cycle-1')) {
            box.classList.remove('cycle-1');
            box.classList.add('cycle-2');
        } else {
            box.classList.add('cycle-1');
        }
    }

    function lockRow(row) {
        for (let i = 0; i < row.children.length; i++) {
            const box = row.children[i];
            box.removeEventListener('click', cycleBoxColor);
            box.style.cursor = 'default';
        }
    }

    // Add click event listener to initial boxes
    const initialBoxes = document.querySelectorAll('.wordle-box');
    initialBoxes.forEach(box => box.addEventListener('click', cycleBoxColor));
});
