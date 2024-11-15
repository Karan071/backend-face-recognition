import React, { useState, useRef, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

const VisitorCheckIn = () => {
  const navigate = useNavigate();
  const [localPhoto, setLocalPhoto] = useState(null);
  const [localFormData, setLocalFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phoneNumber: "",
    purpose: "",
    meetingWith: "",
  });

  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    const startWebcam = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoRef.current.srcObject = stream;
      } catch (err) {
        console.error("Error accessing webcam:", err);
      }
    };

    startWebcam();

    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        const stream = videoRef.current.srcObject;
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
      }
    };
  }, []);

  const capturePhoto = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const capturedPhoto = canvas.toDataURL("image/png");
    setLocalPhoto(capturedPhoto);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    const updatedData = { ...localFormData, [name]: value };
    setLocalFormData(updatedData);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate('/confirmation-visitor', {
      state: {
        visitorPhoto: localPhoto,
        visitorName: {
          firstName: localFormData.firstName,
          lastName: localFormData.lastName
        }
      }
    });
  };

  return (
    <div className="font-poppins bg-gray-50 min-h-screen flex justify-center items-center">
      <div className="w-full max-w-3xl p-6 bg-white rounded-lg shadow-lg">
        <h1 className="text-4xl font-bold text-center mb-6">Visitor Check-In</h1>

        {!localPhoto ? (
          <div>
            <div className="flex justify-center mb-6">
              <video ref={videoRef} autoPlay className="border-2 rounded-lg w-80 h-80" />
            </div>
            <div className="flex justify-center mb-4">
              <button
                type="button"
                onClick={capturePhoto}
                className="px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors duration-300"
              >
                Capture Photo
              </button>
            </div>
          </div>
        ) : (
          <div className="flex justify-center mb-6">
            <img
              src={localPhoto}
              alt="Captured Preview"
              className="w-32 h-32 rounded-lg object-cover border-2 border-gray-300 shadow-md"
            />
          </div>
        )}

        <form className="space-y-6" onSubmit={handleSubmit}>
          <div className="flex gap-4 mb-4">
            <input
              type="text"
              name="firstName"
              value={localFormData.firstName}
              onChange={handleChange}
              placeholder="First Name"
              className="w-1/2 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
            />
            <input
              type="text"
              name="lastName"
              value={localFormData.lastName}
              onChange={handleChange}
              placeholder="Last Name"
              className="w-1/2 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="flex gap-4 mb-4">
            <input
              type="email"
              name="email"
              value={localFormData.email}
              onChange={handleChange}
              placeholder="Email"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
            />
            <input
              type="text"
              name="phoneNumber"
              value={localFormData.phoneNumber}
              onChange={handleChange}
              placeholder="Phone Number"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
            />
          </div>

          <select
            name="purpose"
            value={localFormData.purpose}
            onChange={handleChange}
            className="w-full px-4 py-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
          >
            <option value="" disabled>Purpose Of Visit</option>
            <option value="meeting">Meeting</option>
            <option value="delivery">Delivery</option>
            <option value="interview">Interview</option>
            <option value="other">Other</option>
          </select>


          <input
            type="text"
            name="meetingWith"
            value={localFormData.meetingWith}
            onChange={handleChange}
            placeholder="Meeting With"
            className="w-full px-4 py-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
          />

          <button
            type="submit"
            className="w-full px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors duration-300 mt-10"
          >
            Submit
          </button>
        </form>
      </div>
      <canvas ref={canvasRef} className="hidden" />
    </div>
  );
};

export default VisitorCheckIn;
