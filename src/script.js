document.getElementById('calculate').addEventListener('click', function(e) {
    e.preventDefault();

    const num1 = parseFloat(document.getElementById('num1').value);
    const num2 = parseFloat(document.getElementById('num2').value);
    const operation = document.getElementById('operation').value;

    let result;

    if (isNaN(num1) || isNaN(num2)) {
        result = "Erreur: Valeur invalide";
    } else {
        switch(operation) {
            case 'add':
                result = num1 + num2;
                break;
            case 'subtract':
                result = num1 - num2;
                break;
            case 'multiply':
                result = num1 * num2;
                break;
            case 'divide':
                result = num2 !== 0 ? num1 / num2 : 'Erreur: Division par zéro';
                break;
        }
    }

    document.getElementById('result').textContent = `Résultat: ${result}`;
});
