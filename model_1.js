function loadExample() {
    document.getElementById('id_H_CDR1').value = 'GYTFSDYWIE';
    document.getElementById('id_H_CDR2').value = 'EILPGSGSTNYHERFKG';
    document.getElementById('id_H_CDR3').value = 'GNYDFDG';
    document.getElementById('id_L_CDR1').value = 'SASSSVNYMY';
    document.getElementById('id_L_CDR2').value = 'DTSKLAS';
    document.getElementById('id_L_CDR3').value = 'QQWGRNPT';
    document.getElementById('id_Epitope').value = 'TTYQMDVNPEGKYSFADSYEMEEDGVRKCEGPSDSFTHTPPLDPQPENRTDTKQHEISDVIGTSGQKTKSNRGENSCKAEGCWGPEPRDCREGPREFVECTGRGPDNCCVAGVMGE';
}


function clearInputs2() {
    document.getElementById('prediction-form').reset();
    document.querySelectorAll('.error-message').forEach(element => element.innerHTML = '');
    document.getElementById('result').innerHTML = '';
}

function validateAndShowResult() {
    const inputs = document.querySelectorAll('#prediction-form input');
    const maxLength = 515;
    const regex =  /^[ABCDEFGHIKLMNPQRSTVWY]+$/;
    let valid = true;
    

    inputs.forEach(input => {
        const errorElement = document.getElementById(`${input.id}_error`);
        errorElement.innerHTML = '';

        if (!input.value) {
            valid = false;
            errorElement.innerHTML = 'This field is required.';
        } else if (input.value.length > maxLength) {
            valid = false;
            errorElement.innerHTML = `Input must not exceed ${maxLength} characters.`;
        } else if (!regex.test(input.value)) {
            valid = false;
            errorElement.innerHTML = 'Input must only contain uppercase alphabetic characters.';
        }
    });

    if (valid) {
        showResult();
    }
}

function showResult() {
    const r = document.getElementById('result').value;
    const result = ` 
        <p><strong>Prediction Result For Model1 is:</strong> ${r}</p>
    `;

    document.getElementById('result').innerHTML = result;
    clearInputs();
}


