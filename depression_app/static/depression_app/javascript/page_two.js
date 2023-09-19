let click_to_record = document.getElementById("click_to_record");
click_to_record.addEventListener('click',function(){
    window.SpeechRecognition = window.webkitSpeechRecognition;

    const recognition = new SpeechRecognition();
    recognition.interimResults = true;
    recognition.maxAlternatives = 10;

    recognition.addEventListener('result', e => {
        let transcript = Array.from(e.results)
            .map(result => result[0])
            .map(result => result.transcript)
            .join('')
        document.getElementById("convert_text").innerHTML = transcript;
        console.log(transcript);
    });
    
    recognition.start();
});