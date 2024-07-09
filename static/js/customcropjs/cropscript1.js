document.addEventListener('DOMContentLoaded', function () {
    let cropper;
    const imageInput = document.getElementById('edit_picture');
    const cropperModal = $('#cropperModal');
    const imageToCrop = document.getElementById('image_to_crop');
    const cropImageBtn = document.getElementById('cropImageBtn');
    const currentPicture = document.getElementById('current_picture');

    imageInput.addEventListener('change', function (event) {
        const reader = new FileReader();
        reader.onload = function (e) {
            imageToCrop.src = e.target.result;
            currentPicture.src = e.target.result;
            cropperModal.modal('show');
            cropper = new Cropper(imageToCrop, {
                aspectRatio: 0,
                viewMode: 1,
            });
        };
        reader.readAsDataURL(event.target.files[0]);
    });

    document.getElementById('btn-crop').addEventListener('click', function () {
        cropperModal.modal('show');
    });

    cropImageBtn.addEventListener('click', function () {
        const croppedCanvas = cropper.getCroppedCanvas();
        const croppedImage = croppedCanvas.toDataURL('image/png');

        currentPicture.src = croppedImage;
        document.querySelector('.cropped-container').style.display = 'flex';

        // Convert base64 image to file and replace the file input with the cropped image
        const byteString = atob(croppedImage.split(',')[1]);
        const ab = new ArrayBuffer(byteString.length);
        const ia = new Uint8Array(ab);
        for (let i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        const blob = new Blob([ab], { type: 'image/png' });
        const file = new File([blob], 'cropped_image.png', { type: 'image/png' });

        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        imageInput.files = dataTransfer.files;

        cropperModal.modal('hide');
        cropper.destroy();
    });
});
