import React, {useState} from 'react';
import './Redcapfilter.css';
import BarChart from './BarChart';

function NumberRangeFilter(props) {
  const [greaterThan, setGreaterThan] = useState("");
  const [lessThan, setLessThan] = useState("");
  const [data, setData] = useState(null);
  const [fetching, setFetching] = useState(null);
  const [disableButton, setDisableButton] = useState(false);

  async function fetchData(){
    setDisableButton(true);
    setFetching(true);
    let url = '/api/data/' + props.data.api + '?';
    let params = new URLSearchParams();
    if(props.data.api == 'raw-calc'){
      params.set('name', props.data.name);
    }
    if(greaterThan !== "") params.set('min', greaterThan);
    if(lessThan !== "") params.set('max', lessThan);
    const response = await fetch(url + params);
    let data = await response.json();
    setData(data);
    setFetching(false);
    var cohort = [];
    for(var key in data){
      cohort = cohort.concat(data[key]);
    }
    props.fetch(props.data.name, cohort);
  }

  let summary = <></>;
  let total_count = '';
  if(data !== null){
    let patient_count = 0;
    for(var col in data){
      patient_count += data[col].length;
    }
    total_count = patient_count + ' total subjects';
    summary = <div>
      <BarChart data={data}/>
    </div>
  }

  return (
    <div className="form_box">
      <button className="remove-button" onClick={() => props.remove(props.data.name)}>X</button>
      <h4>{props.data.name}</h4>
      <p>{props.data.label}</p>
      <div className="boxes">
        <div className="num_boxes">
          <label>Greater than or equal to</label>
          <input type='number'
             value={greaterThan}
             onChange={(e) => {
               setDisableButton(false);
               setGreaterThan(e.target.value);
             }}
             placeholder="Greater than..."/>
        </div>
        <div className="num_boxes">
          <label>Less than or equal to</label>
          <input type='number'
             value={lessThan}
             onChange={(e) => {
               setDisableButton(false);
               setLessThan(e.target.value);
             }}
             placeholder="Less than..."/>
         </div>
      </div>
      <div className="fetch-button">
        <button onClick={fetchData} disabled={disableButton}>Fetch Data</button>
        {fetching === true ? <span>...</span> : <></>}
        <span>{total_count}</span>
      </div>
      <div>{summary}</div>
    </div>
  );
}

export default NumberRangeFilter;
