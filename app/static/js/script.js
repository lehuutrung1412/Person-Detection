const dropArea = document.querySelector('.dropArea'),
input = dropArea.querySelector('input');
const imgResult = document.querySelector('#result');
let file;

dropArea.onclick = ()=>{
    input.click();
}

input.addEventListener("change", function (){
    file = this.files[0];
    upload();
});

dropArea.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropArea.classList.add("active");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("active");
});

dropArea.addEventListener("drop", (event) => {
    event.preventDefault();
    file = event.dataTransfer.files[0];
    let fileType = file.type;
    let validExt = ["image/jpeg", "image/jpg", "image/png"];
    if (validExt.includes(fileType)){
        // alert("OK");
        upload();
    }
    else{
        alert("Vui lòng tải lên file ảnh");
        dropArea.classList.remove("active");
    }
});

function upload(){
    let fileForm = new FormData();
    if (file){
        fileForm.append('file', file);
    }
    console.log(file);
    // let fileForm = {image: file};
    console.log(fileForm);
    $.ajax({
        method: 'POST',
        url: '/upload',
        data: fileForm,
        processData: false,
        cache: false,
        contentType: false,
        success: function (response){
            if (response){
                console.log(response);
                let bytestring = response['status']
                let image = 'data:image/jpeg;base64,' + bytestring.split('\'')[1]
                imgResult.src = image
            }
            else{
                console.log('ko nhan dc phan hoi');
            }
        },
        error: function(error){
            console.log(error);
        }
    });
    let resultBox = document.querySelector("#resultBox");
    resultBox.classList.remove("d-none");
    dropArea.classList.remove("active");
}