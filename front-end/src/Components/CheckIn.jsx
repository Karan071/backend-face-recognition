import React, { useState, useRef, useEffect } from 'react';

const CheckIn = () => {
  const [photo, setPhoto] = useState(null);
  const [isPhotoCaptured, setIsPhotoCaptured] = useState(false);
  const videoRef = useRef(null); // Ref to access the video element
  const canvasRef = useRef(null); // Ref to capture image from video feed

  // Start webcam when component mounts
  useEffect(() => {
    const startWebcam = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
        });
        videoRef.current.srcObject = stream;
      } catch (err) {
        console.error("Error accessing webcam:", err);
      }
    };

    if (!isPhotoCaptured) {
      startWebcam();
    }

    // Clean up the webcam stream on component unmount
    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        const stream = videoRef.current.srcObject;
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
      }
    };
  }, [isPhotoCaptured]);

  // Capture photo from video stream
  const capturePhoto = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    setPhoto(canvas.toDataURL("image/png"));
    setIsPhotoCaptured(true);

    // Stop the video stream
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach(track => track.stop());
    }
  };

  const handleRetake = () => {
    setPhoto(null);
    setIsPhotoCaptured(false);
  };

  const handleContinue = () => {
    window.location.href = '/confirmation';
    console.log("Continue with photo:", photo);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Employees Check In</h1>
      
      {/* Webcam feed section */}
      <div className="flex justify-center mb-6">
        <video
          ref={videoRef}
          autoPlay
          className={`border-2 rounded-lg w-[640px] h-[480px] bg-black ${isPhotoCaptured ? 'hidden' : ''}`}
        />
      </div>

      {/* Capture photo button */}
      {!isPhotoCaptured && (
        <div className="flex justify-center mb-4">
          <button
            type="button"
            onClick={capturePhoto}
            className="px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors duration-300"
          >
            Capture Photo
          </button>
        </div>
      )}

      {/* Preview captured photo */}
      {photo && (
        <div className="flex flex-col items-center gap-4">
          <div className="flex justify-center mb-6">
            <img
              src={photo}
              alt="Captured Preview"
              className="w-[640px] h-[480px] rounded-lg object-cover border-2 border-gray-300 shadow-md"
            />
          </div>
          <div className="flex gap-4">
            <button
              onClick={handleRetake}
              className="px-6 py-3 bg-gray-500 text-white font-semibold rounded-lg hover:bg-gray-600 transition-colors duration-300"
            >
              Retake Photo
            </button>
            <button
              onClick={handleContinue}
              className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors duration-300"
            >
              Continue
            </button>
          </div>
        </div>
      )}

      {/* Hidden canvas element for capturing the photo */}
      <canvas ref={canvasRef} className="hidden"></canvas>
    </div>
  );
};

export default CheckIn;
