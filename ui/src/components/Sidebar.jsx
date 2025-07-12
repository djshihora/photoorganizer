function Sidebar({ onSelectFolder, folder }) {
  return (
    <div className="sidebar">
      <button onClick={onSelectFolder}>Choose Folder</button>
      {folder && <p>{folder}</p>}
    </div>
  );
}

export default Sidebar;
