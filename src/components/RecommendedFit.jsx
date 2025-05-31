import React from 'react';
import './recommendedFit.css';

const RecommendedFit = () => {
  const [data, setData] = React.useState([]);

  const url = "https://api.escuelajs.co/api/v1/products?limit=10";
  //const url = "https://fakestoreapi.com/products/category/women's%20clothing";

  React.useEffect(() => {
    async function getData() {
      const dataJson = await fetch(url);
      const resp = await dataJson.json();
      console.log(resp)
      setData(resp)
    }
    getData()
  }, []);

  
  const eleList = data.map((item) => (
    <div className="fit-card" key={item.id}>
      <img src={item.images[0]} alt={item.title} className="fit-image" />
      <div className="fit-info">
        <h3>{item.title}</h3>
        <p>${item.price}</p>
      </div>
    </div>
  ));

  return (
    <div className="recommended-fit">
      <h1 className="fit-heading">Current Affairs</h1>
      <div className="fit-grid">
        {eleList}
      </div>
    </div>
  );
};

export default RecommendedFit;
