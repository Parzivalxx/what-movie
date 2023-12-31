const PageContent = ({ title, children }) => {
  return (
    <div className="text-center pt-5">
      <h1>{title}</h1>
      {children}
    </div>
  );
};

export default PageContent;
