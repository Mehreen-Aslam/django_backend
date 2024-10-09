import React, { useState } from "react";
import axios from "axios";
import styles from "./otp.module.css";
import { API_URL } from "../../../constant/WebsiteConstants";
import Swal from "sweetalert2";

function OTP({ email, closeModal }) {
  const [otp, setOtp] = useState(["", "", "", ""]);

  const handleChange = (e, index) => {
    const value = e.target.value;
    if (value.length <= 1) {
      const newOtp = [...otp];
      newOtp[index] = value;
      setOtp(newOtp);

      if (value && index < 3) {
        document.getElementById(`otp-input-${index + 1}`).focus();
      }
    }
  };

  const handleSubmit = async () => {
    const enteredOtp = otp.join("");  // Joining the array to form a string

    try {
        console.log(email, enteredOtp);
        const response = await axios.post(`${API_URL}/api/verify-otp/`, {
            email,
            otp: enteredOtp,  // Send OTP as a string
        }, {
            headers: {
                "Content-Type": "application/json",  // Ensure the correct content type
            },
        });

        console.log("API response:", response);

        if (response.data.success || response.data.status === "success") {
            Swal.fire("OTP Verified!", "Your account has been verified.", "success");
            closeModal(); // Close the modal and reload the page
            window.location.reload(); // Reload the page
        } else if (response.data.message) {
            Swal.fire("OTP Verification Failed", response.data.message, "error");
        } else {
            Swal.fire("OTP Verification Failed", "Please try again.", "error");
        }
    } catch (error) {
        console.error("Error:", error);
        Swal.fire("Error", "Failed to verify OTP. Please try again.", "error");
    }
};


  return (
    <div className={styles.otpContainer}>
      <h2>Check your Email</h2>
      <p>Enter the 4 digit code sent to your email</p>
      <div className={styles.otpInputs}>
        {otp.map((digit, index) => (
          <input
            key={index}
            id={`otp-input-${index}`}
            type="text"
            maxLength="1"
            value={digit}
            onChange={(e) => handleChange(e, index)}
            className={styles.otpInput}
          />
        ))}
      </div>
      <button onClick={handleSubmit} className={styles.submitOtpBtn}>
        Confirm OTP
      </button>
    </div>
  );
}

export default OTP;

