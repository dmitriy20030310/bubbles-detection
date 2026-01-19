// service/src/components/TestModelPage/TestModelPage.js
import React, { useState, useEffect } from 'react';
import './TestModelPage.css';

const TestModelPage = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState('');
  const [status, setStatus] = useState('idle');
  const [resultImage, setResultImage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    return () => {
      if (preview) URL.revokeObjectURL(preview);
    };
  }, [preview]);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      setPreview(URL.createObjectURL(selected));
      // setTaskID(null);
      setStatus('idle');
      setResultImage('');
      setError('');
    }
  };


  const handleSubmit = async () => {
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  setStatus('processing');
  setError('');
  setResultImage('');

  try {
    const response = await fetch('http://localhost:8000/use_model', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) throw new Error(`Ошибка: ${response.status}`);

    const data = await response.json();
    if (data.error) throw new Error(data.error);

    setResultImage(data.image); // base64
    setStatus('done');
  } catch (err) {
    setError(err.message);
    setStatus('error');
  }
};


  return (
    <section id="test-model" className="test-model-page">
      <h2>Тестирование модели детекции спутников</h2>

      <div className="upload-section">
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button onClick={handleSubmit} disabled={!file || status !== 'idle'}>
          {status === 'uploading' ? 'Загрузка...' : 'Отправить'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {preview && (
        <div className="result-section">
          <h3>Оригинал</h3>
          <img
            src={preview}
            alt="Оригинал"
            style={{ width: '100%', height: 'auto', border: '1px solid #ccc' }}
          />
        </div>
      )}

      {status === 'processing' && <p>Обработка изображения...</p>}

      {status === 'done' && resultImage && (
        <div className="result-section">
          <h3>Результат (с боксами)</h3>
          <img
            src={`data:image/jpeg;base64,${resultImage}`}
            alt="С предсказаниями"
            style={{ width: '100%', height: 'auto', border: '1px solid #00ff00' }}
          />
        </div>
      )}
    </section>
  );
};

export default TestModelPage;
