import React, { useEffect, useState } from "react";
import axios from 'axios';
import Swal from 'sweetalert2';
import style from './addclient.module.css';
import { MdCloudUpload } from "react-icons/md";
import { getStorage, ref, uploadBytesResumable, getDownloadURL } from "firebase/storage";
import { app } from "../../../firebase";
import Button from "../../atoms/buttons/Button";
import { API_URL } from "../../../constants/WebsiteConstants";
import { useNavigate } from 'react-router-dom'; // Import useNavigate

const AddClient = ({ onClose }) => {
    const [Image, setImage] = useState(null);
    const [imageUrl, setImageUrl] = useState("");
    const [error, setError] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);
    const navigate = useNavigate();

    useEffect(() => {
        if (Image) {
            uploadFile(Image);
        }
    }, [Image]);

    const uploadFile = (file) => {
        const storage = getStorage(app);
        const storageRef = ref(storage, 'Team/' + file.name);
        const uploadTask = uploadBytesResumable(storageRef, file);

        uploadTask.on('state_changed',
            (snapshot) => {
                const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
                setUploadProgress(progress);
                console.log('Upload is ' + progress + '% done');
            },
            (error) => {
                console.error('Error uploading file:', error);
            },
            () => {
                getDownloadURL(uploadTask.snapshot.ref).then((downloadURL) => {
                    setImageUrl(downloadURL);
                    console.log('File available at', downloadURL);
                    setUploadProgress(0);
                });
            }
        );
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
    
        if (!imageUrl) {
            setError(true);
            return; // Stop submission if image URL is not ready
        }
    
        const formData = new FormData();
        formData.append('image', Image); // Image file
        // Add other necessary fields if required by your serializer
        // e.g., formData.append('otherField', value);
    
        try {
            const response = await axios.post(`${API_URL}/api/team/add-partner/`, formData, {
                headers: {
                    'Authorization': localStorage.getItem('token'),
                    'Content-Type': 'multipart/form-data' // Set content type
                }
            });
    
            if (response.data.status === "success") {
                Swal.fire('Add New Partner!', 'You have successfully added a new Partner.', 'success');
                navigate('/'); // Navigate to the "/" URL
                onClose();
            } else {
                Swal.fire('Error', response.data.errors.image ? response.data.errors.image[0] : 'Failed to submit data. Please try again.', 'error');
            }
        } catch (error) {
            console.error("Error submitting data: ", error);
            Swal.fire('FAILED!', 'An error occurred while submitting the data. <br /> Please check your internet connection and try again.', 'error');
        }
    };
    
    const overlayStyle = {
        position: 'fixed',
        top: '0',
        left: '0',
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(0, 0, 0, 0.3)',
        zIndex: '999',
        backdropFilter: 'blur(1px)',
    };

    return (
        <>
            <div style={overlayStyle}></div>
            <div className={style.popupForm}>
                <h3>Add New Partner</h3>
                <div className={style.first_row}>
                    <div className={style.image}>
                        <input
                            type="file"
                            className={style.form_image}
                            id="Image"
                            name="Image"
                            accept="image/png, image/jpeg"
                            onChange={(e) => setImage(e.target.files[0])}
                        />

                        <div className={style.image_view}>
                            {Image ? (
                                <img
                                    src={URL.createObjectURL(Image)}
                                    alt="Uploaded"
                                />
                            ) : (
                                <div className={style.image_container}>
                                    <MdCloudUpload className={style.icon} />
                                    <p>Click here to upload an image</p>
                                </div>
                            )}
                        </div>
                        {error && !Image && <span className={style.text_danger}>Please select an image.</span>}
                    </div>

                    {/* Progress Bar */}
                    {uploadProgress > 0 && (
                        <div className={style.progressBarContainer}>
                            <div className={style.progressBar} style={{ width: `${uploadProgress}%` }}></div>
                        </div>
                    )}

                    <div className={style.row}>
                        <Button
                            btnClick={onClose}
                            btnText="CANCEL"
                            size="14px"
                            secondary
                            radius="5px"
                        />

                        <Button
                            btnClick={handleSubmit}
                            btnText="SUBMIT"
                            size="14px"
                            primary
                            radius="5px"
                        />
                    </div>
                </div>
            </div>
        </>
    );
};

export default AddClient;
