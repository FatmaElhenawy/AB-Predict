function looadExample() {
    document.getElementById('id_BWindow').value = 'GSYRYDGGF';
    document.getElementById('id_AWindow').value = 'NPRPNDPTV';
    document.getElementById('id_BSec').value = 'T|T|T|S|S|-|S|-|E'
    document.getElementById('id_ASec').value = 'S|S|-|-|-|-|-|S|S'
    document.getElementById('id_BSol').value = '0.|0.253814285746|0.36036|0.455645|0.031532|0.202454|0.154762|0.011905|0.005076'
    document.getElementById('id_ASol').value ='0.019108|0.183824|0.020161|0.0|0.076433|0.184049|0.014706|0.514085|0.5'
    document.getElementById('id_CDR').value = '1';
    document.getElementById('id_Type').value = 'H';
}

function cleearInputs() {
    document.getElementById('prediction--form').reset();
    document.querySelectorAll('.error-message').forEach(element => element.innerHTML = '');
    document.getElementById('result').innerHTML = '';
}

function validateForm2() {
    const type = document.getElementById('id_Type').value;
    const cdr = document.getElementById('id_CDR').value;
    const bWindow = document.getElementById('id_BWindow').value.toUpperCase();
    const aWindow = document.getElementById('id_AWindow').value.toUpperCase();
    const bSec = document.getElementById('id_BSec').value.toUpperCase();
    const aSec = document.getElementById('id_ASec').value.toUpperCase();
    const bSol = document.getElementById('id_BSol').value;
    const aSol = document.getElementById('id_ASol').value;

    //validation functions
    function isValidType(type) {
        return type === 'H' || type === 'L';
    }

    function isValidCDR(cdr) {
        const cdrInt = parseInt(cdr);
        return !isNaN(cdrInt) && cdrInt >= 1 && cdrInt <= 3;
    }

    function isValidAminoAcidSequence(sequence) {
        const validAminoAcids = /^[ARNDCEQGHILKMFPSTWYV]+$/;
        return sequence.length === 9 && sequence.match(validAminoAcids);
    }

    function isValidSecondaryStructure(sequence) {
        const validSecondaryStructures = /^[HBEGITS\-]+$/;
        return sequence.length === 9 && sequence.match(validSecondaryStructures);
    }

    function isValidSolventAccessibility(values) {
        const validFloatValues = /^(\d+(\.\d+)?\|?)+$/;
        return values.split('|').length === 9 && values.match(validFloatValues);
    }

    //clear previous error messages

    document.querySelectorAll('.error-message').forEach(element => element.innerHTML = '');
    
   
    //validate each field
    let isValid = true;
   

    if (!isValidType(type)) {
        document.getElementById('type_error').innerHTML = 'Invalid type. Please select either "H" or "L".';
        isValid = false;
    }
    if (!isValidCDR(cdr)) {
        document.getElementById('cdr_error').innerHTML = 'Invalid CDR. Please select a number between 1 and 3.';
        isValid = false;
    }
    if (!isValidAminoAcidSequence(bWindow)) {
        document.getElementById('b_window_error').innerHTML = 'Invalid BWindow. It should be a 9-character sequence of valid amino acids.';
        isValid = false;
    }
    if (!isValidAminoAcidSequence(aWindow)) {
        document.getElementById('a_window_error').innerHTML = 'Invalid AWindow. It should be a 9-character sequence of valid amino acids.';
        isValid = false;
    }
    if (!isValidSecondaryStructure(bSec)) {
        document.getElementById('b_sec_error').innerHTML = 'Invalid BSec. It should be a 9-character sequence of valid secondary structure labels.';
        isValid = false;
    }
    if (!isValidSecondaryStructure(aSec)) {
        document.getElementById('a_sec_error').innerHTML = 'Invalid ASec. It should be a 9-character sequence of valid secondary structure labels.';
        isValid = false;
    }
    if (!isValidSolventAccessibility(bSol)) {
        document.getElementById('b_sol_error').innerHTML = 'Invalid BSol. It should be 9 float values separated by "|".';
        isValid = false;
    }
    if (!isValidSolventAccessibility(aSol)) {
        document.getElementById('a_sol_error').innerHTML = 'Invalid ASol. It should be 9 float values separated by "|".';
        isValid = false;
    }

    if (isValid) {
        shhowResult();
    }
}


function shhowResult() {
    const r = document.getElementById('result').value;
    const result = ` 
        <p><strong>Prediction Result For Model2 is:</strong> ${r}</p>
    `;

    document.getElementById('result').innerHTML = result;
    cleearInputs()
}