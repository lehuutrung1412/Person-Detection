const dropArea = document.querySelector('.dropArea'),
input = dropArea.querySelector('input');
const imgResult = document.querySelector('#result');
const dropAreaChild = document.querySelector('.dropArea-child');
const detail = document.querySelector('#detail');
let resultBox = document.querySelector("#resultBox");
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
    dropAreaChild.classList.add("active");
});

dropArea.addEventListener("dragleave", () => {
    dropAreaChild.classList.remove("active");
});

dropArea.addEventListener("drop", (event) => {
    event.preventDefault();
    file = event.dataTransfer.files[0];
    upload();
});

function upload(){
    resultBox.classList.add("d-none");
    detail.innerHTML = 'Detecting . . .';
    let fileType = file.type;
    let validExt = ["image/jpeg", "image/jpg", "image/png"];
    if (validExt.includes(fileType)){
        let fileForm = new FormData();
        if (file){
            fileForm.append('file', file);
        }
        // console.log(file);
        // let fileForm = {image: file};
        // console.log(fileForm);
        $.ajax({
            method: 'POST',
            url: '/upload',
            data: fileForm,
            processData: false,
            cache: false,
            contentType: false,
            success: function (response){
                if (response){
                    // console.log(response);
                    let bytestring = response['status'];
                    let image = 'data:image/jpeg;base64,' + bytestring.split('\'')[1];
                    imgResult.src = image;
                    resultBox.classList.remove("d-none");
                    dropAreaChild.classList.remove("active");
                    detail.innerHTML = 'Upload your image';
                }
                else{
                    console.log('No response');
                    alert('No response');
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    }
    else{
        alert("Vui lòng tải lên file ảnh");
        dropAreaChild.classList.remove("active");
        resultBox.classList.remove("d-none");
        detail.innerHTML = 'Upload your image';
    }
}