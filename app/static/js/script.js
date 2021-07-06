const dropArea = document.querySelector('.dropArea'),
input = dropArea.querySelector('input');
const imgResult = document.querySelectorAll('.result');
const dropAreaChild = document.querySelector('.dropArea-child');
const detail = document.querySelector('#detail');
const resultBox = document.querySelectorAll(".resultBox");
const cloud = document.querySelector(".cloud");
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
    // resultBox.classList.add("d-none");
    resultBox.forEach(rb => {rb.classList.add("d-none");});
    detail.innerHTML = 'Detecting . . .';
    cloud.classList.remove("animated", "infinite", "bounce");
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
                    let bytestring = response['img_hog'];
                    let image_hog = 'data:image/jpeg;base64,' + bytestring.split('\'')[1];
                    let bytestring_ = response['img_yolo'];
                    let image_yolo = 'data:image/jpeg;base64,' + bytestring_.split('\'')[1];
                    imgResult[0].src = image_hog;
                    imgResult[1].src = image_yolo;
                    resultBox.forEach(rb => {rb.classList.remove("d-none");});
                    dropAreaChild.classList.remove("active");
                    cloud.classList.add("animated", "infinite", "bounce");
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
        resultBox.forEach(rb => {rb.classList.remove("d-none");});
        cloud.classList.add("animated", "infinite", "bounce");
        detail.innerHTML = 'Upload your image';
    }
}