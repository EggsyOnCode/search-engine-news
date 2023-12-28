import React, { useState } from "react";
import axios from "axios";

const NewDoc = () => {
  const [showModal, setShowModal] = useState(false);
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("json_file", file);

    try {
      const result = await axios.post(
        "http://localhost:5000/addDoc",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Accept: "application/json", // Specify JSON mimetype
          },
        }
      );
      console.log(result.data);
      // Optionally, perform actions after successful submission
    } catch (error) {
      // Handle errors
    }
  };

  return (
    <div>
      <button onClick={() => setShowModal(true)}>Add New Document</button>

      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <span className="close" onClick={() => setShowModal(false)}>
              &times;
            </span>
            <h2>Add JSON Document</h2>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleSubmit}>Submit</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default NewDoc;
