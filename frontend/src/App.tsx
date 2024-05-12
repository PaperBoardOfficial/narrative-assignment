import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FileUploadPage from './pages/FileUploadPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<FileUploadPage />} />
      </Routes>
    </Router>
  );
}

export default App;