import React, { useState } from "react";
import StyledContainer from "../components/StyledContainer";
import StyledHeader from "../components/StyledHeader";
import StyledForm from "../components/StyledForm";
import StyledButton from "../components/StyledButton";
import StyledMessage from "../components/StyledMessage";
import StyledFileName from "../components/StyledFileName";
import StyledFileInput from "../components/StyledFileInput";
import StyledHiddenInput from "../components/StyledHiddenInput";



function FileUploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState<string>("No file chosen");
  const [message, setMessage] = useState<{ text: string; color: string }>({
    text: "",
    color: "green",
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFile(e.target.files ? e.target.files[0] : null);
    setFileName(e.target.files ? e.target.files[0].name : "");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://localhost:8000/upload/", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      setMessage({ text: "File uploaded successfully", color: "green" });
      setTimeout(() => setMessage({ text: "", color: "green" }), 5000);
    } else {
      setMessage({ text: "Failed to upload file", color: "red" });
      setTimeout(() => setMessage({ text: "", color: "green" }), 5000);
    }
  };

  return (
    <StyledContainer>
      <StyledForm onSubmit={handleSubmit}>
        <StyledHeader>CSV Uploader</StyledHeader>
        <StyledFileInput>
          Choose File
          <StyledHiddenInput type="file" onChange={handleFileChange} />
        </StyledFileInput>
        {fileName && <StyledFileName>{fileName}</StyledFileName>}
        <StyledButton type="submit">Upload</StyledButton>
        {message.text && (
          <StyledMessage color={message.color}>{message.text}</StyledMessage>
        )}
      </StyledForm>
    </StyledContainer>
  );
}

export default FileUploadPage;
