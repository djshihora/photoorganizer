import { useState } from 'react';
import Sidebar from './components/Sidebar';
import ImageGrid from './components/ImageGrid';

function App() {
  const [folder, setFolder] = useState(null);
  const [images, setImages] = useState([]);

  const handleSelectFolder = async () => {
    const selected = await window.electronAPI.selectFolder();
    if (!selected) return;
    setFolder(selected);
    const output = await window.electronAPI.scanFolder(selected);
    try {
      const data = JSON.parse(output);
      setImages(data.map((entry) => entry.path));
    } catch (err) {
      console.error('Failed to parse CLI output', err, output);
    }
  };

  return (
    <div className="app">
      <Sidebar onSelectFolder={handleSelectFolder} folder={folder} />
      <ImageGrid images={images} />
    </div>
  );
}

export default App;
