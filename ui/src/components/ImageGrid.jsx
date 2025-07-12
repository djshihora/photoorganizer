function ImageGrid({ images }) {
  return (
    <div className="grid">
      {images.map((img, i) => (
        <img key={i} src={`file://${img}`} alt="" />
      ))}
    </div>
  );
}

export default ImageGrid;
